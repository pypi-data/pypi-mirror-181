from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AssaysGetResultsJsonBody")

@attr.s(auto_attribs=True)
class AssaysGetResultsJsonBody:
    """ Request to return assay results.

    Attributes:
        assay_id (Union[Unset, None, int]):  Assay identifier.
        start (Union[Unset, None, str]):  Start date and time.
        end (Union[Unset, None, str]):  End date and time.
        limit (Union[Unset, None, int]):  Maximum number of results to return.
        pipeline_id (Union[Unset, None, int]):  Pipeline identifier.
    """

    assay_id: Union[Unset, None, int] = UNSET
    start: Union[Unset, None, str] = UNSET
    end: Union[Unset, None, str] = UNSET
    limit: Union[Unset, None, int] = UNSET
    pipeline_id: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        assay_id = self.assay_id
        start = self.start
        end = self.end
        limit = self.limit
        pipeline_id = self.pipeline_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if assay_id is not UNSET:
            field_dict["assay_id"] = assay_id
        if start is not UNSET:
            field_dict["start"] = start
        if end is not UNSET:
            field_dict["end"] = end
        if limit is not UNSET:
            field_dict["limit"] = limit
        if pipeline_id is not UNSET:
            field_dict["pipeline_id"] = pipeline_id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assay_id = d.pop("assay_id", UNSET)

        start = d.pop("start", UNSET)

        end = d.pop("end", UNSET)

        limit = d.pop("limit", UNSET)

        pipeline_id = d.pop("pipeline_id", UNSET)

        assays_get_results_json_body = cls(
            assay_id=assay_id,
            start=start,
            end=end,
            limit=limit,
            pipeline_id=pipeline_id,
        )

        assays_get_results_json_body.additional_properties = d
        return assays_get_results_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
