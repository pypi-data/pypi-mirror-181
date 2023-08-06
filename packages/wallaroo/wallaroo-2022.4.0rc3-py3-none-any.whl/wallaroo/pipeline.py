import datetime
import pathlib
import time
from dataclasses import asdict
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    List,
    Sequence,
    Tuple,
    Union,
    cast,
)

import pandas as pd
import pyarrow as pa  # type: ignore
from dateutil import parser as dateparse

from wallaroo import notify

from . import queries
from .checks import Alert, Expression, require_dns_compliance
from .deployment import Deployment
from .deployment_config import DeploymentConfig
from .explainability import ExplainabilityConfig, ExplainabilityConfigList
from .inference_result import InferenceResult
from .logs import LogEntries, LogEntriesShadowDeploy
from .model import Model
from .model_config import ModelConfig
from .object import *
from .pipeline_config import PipelineConfigBuilder, Step
from .unwrap import unwrap
from .visibility import _Visibility

if TYPE_CHECKING:
    # Imports that happen below in methods to fix circular import dependency
    # issues need to also be specified here to satisfy mypy type checking.
    from .client import Client
    from .deployment import Deployment
    from .pipeline_variant import PipelineVariant
    from .tag import Tag


def update_timestamp(f):
    def _inner(self, *args, **kwargs):
        results = f(self, *args, **kwargs)
        if isinstance(results, list):
            self._last_infer_time = max(r.timestamp() for r in results)
        elif isinstance(results, pd.DataFrame):
            if "time" in results:
                self._last_infer_time = results["time"].max()
        elif isinstance(results, pa.Table):
            if "time" in results:
                min_max_time = pa.compute.min_max(results["time"])
                self._last_infer_time = min_max_time["max"].as_py()

        return results

    return _inner


