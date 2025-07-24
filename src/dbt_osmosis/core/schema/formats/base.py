from __future__ import annotations

import typing as t


class SchemaEngine(t.Protocol):
    """Protocol for schema engines that handle YAML format differences."""

    version: str

    def load(self, doc: dict[str, t.Any]) -> dict[str, t.Any]:
        """Normalize a raw YAML document to the internal representation."""
        ...

    def dump(self, doc: dict[str, t.Any]) -> dict[str, t.Any]:
        """Convert an internal representation back to a YAML document."""
        ...

    def migrate(self, doc: dict[str, t.Any]) -> dict[str, t.Any]:
        """Migrate a legacy YAML document to this engine's format."""
        ...
