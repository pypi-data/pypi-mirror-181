from enum import Enum


class V1TaskGetByStatusAndWorkspaceJsonBodyTaskStatusType2(str, Enum):
    PENDING = "Pending"

    def __str__(self) -> str:
        return str(self.value)