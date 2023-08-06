from enum import Enum


class V1TaskGetByIdResponse200TaskStatusType6(str, Enum):
    SUCCESS = "Success"

    def __str__(self) -> str:
        return str(self.value)