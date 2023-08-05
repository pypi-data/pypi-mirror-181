from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.v1_task_get_by_workspace_response_200_tasks_item_flavor_type_0 import \
    V1TaskGetByWorkspaceResponse200TasksItemFlavorType0
from ..models.v1_task_get_by_workspace_response_200_tasks_item_flavor_type_1 import \
    V1TaskGetByWorkspaceResponse200TasksItemFlavorType1
from ..models.v1_task_get_by_workspace_response_200_tasks_item_flavor_type_2 import \
    V1TaskGetByWorkspaceResponse200TasksItemFlavorType2
from ..models.v1_task_get_by_workspace_response_200_tasks_item_status_type_0 import \
    V1TaskGetByWorkspaceResponse200TasksItemStatusType0
from ..models.v1_task_get_by_workspace_response_200_tasks_item_status_type_1 import \
    V1TaskGetByWorkspaceResponse200TasksItemStatusType1
from ..models.v1_task_get_by_workspace_response_200_tasks_item_status_type_2 import \
    V1TaskGetByWorkspaceResponse200TasksItemStatusType2
from ..models.v1_task_get_by_workspace_response_200_tasks_item_status_type_3 import \
    V1TaskGetByWorkspaceResponse200TasksItemStatusType3
from ..models.v1_task_get_by_workspace_response_200_tasks_item_status_type_4 import \
    V1TaskGetByWorkspaceResponse200TasksItemStatusType4
from ..models.v1_task_get_by_workspace_response_200_tasks_item_status_type_5 import \
    V1TaskGetByWorkspaceResponse200TasksItemStatusType5
from ..models.v1_task_get_by_workspace_response_200_tasks_item_status_type_6 import \
    V1TaskGetByWorkspaceResponse200TasksItemStatusType6
from ..models.v1_task_get_by_workspace_response_200_tasks_item_status_type_7 import \
    V1TaskGetByWorkspaceResponse200TasksItemStatusType7

T = TypeVar("T", bound="V1TaskGetByWorkspaceResponse200TasksItem")

