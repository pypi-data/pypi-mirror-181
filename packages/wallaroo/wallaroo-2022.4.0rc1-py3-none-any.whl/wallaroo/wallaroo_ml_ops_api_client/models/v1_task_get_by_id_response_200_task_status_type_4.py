from enum import Enum


class V1TaskGetByIdResponse200TaskStatusType4(str, Enum):
    SCHEDULEERROR = "ScheduleError"

    def __str__(self) -> str:
        return str(self.value)