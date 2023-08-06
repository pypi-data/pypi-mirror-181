from enum import Enum


class V1TaskGetByWorkspaceResponse200TasksItemStatusType2(str, Enum):
    PENDING = "Pending"

    def __str__(self) -> str:
        return str(self.value)