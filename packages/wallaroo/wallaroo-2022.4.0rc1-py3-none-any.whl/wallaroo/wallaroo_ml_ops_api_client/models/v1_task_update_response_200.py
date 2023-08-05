from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.v1_task_update_response_200_data import \
    V1TaskUpdateResponse200Data

T = TypeVar("T", bound="V1TaskUpdateResponse200")

@attr.s(auto_attribs=True)
class V1TaskUpdateResponse200:
    """ Response body of /tasks/get_by_workspace

    Attributes:
        data (V1TaskUpdateResponse200Data):  Response structure for updating a task.
    """

    data: V1TaskUpdateResponse200Data
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        data = self.data.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "data": data,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data = V1TaskUpdateResponse200Data.from_dict(d.pop("data"))




        v1_task_update_response_200 = cls(
            data=data,
        )

        v1_task_update_response_200.additional_properties = d
        return v1_task_update_response_200

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
