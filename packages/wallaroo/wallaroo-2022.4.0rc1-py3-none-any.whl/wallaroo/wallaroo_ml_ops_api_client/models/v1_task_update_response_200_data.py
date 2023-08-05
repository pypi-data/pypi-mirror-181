from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.v1_task_update_response_200_data_status_type_0 import \
    V1TaskUpdateResponse200DataStatusType0
from ..models.v1_task_update_response_200_data_status_type_1 import \
    V1TaskUpdateResponse200DataStatusType1
from ..models.v1_task_update_response_200_data_status_type_2 import \
    V1TaskUpdateResponse200DataStatusType2
from ..models.v1_task_update_response_200_data_status_type_3 import \
    V1TaskUpdateResponse200DataStatusType3
from ..models.v1_task_update_response_200_data_status_type_4 import \
    V1TaskUpdateResponse200DataStatusType4
from ..models.v1_task_update_response_200_data_status_type_5 import \
    V1TaskUpdateResponse200DataStatusType5
from ..models.v1_task_update_response_200_data_status_type_6 import \
    V1TaskUpdateResponse200DataStatusType6
from ..models.v1_task_update_response_200_data_status_type_7 import \
    V1TaskUpdateResponse200DataStatusType7

T = TypeVar("T", bound="V1TaskUpdateResponse200Data")

@attr.s(auto_attribs=True)
class V1TaskUpdateResponse200Data:
    """ Response structure for updating a task.

    Attributes:
        task_id (str):  The updated task id.
        status (Union[V1TaskUpdateResponse200DataStatusType0, V1TaskUpdateResponse200DataStatusType1,
            V1TaskUpdateResponse200DataStatusType2, V1TaskUpdateResponse200DataStatusType3,
            V1TaskUpdateResponse200DataStatusType4, V1TaskUpdateResponse200DataStatusType5,
            V1TaskUpdateResponse200DataStatusType6, V1TaskUpdateResponse200DataStatusType7]):  The last set status, and
            returned status from the task update.
        output_id (str):  The primary key of the output table, for output data either additional or error.
    """

    task_id: str
    status: Union[V1TaskUpdateResponse200DataStatusType0, V1TaskUpdateResponse200DataStatusType1, V1TaskUpdateResponse200DataStatusType2, V1TaskUpdateResponse200DataStatusType3, V1TaskUpdateResponse200DataStatusType4, V1TaskUpdateResponse200DataStatusType5, V1TaskUpdateResponse200DataStatusType6, V1TaskUpdateResponse200DataStatusType7]
    output_id: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        task_id = self.task_id
        status: Union[Dict[str, Any], str]

        if isinstance(self.status, V1TaskUpdateResponse200DataStatusType0):
            status = self.status.value

        elif isinstance(self.status, V1TaskUpdateResponse200DataStatusType1):
            status = self.status.value

        elif isinstance(self.status, V1TaskUpdateResponse200DataStatusType2):
            status = self.status.value

        elif isinstance(self.status, V1TaskUpdateResponse200DataStatusType3):
            status = self.status.value

        elif isinstance(self.status, V1TaskUpdateResponse200DataStatusType4):
            status = self.status.value

        elif isinstance(self.status, V1TaskUpdateResponse200DataStatusType5):
            status = self.status.value

        elif isinstance(self.status, V1TaskUpdateResponse200DataStatusType6):
            status = self.status.value

        else:
            status = self.status.to_dict()



        output_id = self.output_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "task_id": task_id,
            "status": status,
            "output_id": output_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        task_id = d.pop("task_id")

        def _parse_status(data: object) -> Union[V1TaskUpdateResponse200DataStatusType0, V1TaskUpdateResponse200DataStatusType1, V1TaskUpdateResponse200DataStatusType2, V1TaskUpdateResponse200DataStatusType3, V1TaskUpdateResponse200DataStatusType4, V1TaskUpdateResponse200DataStatusType5, V1TaskUpdateResponse200DataStatusType6, V1TaskUpdateResponse200DataStatusType7]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = V1TaskUpdateResponse200DataStatusType0(data)



                return status_type_0
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_1 = V1TaskUpdateResponse200DataStatusType1(data)



                return status_type_1
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_2 = V1TaskUpdateResponse200DataStatusType2(data)



                return status_type_2
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_3 = V1TaskUpdateResponse200DataStatusType3(data)



                return status_type_3
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_4 = V1TaskUpdateResponse200DataStatusType4(data)



                return status_type_4
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_5 = V1TaskUpdateResponse200DataStatusType5(data)



                return status_type_5
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_6 = V1TaskUpdateResponse200DataStatusType6(data)



                return status_type_6
            except: # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            status_type_7 = V1TaskUpdateResponse200DataStatusType7.from_dict(data)



            return status_type_7

        status = _parse_status(d.pop("status"))


        output_id = d.pop("output_id")

        v1_task_update_response_200_data = cls(
            task_id=task_id,
            status=status,
            output_id=output_id,
        )

        v1_task_update_response_200_data.additional_properties = d
        return v1_task_update_response_200_data

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
