def calc_spread_pct(buy, sell):
    if buy <= 0:
        return 0.0
    return (sell - buy) / buy * 100
