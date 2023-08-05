from enum import Enum


class V1TaskUpdateJsonBodyStatus(str, Enum):
    PENDING = "Pending"
    CRASHLOOP = "CrashLoop"
    FAILED = "Failed"
    SCHEDULEERROR = "ScheduleError"
    STARTED = "Started"
    RESOURCECONTENTION = "ResourceContention"
    SUCCESS = "Success"

    def __str__(self) -> str:
        return str(self.value)