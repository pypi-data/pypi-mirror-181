from enum import Enum


class V1TaskGetByIdResponse200TaskTaskTypeType2(str, Enum):
    ONESHOT = "OneShot"

    def __str__(self) -> str:
        return str(self.value)