from enum import Enum


class V1TaskGetByStatusAndWorkspaceJsonBodyTaskStatusType6(str, Enum):
    SUCCESS = "Success"

    def __str__(self) -> str:
        return str(self.value)