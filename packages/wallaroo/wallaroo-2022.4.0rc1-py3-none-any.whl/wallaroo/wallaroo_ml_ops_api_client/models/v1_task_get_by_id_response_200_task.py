from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.v1_task_get_by_id_response_200_task_attempt_output_item import \
    V1TaskGetByIdResponse200TaskAttemptOutputItem
from ..models.v1_task_get_by_id_response_200_task_flavor_type_0 import \
    V1TaskGetByIdResponse200TaskFlavorType0
from ..models.v1_task_get_by_id_response_200_task_flavor_type_1 import \
    V1TaskGetByIdResponse200TaskFlavorType1
from ..models.v1_task_get_by_id_response_200_task_flavor_type_2 import \
    V1TaskGetByIdResponse200TaskFlavorType2
from ..models.v1_task_get_by_id_response_200_task_status_type_0 import \
    V1TaskGetByIdResponse200TaskStatusType0
from ..models.v1_task_get_by_id_response_200_task_status_type_1 import \
    V1TaskGetByIdResponse200TaskStatusType1
from ..models.v1_task_get_by_id_response_200_task_status_type_2 import \
    V1TaskGetByIdResponse200TaskStatusType2
from ..models.v1_task_get_by_id_response_200_task_status_type_3 import \
    V1TaskGetByIdResponse200TaskStatusType3
from ..models.v1_task_get_by_id_response_200_task_status_type_4 import \
    V1TaskGetByIdResponse200TaskStatusType4
from ..models.v1_task_get_by_id_response_200_task_status_type_5 import \
    V1TaskGetByIdResponse200TaskStatusType5
from ..models.v1_task_get_by_id_response_200_task_status_type_6 import \
    V1TaskGetByIdResponse200TaskStatusType6
from ..models.v1_task_get_by_id_response_200_task_status_type_7 import \
    V1TaskGetByIdResponse200TaskStatusType7
from ..models.v1_task_get_by_id_response_200_task_task_type_type_0 import \
    V1TaskGetByIdResponse200TaskTaskTypeType0
from ..models.v1_task_get_by_id_response_200_task_task_type_type_1 import \
    V1TaskGetByIdResponse200TaskTaskTypeType1
from ..models.v1_task_get_by_id_response_200_task_task_type_type_2 import \
    V1TaskGetByIdResponse200TaskTaskTypeType2
from ..models.v1_task_get_by_id_response_200_task_task_type_type_3 import \
    V1TaskGetByIdResponse200TaskTaskTypeType3
from ..types import UNSET, Unset

T = TypeVar("T", bound="V1TaskGetByIdResponse200Task")

