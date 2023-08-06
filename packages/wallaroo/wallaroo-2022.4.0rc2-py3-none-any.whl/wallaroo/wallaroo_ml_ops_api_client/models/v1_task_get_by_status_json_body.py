from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.v1_task_get_by_status_json_body_task_status_type_0 import \
    V1TaskGetByStatusJsonBodyTaskStatusType0
from ..models.v1_task_get_by_status_json_body_task_status_type_1 import \
    V1TaskGetByStatusJsonBodyTaskStatusType1
from ..models.v1_task_get_by_status_json_body_task_status_type_2 import \
    V1TaskGetByStatusJsonBodyTaskStatusType2
from ..models.v1_task_get_by_status_json_body_task_status_type_3 import \
    V1TaskGetByStatusJsonBodyTaskStatusType3
from ..models.v1_task_get_by_status_json_body_task_status_type_4 import \
    V1TaskGetByStatusJsonBodyTaskStatusType4
from ..models.v1_task_get_by_status_json_body_task_status_type_5 import \
    V1TaskGetByStatusJsonBodyTaskStatusType5
from ..models.v1_task_get_by_status_json_body_task_status_type_6 import \
    V1TaskGetByStatusJsonBodyTaskStatusType6
from ..models.v1_task_get_by_status_json_body_task_status_type_7 import \
    V1TaskGetByStatusJsonBodyTaskStatusType7

T = TypeVar("T", bound="V1TaskGetByStatusJsonBody")

@attr.s(auto_attribs=True)
class V1TaskGetByStatusJsonBody:
    """ Body for request to /tasks/get_by_status

    Attributes:
        task_status (Union[V1TaskGetByStatusJsonBodyTaskStatusType0, V1TaskGetByStatusJsonBodyTaskStatusType1,
            V1TaskGetByStatusJsonBodyTaskStatusType2, V1TaskGetByStatusJsonBodyTaskStatusType3,
            V1TaskGetByStatusJsonBodyTaskStatusType4, V1TaskGetByStatusJsonBodyTaskStatusType5,
            V1TaskGetByStatusJsonBodyTaskStatusType6, V1TaskGetByStatusJsonBodyTaskStatusType7]):  The task status to query
            for i.e. Failing
    """

    task_status: Union[V1TaskGetByStatusJsonBodyTaskStatusType0, V1TaskGetByStatusJsonBodyTaskStatusType1, V1TaskGetByStatusJsonBodyTaskStatusType2, V1TaskGetByStatusJsonBodyTaskStatusType3, V1TaskGetByStatusJsonBodyTaskStatusType4, V1TaskGetByStatusJsonBodyTaskStatusType5, V1TaskGetByStatusJsonBodyTaskStatusType6, V1TaskGetByStatusJsonBodyTaskStatusType7]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        task_status: Union[Dict[str, Any], str]

        if isinstance(self.task_status, V1TaskGetByStatusJsonBodyTaskStatusType0):
            task_status = self.task_status.value

        elif isinstance(self.task_status, V1TaskGetByStatusJsonBodyTaskStatusType1):
            task_status = self.task_status.value

        elif isinstance(self.task_status, V1TaskGetByStatusJsonBodyTaskStatusType2):
            task_status = self.task_status.value

        elif isinstance(self.task_status, V1TaskGetByStatusJsonBodyTaskStatusType3):
            task_status = self.task_status.value

        elif isinstance(self.task_status, V1TaskGetByStatusJsonBodyTaskStatusType4):
            task_status = self.task_status.value

        elif isinstance(self.task_status, V1TaskGetByStatusJsonBodyTaskStatusType5):
            task_status = self.task_status.value

        elif isinstance(self.task_status, V1TaskGetByStatusJsonBodyTaskStatusType6):
            task_status = self.task_status.value

        else:
            task_status = self.task_status.to_dict()




        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "task_status": task_status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        def _parse_task_status(data: object) -> Union[V1TaskGetByStatusJsonBodyTaskStatusType0, V1TaskGetByStatusJsonBodyTaskStatusType1, V1TaskGetByStatusJsonBodyTaskStatusType2, V1TaskGetByStatusJsonBodyTaskStatusType3, V1TaskGetByStatusJsonBodyTaskStatusType4, V1TaskGetByStatusJsonBodyTaskStatusType5, V1TaskGetByStatusJsonBodyTaskStatusType6, V1TaskGetByStatusJsonBodyTaskStatusType7]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                task_status_type_0 = V1TaskGetByStatusJsonBodyTaskStatusType0(data)



                return task_status_type_0
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                task_status_type_1 = V1TaskGetByStatusJsonBodyTaskStatusType1(data)



                return task_status_type_1
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                task_status_type_2 = V1TaskGetByStatusJsonBodyTaskStatusType2(data)



                return task_status_type_2
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                task_status_type_3 = V1TaskGetByStatusJsonBodyTaskStatusType3(data)



                return task_status_type_3
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                task_status_type_4 = V1TaskGetByStatusJsonBodyTaskStatusType4(data)



                return task_status_type_4
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                task_status_type_5 = V1TaskGetByStatusJsonBodyTaskStatusType5(data)



                return task_status_type_5
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                task_status_type_6 = V1TaskGetByStatusJsonBodyTaskStatusType6(data)



                return task_status_type_6
            except: # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            task_status_type_7 = V1TaskGetByStatusJsonBodyTaskStatusType7.from_dict(data)



            return task_status_type_7

        task_status = _parse_task_status(d.pop("task_status"))


        v1_task_get_by_status_json_body = cls(
            task_status=task_status,
        )

        v1_task_get_by_status_json_body.additional_properties = d
        return v1_task_get_by_status_json_body

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
