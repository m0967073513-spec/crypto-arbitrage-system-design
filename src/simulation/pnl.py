from __future__ import annotations


def pnl_usd(position_usd: float, net_pct: float) -> float:
    """
    Calculate PnL in USD for a simulated trade given net % edge.
    Example: position=200, net_pct=0.25 -> 0.5 USD
    """
    if position_usd <= 0:
        return 0.0
    return position_usd * (net_pct / 100.0)


def roi_pct(pnl_usd_value: float, position_usd: float) -> float:
    """Return ROI % for the simulated trade."""
    if position_usd <= 0:
        return 0.0
    return (pnl_usd_value / position_usd) * 100.0

