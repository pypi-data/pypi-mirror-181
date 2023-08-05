from enum import Enum


class V1TaskUpdateResponse200DataStatusType6(str, Enum):
    SUCCESS = "Success"

    def __str__(self) -> str:
        return str(self.value)