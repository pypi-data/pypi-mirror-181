from typing import Optional, TypeVar

T = TypeVar("T")


def unwrap(v: Optional[T]) -> T:
    """Simple function to placate pylance"""
    if v:
        return v
    raise Exception("Expected a value in forced unwrap")
