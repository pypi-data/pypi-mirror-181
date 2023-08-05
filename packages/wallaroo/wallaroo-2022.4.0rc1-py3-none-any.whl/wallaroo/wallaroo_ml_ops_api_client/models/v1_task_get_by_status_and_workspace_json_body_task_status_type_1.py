from enum import Enum


class V1TaskGetByStatusAndWorkspaceJsonBodyTaskStatusType1(str, Enum):
    FAILED = "Failed"

    def __str__(self) -> str:
        return str(self.value)