from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Quote:
    """Normalized quote format used across the pipeline."""
    symbol: str
    buy: float
    sell: float
    latency_ms: int
    ts: int
    source: str = "mock"


def normalize_quote(raw: Dict[str, Any], *, source: str = "unknown") -> Optional[Quote]:
    """
    Convert a raw quote dict into a normalized Quote.
    Returns None if data is invalid.

    Expected raw keys (minimum): symbol, buy, sell, latency_ms, ts
    """
    try:
        symbol = str(raw["symbol"])
        buy = float(raw["buy"])
        sell = float(raw["sell"])
        latency_ms = int(raw.get("latency_ms", 0))
        ts = int(raw.get("ts", 0))
    except (KeyError, TypeError, ValueError):
        return None

    if buy <= 0 or sell <= 0:
        return None

    # Ensure buy <= sell
    buy2 = min(buy, sell)
    sell2 = max(buy, sell)

    return Quote(
        symbol=symbol,
        buy=buy2,
        sell=sell2,
        latency_ms=latency_ms,
        ts=ts,
        source=source,
    )
