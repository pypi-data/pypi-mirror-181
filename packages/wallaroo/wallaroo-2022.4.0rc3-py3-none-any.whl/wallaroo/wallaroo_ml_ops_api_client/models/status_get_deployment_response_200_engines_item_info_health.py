from enum import Enum


class StatusGetDeploymentResponse200EnginesItemInfoHealth(str, Enum):
    ERROR = "Error"
    STARTING = "Starting"
    RUNNING = "Running"

    def __str__(self) -> str:
        return str(self.value)