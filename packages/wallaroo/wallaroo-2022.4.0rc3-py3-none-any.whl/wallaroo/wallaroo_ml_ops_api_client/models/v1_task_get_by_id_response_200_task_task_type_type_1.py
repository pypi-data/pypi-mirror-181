from enum import Enum


class V1TaskGetByIdResponse200TaskTaskTypeType1(str, Enum):
    NETWORKSERVICE = "NetworkService"

    def __str__(self) -> str:
        return str(self.value)