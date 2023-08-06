from importlib import resources

from . import graphql


def named(name: str) -> str:
    return resources.read_text(graphql, f"{name}.graphql")
