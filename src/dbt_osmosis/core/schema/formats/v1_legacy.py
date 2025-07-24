from __future__ import annotations

import copy
import typing as t


class LegacyEngine:
    """Schema engine for the legacy YAML layout used prior to dbt 1.10."""

    version = "legacy"
    MOVED_KEYS = {"meta", "tags", "docs", "group", "access", "freshness"}

    def load(self, doc: dict[str, t.Any]) -> dict[str, t.Any]:
        """Normalize YAML that may contain ``config`` blocks to the legacy shape."""
        data = t.cast(dict[str, t.Any], copy.deepcopy(doc))
        for section in ("models", "sources", "seeds", "snapshots"):
            for entry in data.get(section, []):
                self._pull_config(entry)
                for col in entry.get("columns", []):
                    self._pull_column_config(col)
                if section == "sources":
                    for tbl in entry.get("tables", []):
                        self._pull_config(tbl)
                        for col in tbl.get("columns", []):
                            self._pull_column_config(col)
        return data

    def dump(self, doc: dict[str, t.Any]) -> dict[str, t.Any]:
        """Return YAML in the legacy layout (no ``config`` wrappers)."""
        # ``load`` already returns the document with config keys pulled up, so we
        # reuse it to ensure any stray config blocks are flattened.
        return self.load(doc)

    def migrate(self, doc: dict[str, t.Any]) -> dict[str, t.Any]:
        """Alias for ``load`` allowing v1.10 documents to be downgraded."""
        return self.load(doc)

    def _pull_config(self, entry: dict[str, t.Any]) -> None:
        cfg = entry.pop("config", {})
        meta = cfg.pop("meta", None)
        if meta is not None:
            entry.setdefault("meta", meta)
        for k in self.MOVED_KEYS - {"meta"}:
            if k in cfg:
                entry.setdefault(k, cfg.pop(k))
        if cfg:
            entry["config"] = cfg

    def _pull_column_config(self, col: dict[str, t.Any]) -> None:
        cfg = col.pop("config", {})
        meta = cfg.pop("meta", None)
        if meta is not None:
            col.setdefault("meta", meta)
        if cfg:
            col["config"] = cfg


__all__ = ["LegacyEngine"]
