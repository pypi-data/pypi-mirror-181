from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.v1_task_get_by_id_response_200_task import \
    V1TaskGetByIdResponse200Task

T = TypeVar("T", bound="V1TaskGetByIdResponse200")

@attr.s(auto_attribs=True)
class V1TaskGetByIdResponse200:
    """ Response body of /tasks/get_by_id

    Attributes:
        task (V1TaskGetByIdResponse200Task):  The task by it's given id
    """

    task: V1TaskGetByIdResponse200Task
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        task = self.task.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "task": task,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        task = V1TaskGetByIdResponse200Task.from_dict(d.pop("task"))




        v1_task_get_by_id_response_200 = cls(
            task=task,
        )

        v1_task_get_by_id_response_200.additional_properties = d
        return v1_task_get_by_id_response_200

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