class Pipeline(Object):
    """A pipeline is an execution context for models. Pipelines contain Steps, which are often Models. Pipelines can be deployed or undeployed."""

    def __init__(
        self,
        client: Optional["Client"],
        data: Dict[str, Any],
    ) -> None:
        from .pipeline_config import PipelineConfigBuilder  # avoids circular imports

        self.client = client
        assert client is not None

        # We track the last timestamp received as a hack, so that we can wait for logs
        # that are still being processed.
        self._last_infer_time = None

        # We will shim through to all builder methods but return self so we can chain pipeline
        # calls. See "Shims" below. Using multiple inheritance from the PipelineConfigBuilder was
        # another option considered, and maybe it's an option, but shims let us fiddle with args
        # individually if needed.
        self._builder = None
        self._deployment = None

        super().__init__(gql_client=client._gql_client, data=data)

    def __repr__(self) -> str:
        return str(
            {
                "name": self.name(),
                "create_time": self.create_time(),
                "definition": self.definition(),
            }
        )

    def _html_steptable(self) -> str:
        models = self._fetch_models()
        return ", ".join(models)

        # Yes this is biased towards models only
        # TODO: other types of steps
        # steps = self.steps()
        # steptable = ""
        # if steps:
        #     rows = ""
        #     for step in steps:
        #         rows += step._repr_html_()
        #     steptable = f"<table>{rows}</table>"
        # else:
        #     steptable = "(no steps)"
        # return steptable

    def _repr_html_(self) -> str:
        tags = ", ".join([tag.tag() for tag in self.tags()])
        deployment = self._deployment_for_pipeline()
        deployed = "(none)" if deployment is None else deployment.deployed()
        variants = ", ".join([variant.name() for variant in self.variants()])

        return (
            f"<table>"
            f"<tr><th>name</th> <td>{self.name()}</td></tr>"
            f"<tr><th>created</th> <td>{self.create_time()}</td></tr>"
            f"<tr><th>last_updated</th> <td>{self.last_update_time()}</td></tr>"
            f"<tr><th>deployed</th> <td>{deployed}</td></tr>"
            f"<tr><th>tags</th> <td>{tags}</td></tr>"
            f"<tr><th>versions</th> <td>{variants}</td></tr>"
            f"<tr><th>steps</th> <td>{self._html_steptable()}</td></tr>"
            f"</table>"
        )

    def _is_named(self) -> bool:
        try:
            self.name()
            return True
        except:
            return False

    def builder(self) -> "PipelineConfigBuilder":
        if self._builder is None:
            self._builder = PipelineConfigBuilder(
                self.client,
                pipeline_name=self.name(),
                standalone=False,
            )
        return cast(PipelineConfigBuilder, self._builder)

    def _fill(self, data: Dict[str, Any]) -> None:
        from .pipeline_variant import PipelineVariant  # avoids circular imports
        from .tag import Tag

        for required_attribute in ["id"]:
            if required_attribute not in data:
                raise RequiredAttributeMissing(
                    self.__class__.__name__, required_attribute
                )
        self._id = data["id"]

        # Optional
        self._owner_id = value_if_present(data, "owner_id")

        # Optional
        self._tags = (
            [Tag(self.client, tag["tag"]) for tag in data["pipeline_tags"]]
            if "pipeline_tags" in data
            else DehydratedValue()
        )
        self._create_time = (
            dateparse.isoparse(data["created_at"])
            if "created_at" in data
            else DehydratedValue()
        )
        self._last_update_time = (
            dateparse.isoparse(data["updated_at"])
            if "updated_at" in data
            else DehydratedValue()
        )
        self._name = value_if_present(data, "pipeline_id")
        self._variants = (
            [PipelineVariant(self.client, elem) for elem in data["pipeline_versions"]]
            if "pipeline_versions" in data
            else DehydratedValue()
        )

    def _fetch_attributes(self) -> Dict[str, Any]:
        assert self.client is not None
        return self.client._gql_client.execute(
            gql.gql(
                """
            query PipelineById($pipeline_id: bigint!) {
                pipeline_by_pk(id: $pipeline_id) {
                    id
                    pipeline_id
                    created_at
                    updated_at
                    visibility
                    owner_id
                    pipeline_versions(order_by: {id: desc}) {
                        id
                    }
                    pipeline_tags {
                      tag {
                        id
                        tag
                      }
                    }
                }
            }
                """
            ),
            variable_values={
                "pipeline_id": self._id,
            },
        )["pipeline_by_pk"]

    def _update_visibility(self, visibility: _Visibility):
        assert self.client is not None
        return self._fill(
            self.client._gql_client.execute(
                gql.gql(
                    """
                mutation UpdatePipelineVisibility(
                    $pipeline_id: bigint!,
                    $visibility: String
                ) {
                  update_pipeline(
                    where: {id: {_eq: $pipeline_id}},
                    _set: {visibility: $visibility}) {
                      returning  {
                          id
                          pipeline_id
                          created_at
                          updated_at
                          visibility
                          owner_id
                          pipeline_versions(order_by: {id: desc}) {
                                id
                            }
                        }
                    }
                }
                """
                ),
                variable_values={
                    "pipeline_id": self._id,
                    "visibility": visibility,
                },
            )["update_pipeline"]["returning"][0]
        )

    def _fetch_models(self):
        """Load deployment and any models associated, used only for listing and searching cases."""
        data = self._gql_client.execute(
            gql.gql(queries.named("PipelineModels")),
            variable_values={"pipeline_id": self.id()},
        )
        names = []
        try:
            mc_nodes = data["pipeline_by_pk"]["deployment"][
                "deployment_model_configs_aggregate"
            ]["nodes"]
            names = [mc["model_config"]["model"]["model"]["name"] for mc in mc_nodes]
        except Exception:
            pass
        return names

    def id(self) -> int:
        return self._id

    @rehydrate("_owner_id")
    def owner_id(self) -> str:
        return cast(str, self._owner_id)

    @rehydrate("_create_time")
    def create_time(self) -> datetime.datetime:
        return cast(datetime.datetime, self._create_time)

    @rehydrate("_last_update_time")
    def last_update_time(self) -> datetime.datetime:
        return cast(datetime.datetime, self._last_update_time)

    @rehydrate("_name")
    def name(self) -> str:
        return cast(str, self._name)

    @rehydrate("_variants")
    def variants(self) -> List["PipelineVariant"]:
        from .pipeline_variant import PipelineVariant  # avoids import cycles

        return cast(List[PipelineVariant], self._variants)

    @rehydrate("_tags")
    def tags(self) -> List["Tag"]:
        from .tag import Tag

        return cast(List[Tag], self._tags)

    def logs(self, limit: int = 100, valid: Optional[bool] = None) -> LogEntries:
        topic = self.get_topic_name()

        if valid is False:
            topic += "-failures"
        assert self.client is not None

        [entries, status] = self.client.get_logs(topic, limit)

        # XXX: hack to attempt to align logs with received inference results.
        # Ideally we'd use indices from plateau directly for querying, but the
        # engine currently does not support that.
        if self._last_infer_time is not None:
            for ix in range(5):
                if entries and self._last_infer_time <= max(
                    e.timestamp for e in entries
                ):
                    break

                time.sleep(1)
                [entries, status] = self.client.get_logs(topic, limit)

        if status == "ByteLimited":
            returned = len(entries)
            print(
                f"Warning: only displaying {returned} log messages (of {limit} requested) due to payload size limitations."
            )

        return entries

    def logs_shadow_deploy(self):
        logs = self.logs()
        return LogEntriesShadowDeploy(logs)

    def url(self) -> str:
        """Returns the inference URL for this pipeline."""
        deployment = self._deployment_for_pipeline()
        if deployment is None:
            raise RuntimeError("Pipeline has not been deployed and has no url")
        else:
            return deployment.url()

    def deploy(
        self,
        pipeline_name: Optional[str] = None,
        deployment_config: Optional[DeploymentConfig] = None,
    ) -> "Pipeline":
        """Deploy pipeline. `pipeline_name` is optional if deploy was called previously. When specified,
        `pipeline_name` must be ASCII alpha-numeric characters, plus dash (-) only."""
        if pipeline_name is not None:
            require_dns_compliance(pipeline_name)
        self._deploy_upload_optional(pipeline_name, deployment_config)
        return self

    def definition(self) -> str:
        """Get the current definition of the pipeline as a string"""
        return str(self.builder().steps)

    def _deploy_upload_optional(
        self,
        pipeline_name: Optional[str] = None,
        deployment_config: Optional[DeploymentConfig] = None,
        upload: bool = True,
    ) -> "Pipeline":
        """INTERNAL USE ONLY: This is used in convenience methods that create pipelines"""

        if pipeline_name is None:
            if not self._is_named():
                raise RuntimeError(
                    "pipeline_name is required when pipeline was not previously deployed."
                )
            else:
                pipeline_name = self.name()
        if upload:
            self._upload()

        self._deployment = self.variants()[0].deploy(
            deployment_name=pipeline_name,
            model_configs=self.builder()._model_configs(),
            config=deployment_config,
        )
        return self

    def _deployment_for_pipeline(self) -> Optional["Deployment"]:
        """Fetch a pipeline's deployment."""
        if self._deployment is not None:
            return self._deployment

        res = self._gql_client.execute(
            gql.gql(
                """
		query GetDeploymentForPipeline($pipeline_id: bigint!) {
		  pipeline_by_pk(id: $pipeline_id) {
		    deployment {
		      id
		      deploy_id
		      deployed
		    }
		  }
		}"""
            ),
            variable_values={
                "pipeline_id": self.id(),
            },
        )
        if not res["pipeline_by_pk"]:
            raise EntityNotFoundError("Pipeline", {"pipeline_id": str(self.id())})

        if res["pipeline_by_pk"]["deployment"]:
            self._deployment = Deployment(
                client=self.client,
                data=res["pipeline_by_pk"]["deployment"],
            )
        return self._deployment

    def get_topic_name(self) -> str:
        if self.client is None:
            return f"pipeline-{self.name()}-inference"
        return self.client.get_topic_name(self.id())

    # -----------------------------------------------------------------------------
    # Shims for Deployment methods
    # -----------------------------------------------------------------------------

    def undeploy(self) -> "Pipeline":

        assert self.client is not None
        deployment = self._deployment_for_pipeline()
        if deployment:
            deployment.undeploy()
        return self

    @update_timestamp
    def infer(
        self,
        tensor: Union[Dict[str, Any], pd.DataFrame, pa.Table],
        timeout: Optional[Union[int, float]] = None,
        dataset: Optional[Union[Sequence[str], str]] = None,
        dataset_exclude: Optional[Union[Sequence[str], str]] = None,
        dataset_separator: Optional[str] = None,
    ) -> Union[List[InferenceResult], pd.DataFrame, pa.Table]:
        """
        Returns an inference result on this deployment, given a tensor.
        :param: tensor: Union[Dict[str, Any], pd.DataFrame, pa.Table] Inference data. Should be a dictionary.
        Future improvement: will be a pandas dataframe or arrow table
        :param: timeout: Optional[Union[int, float]] infer requests will time out after
            the amount of seconds provided are exceeded. timeout defaults
            to 15 secs.
        :param: dataset: Optional[list] By default this is set to return, ["time", "out"].
            Other available options "check_failures", "metadata"
        :param: dataset_exclude: Optional[Union[Sequence[str], str]] If set, allows user to exclude parts of dataset.
        :param: dataset_separator: Optional[Union[Sequence[str], str]] If set to ".", return dataset will be flattened.
        :return: InferenceResult in dictionary, dataframe or arrow format.
        """
        deployment = self._deployment_for_pipeline()
        if deployment:
            return deployment.infer(
                tensor, timeout, dataset, dataset_exclude, dataset_separator
            )
        else:
            raise RuntimeError("Pipeline {self.name} is not deployed")

    @update_timestamp
    def infer_from_file(
        self,
        filename: Union[str, pathlib.Path],
        timeout: Optional[Union[int, float]] = None,
        dataset: Optional[Sequence[str]] = None,
        exclude: Optional[Sequence[str]] = None,
        dataset_separator: Optional[str] = None,
    ) -> List[InferenceResult]:
        """Returns an inference result on this deployment, given tensors in a file."""

        deployment = self._deployment_for_pipeline()
        if deployment:
            return deployment.infer_from_file(
                filename, timeout, dataset, exclude, dataset_separator
            )
        else:
            raise RuntimeError("Pipeline {self.name} is not deployed")

    async def batch_infer_from_file(
        self,
        filename: Union[str, pathlib.Path],
        data_key: str = "tensor",
        batch_size: int = 1000,
        connector_limit: int = 4,
    ) -> List[InferenceResult]:
        """Async method to run batched inference on a data file for a given deployment.

        :param str filename: path to an existing file with tensor data in JSON format.
        :param str data_key: key which the tensor data is under within the JSON. defaults to "tensor".
        :param int batch_size: batch size to use when sending requests to the engine. defaults to 1000.
        :param int connector_limit: limit for the amount of TCP connections. defaults to 4.
        :return: List of InferenceResult's.
        :rtype: List[InferenceResult]
        """
        deployment = self._deployment_for_pipeline()
        if deployment:
            return await deployment.batch_infer_from_file(
                filename, data_key, batch_size, connector_limit
            )
        else:
            raise RuntimeError("Pipeline {self.name} is not deployed")

    def status(self) -> Dict[str, Any]:
        """Status of pipeline"""
        deployment = self._deployment_for_pipeline()
        if deployment:
            return deployment.status()
        else:
            return {"status": f"Pipeline {self.name()} is not deployed"}

    # -----------------------------------------------------------------------------
    # Accessors for PipelineConfigBuilder attributes. Not exactly shims and they may be changing a
    # contract elsewhere.
    # -----------------------------------------------------------------------------

    def steps(self) -> List[Step]:
        """Returns a list of the steps of a pipeline. Not exactly a shim"""
        return self.builder().steps

    def model_configs(self) -> List[ModelConfig]:
        """Returns a list of the model configs of a pipeline. Not exactly a shim"""
        return self.builder()._model_configs()

    # -----------------------------------------------------------------------------
    # Shims for PipelineConfigBuilder methods
    # -----------------------------------------------------------------------------

    def _upload(self) -> "Pipeline":
        assert self.client is not None

        # Special case: deploying an existing pipeline where pipeline steps are of type ModelInference
        # The builder doesn't get repopulated so we do that here.

        if self.builder().steps == []:
            for step in self.variants()[0].definition()["steps"]:
                if "ModelInference" in step:
                    name = step["ModelInference"]["models"][0]["name"]
                    version = step["ModelInference"]["models"][0]["version"]
                    model = self.client.model_by_name(
                        model_class=name, model_name=version
                    )
                    self.add_model_step(model)

        new_pipeline = self.builder().upload()
        self._fill({"id": new_pipeline.id()})
        return self

    def remove_step(self, index: int) -> "Pipeline":
        """Remove a step at a given index"""
        self.builder().remove_step(index)
        return self

    def add_model_step(self, model: Model) -> "Pipeline":
        """Perform inference with a single model."""
        self.builder().add_model_step(model)
        return self

    def replace_with_model_step(self, index: int, model: Model) -> "Pipeline":
        """Replaces the step at the given index with a model step"""
        self.builder().replace_with_model_step(index, model)
        return self

    def add_multi_model_step(self, models: Iterable[Model]) -> "Pipeline":
        """Perform inference on the same input data for any number of models."""
        self.builder().add_multi_model_step(models)
        return self

    def replace_with_multi_model_step(
        self, index: int, models: Iterable[Model]
    ) -> "Pipeline":
        """Replaces the step at the index with a multi model step"""
        self.builder().replace_with_multi_model_step(index, models)
        return self

    def add_audit(self, slice) -> "Pipeline":
        """Run audit logging on a specified `slice` of model outputs.

        The slice must be in python-like format. `start:`, `start:end`, and
        `:end` are supported.
        """
        self.builder().add_audit(slice)
        return self

    def replace_with_audit(self, index: int, audit_slice: str) -> "Pipeline":
        """Replaces the step at the index with an audit step"""
        self.builder().replace_with_audit(index, audit_slice)
        return self

    def add_select(self, index: int) -> "Pipeline":
        """Select only the model output with the given `index` from an array of
        outputs.
        """
        self.builder().add_select(index)
        return self

    def replace_with_select(self, step_index: int, select_index: int) -> "Pipeline":
        """Replaces the step at the index with a select step"""
        self.builder().replace_with_select(step_index, select_index)
        return self

    def add_key_split(
        self, default: Model, meta_key: str, options: Dict[str, Model]
    ) -> "Pipeline":
        """Split traffic based on the value at a given `meta_key` in the input data,
        routing to the appropriate model.

        If the resulting value is a key in `options`, the corresponding model is used.
        Otherwise, the `default` model is used for inference.
        """
        self.builder().add_key_split(default, meta_key, options)
        return self

    def replace_with_key_split(
        self, index: int, default: Model, meta_key: str, options: Dict[str, Model]
    ) -> "Pipeline":
        """Replace the step at the index with a key split step"""
        self.builder().replace_with_key_split(index, default, meta_key, options)
        return self

    def add_random_split(
        self,
        weighted: Iterable[Tuple[float, Model]],
        hash_key: Optional[str] = None,
    ) -> "Pipeline":
        """Routes inputs to a single model, randomly chosen from the list of
        `weighted` options.

        Each model receives inputs that are approximately proportional to the
        weight it is assigned.  For example, with two models having weights 1
        and 1, each will receive roughly equal amounts of inference inputs. If
        the weights were changed to 1 and 2, the models would receive roughly
        33% and 66% respectively instead.

        When choosing the model to use, a random number between 0.0 and 1.0 is
        generated. The weighted inputs are mapped to that range, and the random
        input is then used to select the model to use. For example, for the
        two-models equal-weight case, a random key of 0.4 would route to the
        first model. 0.6 would route to the second.

        To support consistent assignment to a model, a `hash_key` can be
        specified. This must be between 0.0 and 1.0. The value at this key, when
        present in the input data, will be used instead of a random number for
        model selection.
        """
        self.builder().add_random_split(weighted, hash_key)
        return self

    def replace_with_random_split(
        self,
        index: int,
        weighted: Iterable[Tuple[float, Model]],
        hash_key: Optional[str] = None,
    ) -> "Pipeline":
        """Replace the step at the index with a random split step"""
        self.builder().replace_with_random_split(index, weighted, hash_key)
        return self

    def add_shadow_deploy(
        self, champion: Model, challengers: Iterable[Model]
    ) -> "Pipeline":
        """Create a "shadow deployment" experiment pipeline. The `champion`
        model and all `challengers` are run for each input. The result data for
        all models is logged, but the output of the `champion` is the only
        result returned.

        This is particularly useful for "burn-in" testing a new model with real
        world data without displacing the currently proven model.

        This is currently implemented as three steps: A multi model step, an audit step, and
        a select step. To remove or replace this step, you need to remove or replace
        all three. You can remove steps using pipeline.remove_step
        """
        self.builder().add_shadow_deploy(champion, challengers)
        return self

    def replace_with_shadow_deploy(
        self, index: int, champion: Model, challengers: Iterable[Model]
    ) -> "Pipeline":
        """Replace a given step with a shadow deployment"""
        self.builder().replace_with_shadow_deploy(index, champion, challengers)
        return self

    def add_validation(self, name: str, validation: Expression) -> "Pipeline":
        """Add a `validation` with the given `name`. All validations are run on
        all outputs, and all failures are logged.
        """
        self.builder().add_validation(name, validation)
        return self

    def add_alert(
        self, name: str, alert: Alert, notifications: List[notify.Notification]
    ) -> "Pipeline":
        self.builder().add_alert(name, alert, notifications)
        return self

    def replace_with_alert(
        self,
        index: int,
        name: str,
        alert: Alert,
        notifications: List[notify.Notification],
    ) -> "Pipeline":
        """Replace the step at the given index with the specified alert"""
        self.builder().replace_with_alert(index, name, alert, notifications)
        return self

    def clear(self) -> "Pipeline":
        """
        Remove all steps from the pipeline. This might be desireable if replacing models, for example.
        """
        self.builder().clear()
        return self

    def list_explainability_configs(self) -> List[ExplainabilityConfig]:
        """List the explainability configs we've created."""

        result = unwrap(self.client)._post_rest_api_json(
            f"v1/api/explainability/list_configs_by_pipeline",
            {"pipeline_id": self.id()},
        )
        l = [ExplainabilityConfig(**ec) for ec in result]
        for ec in l:
            ec.client = self.client  # type: ignore
        return ExplainabilityConfigList(l)

    def get_explainability_config(
        self, expr: Union[str, ExplainabilityConfig]
    ) -> ExplainabilityConfig:
        """Get the details of an explainability config."""

        if isinstance(expr, str):
            explainability_config_id = expr
        else:
            explainability_config_id = str(expr.id)

        result = unwrap(self.client)._post_rest_api_json(
            f"v1/api/explainability/get_config",
            {"explainability_config_id": explainability_config_id},
        )

        exp_cfg = ExplainabilityConfig(**result)
        exp_cfg.client = self.client  # type: ignore
        return exp_cfg

    def create_explainability_config(self, feature_names: Sequence[str], num_points=10):
        """Create a shap config to be used later for reference and adhoc requests."""

        output_names = ["output_0"]
        feature_name_list = list(feature_names)
        reference_version = self.variants()[0].name()
        workspace_id = unwrap(self.client).get_current_workspace().id()

        shap_config = ExplainabilityConfig(
            id=None,
            workspace_id=workspace_id,
            reference_pipeline_version=reference_version,
            explainability_pipeline_version=None,
            status={},
            feature_bounds={},
            num_points=num_points,
            feature_names=feature_name_list,
            output_names=output_names,
        )

        result = unwrap(self.client)._post_rest_api_json(
            f"v1/api/explainability/create_config", asdict(shap_config)
        )
        exp_id = result["id"]
        return self.get_explainability_config(exp_id)


