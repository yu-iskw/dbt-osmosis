from __future__ import annotations

from .base import SchemaEngine
from .v1_10 import V110Engine
from .v1_legacy import LegacyEngine

_REGISTRY = {
    "legacy": LegacyEngine(),
    "1.10": V110Engine(),
}


def get_engine(version: str) -> SchemaEngine:
    if version not in _REGISTRY:
        raise ValueError(f"Unknown YAML schema version: {version}")
    return _REGISTRY[version]


__all__ = [
    "SchemaEngine",
    "get_engine",
]
