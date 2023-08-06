from enum import Enum


class V1TaskGetByStatusJsonBodyTaskStatusType4(str, Enum):
    SCHEDULEERROR = "ScheduleError"

    def __str__(self) -> str:
        return str(self.value)