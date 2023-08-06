from enum import Enum


class V1TaskGetByWorkspaceResponse200TasksItemStatusType1(str, Enum):
    FAILED = "Failed"

    def __str__(self) -> str:
        return str(self.value)