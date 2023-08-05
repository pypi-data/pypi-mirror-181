from enum import Enum


class AssaysRunInteractiveResponse200ItemBaselineSummaryAggregation(str, Enum):
    EDGES = "Edges"
    DENSITY = "Density"
    CUMULATIVE = "Cumulative"

    def __str__(self) -> str:
        return str(self.value)