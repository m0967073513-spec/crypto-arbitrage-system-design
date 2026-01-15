def simulate_trade(symbol, net_pct, cfg):
    max_pos = cfg["simulation"]["max_position_usd"]
    pnl = max_pos * (net_pct / 100.0)
    return {"symbol": symbol, "position_usd": max_pos, "pnl_usd": pnl}
