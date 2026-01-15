
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class PositionDecision:
    allowed: bool
    reason: str
    position_usd: float


def decide_position_usd(
    *,
    starting_usd: float,
    max_position_usd: float,
    reserve_usd: float = 50.0,
    requested_usd: Optional[float] = None,
) -> PositionDecision:
    """
    Decide how much USD we can allocate to a simulated position.

    - starting_usd: portfolio size in simulation
    - max_position_usd: hard cap per trade
    - reserve_usd: cash to keep untouched (risk buffer)
    - requested_usd: desired position size (optional)

    Returns:
        PositionDecision(allowed, reason, position_usd)
    """
    if starting_usd <= 0:
        return PositionDecision(False, "invalid_starting_balance", 0.0)

    if max_position_usd <= 0:
        return PositionDecision(False, "invalid_max_position", 0.0)

    if reserve_usd < 0:
        reserve_usd = 0.0

    available = max(starting_usd - reserve_usd, 0.0)
    if available <= 0:
        return PositionDecision(False, "insufficient_funds_after_reserve", 0.0)

    target = requested_usd if requested_usd is not None else max_position_usd
    target = max(0.0, float(target))

    position = min(target, max_position_usd, available)

    if position <= 0:
        return PositionDecision(False, "position_size_zero", 0.0)

    reason = "ok"
    if position < target:
        reason = "capped_by_limits_or_balance"

    return PositionDecision(True, reason, position)


def clamp_thresholds(
    *,
    min_spread_pct: float,
    min_spread_floor_pct: float = 0.0,
    min_spread_cap_pct: float = 10.0,
) -> Tuple[float, str]:
    """
    Optional helper to keep thresholds sane.
    Returns (clamped_value, note).
    """
    note = "ok"
    val = float(min_spread_pct)

    if val < min_spread_floor_pct:
        val = min_spread_floor_pct
        note = "clamped_to_floor"

    if val > min_spread_cap_pct:
        val = min_spread_cap_pct
        note = "clamped_to_cap"

    return val, note