@attr.s(auto_attribs=True)
class V1TaskGetByIdResponse200Task:
    """ The task by it's given id

    Attributes:
        id (str):
        status (Union[V1TaskGetByIdResponse200TaskStatusType0, V1TaskGetByIdResponse200TaskStatusType1,
            V1TaskGetByIdResponse200TaskStatusType2, V1TaskGetByIdResponse200TaskStatusType3,
            V1TaskGetByIdResponse200TaskStatusType4, V1TaskGetByIdResponse200TaskStatusType5,
            V1TaskGetByIdResponse200TaskStatusType6, V1TaskGetByIdResponse200TaskStatusType7]):
        flavor (Union[V1TaskGetByIdResponse200TaskFlavorType0, V1TaskGetByIdResponse200TaskFlavorType1,
            V1TaskGetByIdResponse200TaskFlavorType2]):
        subject (str):
        task_type (Union[V1TaskGetByIdResponse200TaskTaskTypeType0, V1TaskGetByIdResponse200TaskTaskTypeType1,
            V1TaskGetByIdResponse200TaskTaskTypeType2, V1TaskGetByIdResponse200TaskTaskTypeType3]):
        next_attempt (Union[Unset, None, int]):
        attempt_output (Union[Unset, None, List[V1TaskGetByIdResponse200TaskAttemptOutputItem]]):
    """

    id: str
    status: Union[V1TaskGetByIdResponse200TaskStatusType0, V1TaskGetByIdResponse200TaskStatusType1, V1TaskGetByIdResponse200TaskStatusType2, V1TaskGetByIdResponse200TaskStatusType3, V1TaskGetByIdResponse200TaskStatusType4, V1TaskGetByIdResponse200TaskStatusType5, V1TaskGetByIdResponse200TaskStatusType6, V1TaskGetByIdResponse200TaskStatusType7]
    flavor: Union[V1TaskGetByIdResponse200TaskFlavorType0, V1TaskGetByIdResponse200TaskFlavorType1, V1TaskGetByIdResponse200TaskFlavorType2]
    subject: str
    task_type: Union[V1TaskGetByIdResponse200TaskTaskTypeType0, V1TaskGetByIdResponse200TaskTaskTypeType1, V1TaskGetByIdResponse200TaskTaskTypeType2, V1TaskGetByIdResponse200TaskTaskTypeType3]
    next_attempt: Union[Unset, None, int] = UNSET
    attempt_output: Union[Unset, None, List[V1TaskGetByIdResponse200TaskAttemptOutputItem]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        status: Union[Dict[str, Any], str]

        if isinstance(self.status, V1TaskGetByIdResponse200TaskStatusType0):
            status = self.status.value

        elif isinstance(self.status, V1TaskGetByIdResponse200TaskStatusType1):
            status = self.status.value

        elif isinstance(self.status, V1TaskGetByIdResponse200TaskStatusType2):
            status = self.status.value

        elif isinstance(self.status, V1TaskGetByIdResponse200TaskStatusType3):
            status = self.status.value

        elif isinstance(self.status, V1TaskGetByIdResponse200TaskStatusType4):
            status = self.status.value

        elif isinstance(self.status, V1TaskGetByIdResponse200TaskStatusType5):
            status = self.status.value

        elif isinstance(self.status, V1TaskGetByIdResponse200TaskStatusType6):
            status = self.status.value

        else:
            status = self.status.to_dict()



        flavor: Union[Dict[str, Any], str]

        if isinstance(self.flavor, V1TaskGetByIdResponse200TaskFlavorType0):
            flavor = self.flavor.value

        elif isinstance(self.flavor, V1TaskGetByIdResponse200TaskFlavorType1):
            flavor = self.flavor.value

        else:
            flavor = self.flavor.to_dict()



        subject = self.subject
        task_type: Union[Dict[str, Any], str]

        if isinstance(self.task_type, V1TaskGetByIdResponse200TaskTaskTypeType0):
            task_type = self.task_type.value

        elif isinstance(self.task_type, V1TaskGetByIdResponse200TaskTaskTypeType1):
            task_type = self.task_type.value

        elif isinstance(self.task_type, V1TaskGetByIdResponse200TaskTaskTypeType2):
            task_type = self.task_type.value

        else:
            task_type = self.task_type.to_dict()



        next_attempt = self.next_attempt
        attempt_output: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.attempt_output, Unset):
            if self.attempt_output is None:
                attempt_output = None
            else:
                attempt_output = []
                for attempt_output_item_data in self.attempt_output:
                    attempt_output_item = attempt_output_item_data.to_dict()

                    attempt_output.append(attempt_output_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "status": status,
            "flavor": flavor,
            "subject": subject,
            "task_type": task_type,
        })
        if next_attempt is not UNSET:
            field_dict["next_attempt"] = next_attempt
        if attempt_output is not UNSET:
            field_dict["attempt_output"] = attempt_output

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        def _parse_status(data: object) -> Union[V1TaskGetByIdResponse200TaskStatusType0, V1TaskGetByIdResponse200TaskStatusType1, V1TaskGetByIdResponse200TaskStatusType2, V1TaskGetByIdResponse200TaskStatusType3, V1TaskGetByIdResponse200TaskStatusType4, V1TaskGetByIdResponse200TaskStatusType5, V1TaskGetByIdResponse200TaskStatusType6, V1TaskGetByIdResponse200TaskStatusType7]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = V1TaskGetByIdResponse200TaskStatusType0(data)



                return status_type_0
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_1 = V1TaskGetByIdResponse200TaskStatusType1(data)



                return status_type_1
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_2 = V1TaskGetByIdResponse200TaskStatusType2(data)



                return status_type_2
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_3 = V1TaskGetByIdResponse200TaskStatusType3(data)



                return status_type_3
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_4 = V1TaskGetByIdResponse200TaskStatusType4(data)



                return status_type_4
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_5 = V1TaskGetByIdResponse200TaskStatusType5(data)



                return status_type_5
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_6 = V1TaskGetByIdResponse200TaskStatusType6(data)



                return status_type_6
            except: # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            status_type_7 = V1TaskGetByIdResponse200TaskStatusType7.from_dict(data)



            return status_type_7

        status = _parse_status(d.pop("status"))


        def _parse_flavor(data: object) -> Union[V1TaskGetByIdResponse200TaskFlavorType0, V1TaskGetByIdResponse200TaskFlavorType1, V1TaskGetByIdResponse200TaskFlavorType2]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                flavor_type_0 = V1TaskGetByIdResponse200TaskFlavorType0(data)



                return flavor_type_0
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                flavor_type_1 = V1TaskGetByIdResponse200TaskFlavorType1(data)



                return flavor_type_1
            except: # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            flavor_type_2 = V1TaskGetByIdResponse200TaskFlavorType2.from_dict(data)



            return flavor_type_2

        flavor = _parse_flavor(d.pop("flavor"))


        subject = d.pop("subject")

        def _parse_task_type(data: object) -> Union[V1TaskGetByIdResponse200TaskTaskTypeType0, V1TaskGetByIdResponse200TaskTaskTypeType1, V1TaskGetByIdResponse200TaskTaskTypeType2, V1TaskGetByIdResponse200TaskTaskTypeType3]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                task_type_type_0 = V1TaskGetByIdResponse200TaskTaskTypeType0(data)



                return task_type_type_0
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                task_type_type_1 = V1TaskGetByIdResponse200TaskTaskTypeType1(data)



                return task_type_type_1
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                task_type_type_2 = V1TaskGetByIdResponse200TaskTaskTypeType2(data)



                return task_type_type_2
            except: # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            task_type_type_3 = V1TaskGetByIdResponse200TaskTaskTypeType3.from_dict(data)



            return task_type_type_3

        task_type = _parse_task_type(d.pop("task_type"))


        next_attempt = d.pop("next_attempt", UNSET)

        attempt_output = []
        _attempt_output = d.pop("attempt_output", UNSET)
        for attempt_output_item_data in (_attempt_output or []):
            attempt_output_item = V1TaskGetByIdResponse200TaskAttemptOutputItem.from_dict(attempt_output_item_data)



            attempt_output.append(attempt_output_item)


        v1_task_get_by_id_response_200_task = cls(
            id=id,
            status=status,
            flavor=flavor,
            subject=subject,
            task_type=task_type,
            next_attempt=next_attempt,
            attempt_output=attempt_output,
        )

        v1_task_get_by_id_response_200_task.additional_properties = d
        return v1_task_get_by_id_response_200_task

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
