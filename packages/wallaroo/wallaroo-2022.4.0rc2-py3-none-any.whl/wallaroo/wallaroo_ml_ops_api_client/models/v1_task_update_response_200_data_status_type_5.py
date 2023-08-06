from enum import Enum


class V1TaskUpdateResponse200DataStatusType5(str, Enum):
    STARTED = "Started"

    def __str__(self) -> str:
        return str(self.value)