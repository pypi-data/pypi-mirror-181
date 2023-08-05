from enum import Enum


class V1TaskUpdateResponse200DataStatusType4(str, Enum):
    SCHEDULEERROR = "ScheduleError"

    def __str__(self) -> str:
        return str(self.value)