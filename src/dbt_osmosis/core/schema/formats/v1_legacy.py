from __future__ import annotations

import typing as t


class LegacyEngine:
    """Pass-through engine for legacy YAML layout."""

    version = "legacy"

    def load(self, doc: dict[str, t.Any]) -> dict[str, t.Any]:
        return doc

    def dump(self, doc: dict[str, t.Any]) -> dict[str, t.Any]:
        return doc

    def migrate(self, doc: dict[str, t.Any]) -> dict[str, t.Any]:
        return doc


__all__ = ["LegacyEngine"]
