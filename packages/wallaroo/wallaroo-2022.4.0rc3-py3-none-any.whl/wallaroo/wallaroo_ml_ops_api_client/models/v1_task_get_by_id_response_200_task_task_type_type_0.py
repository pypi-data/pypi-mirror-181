from enum import Enum


class V1TaskGetByIdResponse200TaskTaskTypeType0(str, Enum):
    CRON = "Cron"

    def __str__(self) -> str:
        return str(self.value)