from enum import Enum


class V1TaskGetByStatusJsonBodyTaskStatusType3(str, Enum):
    RESOURCECONTENTION = "ResourceContention"

    def __str__(self) -> str:
        return str(self.value)