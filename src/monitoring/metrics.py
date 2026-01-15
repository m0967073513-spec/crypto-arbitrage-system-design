
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Metrics:
    started_at: float = field(default_factory=time.time)
    counters: Dict[str, int] = field(default_factory=dict)

    def inc(self, key: str, value: int = 1) -> None:
        self.counters[key] = self.counters.get(key, 0) + value

    def snapshot(self) -> Dict[str, object]:
        uptime_sec = int(time.time() - self.started_at)
        return {
            "uptime_sec": uptime_sec,
            "counters": dict(self.counters),
        }


METRICS = Metrics()


def metric_inc(key: str, value: int = 1) -> None:
    METRICS.inc(key, value)


def metric_snapshot() -> Dict[str, object]:
    return METRICS.snapshot()
