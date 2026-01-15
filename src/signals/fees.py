def estimate_total_cost_pct(fees_cfg):
    # simplified model: taker fee on both legs + small fixed withdrawal cost approximation
    taker = fees_cfg["taker_pct"]
    withdrawal_usd = fees_cfg["withdrawal_usd"]
    # convert fixed withdrawal into rough percent proxy (kept minimal and documented)
    fixed_proxy_pct = min(withdrawal_usd / 1000 * 100, 0.2)
    return (taker * 2) + fixed_proxy_pct
