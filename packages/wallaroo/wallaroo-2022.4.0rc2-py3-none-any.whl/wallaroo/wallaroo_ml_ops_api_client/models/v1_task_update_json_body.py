from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.v1_task_update_json_body_additional_data import \
    V1TaskUpdateJsonBodyAdditionalData
from ..models.v1_task_update_json_body_error_data import \
    V1TaskUpdateJsonBodyErrorData
from ..models.v1_task_update_json_body_status import V1TaskUpdateJsonBodyStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="V1TaskUpdateJsonBody")

@attr.s(auto_attribs=True)
class V1TaskUpdateJsonBody:
    """ Body for request to /tasks/get_by_workspace   The Request body for v1.task.update

    Attributes:
        task_id (str):  The primary id of the task.
        attempt (int):  The attempt number of this update.
        status (V1TaskUpdateJsonBodyStatus):  The status of the task.
        additional_data (Union[Unset, None, V1TaskUpdateJsonBodyAdditionalData]):  Any additional output data from the
            task as a json value.
        error_data (Union[Unset, None, V1TaskUpdateJsonBodyErrorData]):  Any additional error output as a json value.
        end_time (Union[Unset, None, str]):  The end time of the task if finished, optional can be null to denote not
            finished.
    """

    task_id: str
    attempt: int
    status: V1TaskUpdateJsonBodyStatus
    additional_data: Union[Unset, None, V1TaskUpdateJsonBodyAdditionalData] = UNSET
    error_data: Union[Unset, None, V1TaskUpdateJsonBodyErrorData] = UNSET
    end_time: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        task_id = self.task_id
        attempt = self.attempt
        status = self.status.value

        additional_data: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.additional_data, Unset):
            additional_data = self.additional_data.to_dict() if self.additional_data else None

        error_data: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.error_data, Unset):
            error_data = self.error_data.to_dict() if self.error_data else None

        end_time = self.end_time

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "task_id": task_id,
            "attempt": attempt,
            "status": status,
        })
        if additional_data is not UNSET:
            field_dict["additional_data"] = additional_data
        if error_data is not UNSET:
            field_dict["error_data"] = error_data
        if end_time is not UNSET:
            field_dict["end_time"] = end_time

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        task_id = d.pop("task_id")

        attempt = d.pop("attempt")

        status = V1TaskUpdateJsonBodyStatus(d.pop("status"))




        _additional_data = d.pop("additional_data", UNSET)
        additional_data: Union[Unset, None, V1TaskUpdateJsonBodyAdditionalData]
        if _additional_data is None:
            additional_data = None
        elif isinstance(_additional_data,  Unset):
            additional_data = UNSET
        else:
            additional_data = V1TaskUpdateJsonBodyAdditionalData.from_dict(_additional_data)




        _error_data = d.pop("error_data", UNSET)
        error_data: Union[Unset, None, V1TaskUpdateJsonBodyErrorData]
        if _error_data is None:
            error_data = None
        elif isinstance(_error_data,  Unset):
            error_data = UNSET
        else:
            error_data = V1TaskUpdateJsonBodyErrorData.from_dict(_error_data)




        end_time = d.pop("end_time", UNSET)

        v1_task_update_json_body = cls(
            task_id=task_id,
            attempt=attempt,
            status=status,
            additional_data=additional_data,
            error_data=error_data,
            end_time=end_time,
        )

        v1_task_update_json_body.additional_properties = d
        return v1_task_update_json_body

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
