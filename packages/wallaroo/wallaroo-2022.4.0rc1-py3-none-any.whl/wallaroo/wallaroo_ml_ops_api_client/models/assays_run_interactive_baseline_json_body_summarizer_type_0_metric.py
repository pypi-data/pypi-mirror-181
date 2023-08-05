from enum import Enum


class AssaysRunInteractiveBaselineJsonBodySummarizerType0Metric(str, Enum):
    MAXDIFF = "MaxDiff"
    SUMDIFF = "SumDiff"
    PSI = "PSI"

    def __str__(self) -> str:
        return str(self.value)