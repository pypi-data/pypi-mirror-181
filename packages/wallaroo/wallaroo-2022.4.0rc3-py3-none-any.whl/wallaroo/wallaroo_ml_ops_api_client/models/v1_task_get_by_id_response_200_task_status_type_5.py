from enum import Enum


class V1TaskGetByIdResponse200TaskStatusType5(str, Enum):
    STARTED = "Started"

    def __str__(self) -> str:
        return str(self.value)