from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.v1_task_get_by_id_response_200_task_attempt_output_item_error_data import \
    V1TaskGetByIdResponse200TaskAttemptOutputItemErrorData
from ..models.v1_task_get_by_id_response_200_task_attempt_output_item_output_data import \
    V1TaskGetByIdResponse200TaskAttemptOutputItemOutputData
from ..models.v1_task_get_by_id_response_200_task_attempt_output_item_status_type_0 import \
    V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType0
from ..models.v1_task_get_by_id_response_200_task_attempt_output_item_status_type_1 import \
    V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType1
from ..models.v1_task_get_by_id_response_200_task_attempt_output_item_status_type_2 import \
    V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType2
from ..models.v1_task_get_by_id_response_200_task_attempt_output_item_status_type_3 import \
    V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType3
from ..models.v1_task_get_by_id_response_200_task_attempt_output_item_status_type_4 import \
    V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType4
from ..models.v1_task_get_by_id_response_200_task_attempt_output_item_status_type_5 import \
    V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType5
from ..models.v1_task_get_by_id_response_200_task_attempt_output_item_status_type_6 import \
    V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType6
from ..models.v1_task_get_by_id_response_200_task_attempt_output_item_status_type_7 import \
    V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType7
from ..types import UNSET, Unset

T = TypeVar("T", bound="V1TaskGetByIdResponse200TaskAttemptOutputItem")

@attr.s(auto_attribs=True)
class V1TaskGetByIdResponse200TaskAttemptOutputItem:
    """
    Attributes:
        id (str):
        attempt (int):
        status (Union[V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType0,
            V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType1,
            V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType2,
            V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType3,
            V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType4,
            V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType5,
            V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType6,
            V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType7]):
        start_time (str):
        error_data (Union[Unset, None, V1TaskGetByIdResponse200TaskAttemptOutputItemErrorData]):
        output_data (Union[Unset, None, V1TaskGetByIdResponse200TaskAttemptOutputItemOutputData]):
        end_time (Union[Unset, None, str]):
    """

    id: str
    attempt: int
    status: Union[V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType0, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType1, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType2, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType3, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType4, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType5, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType6, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType7]
    start_time: str
    error_data: Union[Unset, None, V1TaskGetByIdResponse200TaskAttemptOutputItemErrorData] = UNSET
    output_data: Union[Unset, None, V1TaskGetByIdResponse200TaskAttemptOutputItemOutputData] = UNSET
    end_time: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        attempt = self.attempt
        status: Union[Dict[str, Any], str]

        if isinstance(self.status, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType0):
            status = self.status.value

        elif isinstance(self.status, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType1):
            status = self.status.value

        elif isinstance(self.status, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType2):
            status = self.status.value

        elif isinstance(self.status, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType3):
            status = self.status.value

        elif isinstance(self.status, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType4):
            status = self.status.value

        elif isinstance(self.status, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType5):
            status = self.status.value

        elif isinstance(self.status, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType6):
            status = self.status.value

        else:
            status = self.status.to_dict()



        start_time = self.start_time
        error_data: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.error_data, Unset):
            error_data = self.error_data.to_dict() if self.error_data else None

        output_data: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.output_data, Unset):
            output_data = self.output_data.to_dict() if self.output_data else None

        end_time = self.end_time

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "attempt": attempt,
            "status": status,
            "start_time": start_time,
        })
        if error_data is not UNSET:
            field_dict["error_data"] = error_data
        if output_data is not UNSET:
            field_dict["output_data"] = output_data
        if end_time is not UNSET:
            field_dict["end_time"] = end_time

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        attempt = d.pop("attempt")

        def _parse_status(data: object) -> Union[V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType0, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType1, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType2, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType3, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType4, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType5, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType6, V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType7]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType0(data)



                return status_type_0
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_1 = V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType1(data)



                return status_type_1
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_2 = V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType2(data)



                return status_type_2
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_3 = V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType3(data)



                return status_type_3
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_4 = V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType4(data)



                return status_type_4
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_5 = V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType5(data)



                return status_type_5
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_6 = V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType6(data)



                return status_type_6
            except: # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            status_type_7 = V1TaskGetByIdResponse200TaskAttemptOutputItemStatusType7.from_dict(data)



            return status_type_7

        status = _parse_status(d.pop("status"))


        start_time = d.pop("start_time")

        _error_data = d.pop("error_data", UNSET)
        error_data: Union[Unset, None, V1TaskGetByIdResponse200TaskAttemptOutputItemErrorData]
        if _error_data is None:
            error_data = None
        elif isinstance(_error_data,  Unset):
            error_data = UNSET
        else:
            error_data = V1TaskGetByIdResponse200TaskAttemptOutputItemErrorData.from_dict(_error_data)




        _output_data = d.pop("output_data", UNSET)
        output_data: Union[Unset, None, V1TaskGetByIdResponse200TaskAttemptOutputItemOutputData]
        if _output_data is None:
            output_data = None
        elif isinstance(_output_data,  Unset):
            output_data = UNSET
        else:
            output_data = V1TaskGetByIdResponse200TaskAttemptOutputItemOutputData.from_dict(_output_data)




        end_time = d.pop("end_time", UNSET)

        v1_task_get_by_id_response_200_task_attempt_output_item = cls(
            id=id,
            attempt=attempt,
            status=status,
            start_time=start_time,
            error_data=error_data,
            output_data=output_data,
            end_time=end_time,
        )

        v1_task_get_by_id_response_200_task_attempt_output_item.additional_properties = d
        return v1_task_get_by_id_response_200_task_attempt_output_item

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
