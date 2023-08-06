from enum import Enum


class V1TaskGetByWorkspaceResponse200TasksItemFlavorType0(str, Enum):
    DATACONNECTOR = "DataConnector"

    def __str__(self) -> str:
        return str(self.value)