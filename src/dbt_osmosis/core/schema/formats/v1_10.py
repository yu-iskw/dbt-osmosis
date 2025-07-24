from __future__ import annotations

import copy
import typing as t


class V110Engine:
    """Schema engine that moves certain keys under a config block."""

    version = "1.10"
    MOVED_KEYS = {"meta", "tags", "docs", "group", "access", "freshness"}

    def load(self, doc: dict[str, t.Any]) -> dict[str, t.Any]:
        data = copy.deepcopy(doc)
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
        data = copy.deepcopy(doc)
        for section in ("models", "sources", "seeds", "snapshots"):
            for entry in data.get(section, []):
                self._push_config(entry)
                for col in entry.get("columns", []):
                    self._push_column_config(col)
                if section == "sources":
                    for tbl in entry.get("tables", []):
                        self._push_config(tbl)
                        for col in tbl.get("columns", []):
                            self._push_column_config(col)
        return data

    def migrate(self, doc: dict[str, t.Any]) -> dict[str, t.Any]:
        """Migrate a legacy document to v1.10 layout."""
        return self.dump(doc)

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

    def _push_config(self, entry: dict[str, t.Any]) -> None:
        cfg = entry.get("config", {})
        meta = entry.pop("meta", None)
        if meta is not None:
            cfg.setdefault("meta", meta)
        for k in self.MOVED_KEYS - {"meta"}:
            val = entry.pop(k, None)
            if val is not None:
                cfg.setdefault(k, val)
        if cfg:
            entry["config"] = cfg
        else:
            entry.pop("config", None)

    def _push_column_config(self, col: dict[str, t.Any]) -> None:
        cfg = col.get("config", {})
        meta = col.pop("meta", None)
        if meta is not None:
            cfg.setdefault("meta", meta)
        if cfg:
            col["config"] = cfg
        else:
            col.pop("config", None)


__all__ = ["V110Engine"]