@attr.s(auto_attribs=True)
class V1TaskGetByWorkspaceResponse200TasksItem:
    """
    Attributes:
        id (str):
        flavor (Union[V1TaskGetByWorkspaceResponse200TasksItemFlavorType0,
            V1TaskGetByWorkspaceResponse200TasksItemFlavorType1, V1TaskGetByWorkspaceResponse200TasksItemFlavorType2]):
        subject (str):
        status (Union[V1TaskGetByWorkspaceResponse200TasksItemStatusType0,
            V1TaskGetByWorkspaceResponse200TasksItemStatusType1, V1TaskGetByWorkspaceResponse200TasksItemStatusType2,
            V1TaskGetByWorkspaceResponse200TasksItemStatusType3, V1TaskGetByWorkspaceResponse200TasksItemStatusType4,
            V1TaskGetByWorkspaceResponse200TasksItemStatusType5, V1TaskGetByWorkspaceResponse200TasksItemStatusType6,
            V1TaskGetByWorkspaceResponse200TasksItemStatusType7]):
        attempt (int):
    """

    id: str
    flavor: Union[V1TaskGetByWorkspaceResponse200TasksItemFlavorType0, V1TaskGetByWorkspaceResponse200TasksItemFlavorType1, V1TaskGetByWorkspaceResponse200TasksItemFlavorType2]
    subject: str
    status: Union[V1TaskGetByWorkspaceResponse200TasksItemStatusType0, V1TaskGetByWorkspaceResponse200TasksItemStatusType1, V1TaskGetByWorkspaceResponse200TasksItemStatusType2, V1TaskGetByWorkspaceResponse200TasksItemStatusType3, V1TaskGetByWorkspaceResponse200TasksItemStatusType4, V1TaskGetByWorkspaceResponse200TasksItemStatusType5, V1TaskGetByWorkspaceResponse200TasksItemStatusType6, V1TaskGetByWorkspaceResponse200TasksItemStatusType7]
    attempt: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        flavor: Union[Dict[str, Any], str]

        if isinstance(self.flavor, V1TaskGetByWorkspaceResponse200TasksItemFlavorType0):
            flavor = self.flavor.value

        elif isinstance(self.flavor, V1TaskGetByWorkspaceResponse200TasksItemFlavorType1):
            flavor = self.flavor.value

        else:
            flavor = self.flavor.to_dict()



        subject = self.subject
        status: Union[Dict[str, Any], str]

        if isinstance(self.status, V1TaskGetByWorkspaceResponse200TasksItemStatusType0):
            status = self.status.value

        elif isinstance(self.status, V1TaskGetByWorkspaceResponse200TasksItemStatusType1):
            status = self.status.value

        elif isinstance(self.status, V1TaskGetByWorkspaceResponse200TasksItemStatusType2):
            status = self.status.value

        elif isinstance(self.status, V1TaskGetByWorkspaceResponse200TasksItemStatusType3):
            status = self.status.value

        elif isinstance(self.status, V1TaskGetByWorkspaceResponse200TasksItemStatusType4):
            status = self.status.value

        elif isinstance(self.status, V1TaskGetByWorkspaceResponse200TasksItemStatusType5):
            status = self.status.value

        elif isinstance(self.status, V1TaskGetByWorkspaceResponse200TasksItemStatusType6):
            status = self.status.value

        else:
            status = self.status.to_dict()



        attempt = self.attempt

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "flavor": flavor,
            "subject": subject,
            "status": status,
            "attempt": attempt,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        def _parse_flavor(data: object) -> Union[V1TaskGetByWorkspaceResponse200TasksItemFlavorType0, V1TaskGetByWorkspaceResponse200TasksItemFlavorType1, V1TaskGetByWorkspaceResponse200TasksItemFlavorType2]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                flavor_type_0 = V1TaskGetByWorkspaceResponse200TasksItemFlavorType0(data)



                return flavor_type_0
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                flavor_type_1 = V1TaskGetByWorkspaceResponse200TasksItemFlavorType1(data)



                return flavor_type_1
            except: # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            flavor_type_2 = V1TaskGetByWorkspaceResponse200TasksItemFlavorType2.from_dict(data)



            return flavor_type_2

        flavor = _parse_flavor(d.pop("flavor"))


        subject = d.pop("subject")

        def _parse_status(data: object) -> Union[V1TaskGetByWorkspaceResponse200TasksItemStatusType0, V1TaskGetByWorkspaceResponse200TasksItemStatusType1, V1TaskGetByWorkspaceResponse200TasksItemStatusType2, V1TaskGetByWorkspaceResponse200TasksItemStatusType3, V1TaskGetByWorkspaceResponse200TasksItemStatusType4, V1TaskGetByWorkspaceResponse200TasksItemStatusType5, V1TaskGetByWorkspaceResponse200TasksItemStatusType6, V1TaskGetByWorkspaceResponse200TasksItemStatusType7]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = V1TaskGetByWorkspaceResponse200TasksItemStatusType0(data)



                return status_type_0
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_1 = V1TaskGetByWorkspaceResponse200TasksItemStatusType1(data)



                return status_type_1
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_2 = V1TaskGetByWorkspaceResponse200TasksItemStatusType2(data)



                return status_type_2
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_3 = V1TaskGetByWorkspaceResponse200TasksItemStatusType3(data)



                return status_type_3
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_4 = V1TaskGetByWorkspaceResponse200TasksItemStatusType4(data)



                return status_type_4
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_5 = V1TaskGetByWorkspaceResponse200TasksItemStatusType5(data)



                return status_type_5
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_6 = V1TaskGetByWorkspaceResponse200TasksItemStatusType6(data)



                return status_type_6
            except: # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            status_type_7 = V1TaskGetByWorkspaceResponse200TasksItemStatusType7.from_dict(data)



            return status_type_7

        status = _parse_status(d.pop("status"))


        attempt = d.pop("attempt")

        v1_task_get_by_workspace_response_200_tasks_item = cls(
            id=id,
            flavor=flavor,
            subject=subject,
            status=status,
            attempt=attempt,
        )

        v1_task_get_by_workspace_response_200_tasks_item.additional_properties = d
        return v1_task_get_by_workspace_response_200_tasks_item

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
