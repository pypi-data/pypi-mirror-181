from enum import Enum


class V1TaskGetByStatusResponse200TasksItemFlavorType1(str, Enum):
    MODELCONVERSION = "ModelConversion"

    def __str__(self) -> str:
        return str(self.value)