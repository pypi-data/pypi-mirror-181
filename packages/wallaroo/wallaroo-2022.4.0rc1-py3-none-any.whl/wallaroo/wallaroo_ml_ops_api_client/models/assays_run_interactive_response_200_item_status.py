from enum import Enum


class AssaysRunInteractiveResponse200ItemStatus(str, Enum):
    OK = "Ok"
    WARNING = "Warning"
    ALERT = "Alert"
    BASELINERUN = "BaselineRun"

    def __str__(self) -> str:
        return str(self.value)