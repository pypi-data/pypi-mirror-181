from enum import Enum


class V1TaskGetByStatusJsonBodyTaskStatusType6(str, Enum):
    SUCCESS = "Success"

    def __str__(self) -> str:
        return str(self.value)