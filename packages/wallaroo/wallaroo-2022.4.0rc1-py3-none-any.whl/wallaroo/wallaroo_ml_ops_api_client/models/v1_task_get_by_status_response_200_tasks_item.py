from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.v1_task_get_by_status_response_200_tasks_item_flavor_type_0 import \
    V1TaskGetByStatusResponse200TasksItemFlavorType0
from ..models.v1_task_get_by_status_response_200_tasks_item_flavor_type_1 import \
    V1TaskGetByStatusResponse200TasksItemFlavorType1
from ..models.v1_task_get_by_status_response_200_tasks_item_flavor_type_2 import \
    V1TaskGetByStatusResponse200TasksItemFlavorType2

T = TypeVar("T", bound="V1TaskGetByStatusResponse200TasksItem")

@attr.s(auto_attribs=True)
class V1TaskGetByStatusResponse200TasksItem:
    """
    Attributes:
        id (str):
        flavor (Union[V1TaskGetByStatusResponse200TasksItemFlavorType0,
            V1TaskGetByStatusResponse200TasksItemFlavorType1, V1TaskGetByStatusResponse200TasksItemFlavorType2]):
        subject (str):
        attempt (int):
    """

    id: str
    flavor: Union[V1TaskGetByStatusResponse200TasksItemFlavorType0, V1TaskGetByStatusResponse200TasksItemFlavorType1, V1TaskGetByStatusResponse200TasksItemFlavorType2]
    subject: str
    attempt: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        flavor: Union[Dict[str, Any], str]

        if isinstance(self.flavor, V1TaskGetByStatusResponse200TasksItemFlavorType0):
            flavor = self.flavor.value

        elif isinstance(self.flavor, V1TaskGetByStatusResponse200TasksItemFlavorType1):
            flavor = self.flavor.value

        else:
            flavor = self.flavor.to_dict()



        subject = self.subject
        attempt = self.attempt

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "flavor": flavor,
            "subject": subject,
            "attempt": attempt,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        def _parse_flavor(data: object) -> Union[V1TaskGetByStatusResponse200TasksItemFlavorType0, V1TaskGetByStatusResponse200TasksItemFlavorType1, V1TaskGetByStatusResponse200TasksItemFlavorType2]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                flavor_type_0 = V1TaskGetByStatusResponse200TasksItemFlavorType0(data)



                return flavor_type_0
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                flavor_type_1 = V1TaskGetByStatusResponse200TasksItemFlavorType1(data)



                return flavor_type_1
            except: # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            flavor_type_2 = V1TaskGetByStatusResponse200TasksItemFlavorType2.from_dict(data)



            return flavor_type_2

        flavor = _parse_flavor(d.pop("flavor"))


        subject = d.pop("subject")

        attempt = d.pop("attempt")

        v1_task_get_by_status_response_200_tasks_item = cls(
            id=id,
            flavor=flavor,
            subject=subject,
            attempt=attempt,
        )

        v1_task_get_by_status_response_200_tasks_item.additional_properties = d
        return v1_task_get_by_status_response_200_tasks_item

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
