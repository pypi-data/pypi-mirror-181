from enum import Enum


class AssaysListResponse200ItemSummarizerType0BinMode(str, Enum):
    NONE = "None"
    EQUAL = "Equal"
    QUANTILE = "Quantile"
    PROVIDED = "Provided"

    def __str__(self) -> str:
        return str(self.value)