class Pipelines(List[Pipeline]):
    """Wraps a list of pipelines for display in a display-aware environment like Jupyter."""

    def _repr_html_(self) -> str:
        def row(pipeline):
            steptable = pipeline._html_steptable()
            fmt = pipeline.client._time_format
            tags = ", ".join([tag.tag() for tag in pipeline.tags()])
            deployment = pipeline._deployment_for_pipeline()
            depstr = "(unknown)" if deployment is None else deployment.deployed()
            variants = ", ".join([variant.name() for variant in pipeline.variants()])

            return (
                "<tr>"
                + f"<td>{pipeline.name()}</td>"
                + f"<td>{pipeline.create_time().strftime(fmt)}</td>"
                + f"<td>{pipeline.last_update_time().strftime(fmt)}</td>"
                + f"<td>{depstr}</td>"
                + f"<td>{tags}</td>"
                + f"<td>{variants}</td>"
                + f"<td>{steptable}</td>"
                + "</tr>"
            )

        fields = [
            "name",
            "created",
            "last_updated",
            "deployed",
            "tags",
            "versions",
            "steps",
        ]

        if self == []:
            return "(no pipelines)"
        else:
            return (
                "<table>"
                + "<tr><th>"
                + "</th><th>".join(fields)
                + "</th></tr>"
                + ("".join([row(p) for p in self]))
                + "</table>"
            )
