from dotenv import load_dotenv
from .logging_setup import setup_logging
from .config import load_config

from .data.collectors import get_mock_quotes
from .signals.spread import calc_spread_pct
from .signals.fees import estimate_total_cost_pct
from .signals.filters import is_opportunity
from .risk.guards import check_latency
from .simulation.paper_trading import simulate_trade
from .monitoring.telegram import notify

def main():
    load_dotenv()
    logger = setup_logging()
    cfg = load_config()

    logger.info("Starting arbitrage pipeline (SIMULATION)")
    quotes = get_mock_quotes(cfg["symbols"])

    for q in quotes:
        symbol = q["symbol"]
        latency_ms = q["latency_ms"]

        if not check_latency(latency_ms, cfg["thresholds"]["max_latency_ms"]):
            logger.warning(f"[{symbol}] skipped: high latency {latency_ms}ms")
            continue

        spread_pct = calc_spread_pct(q["buy"], q["sell"])
        cost_pct = estimate_total_cost_pct(cfg["fees"])
        net_pct = spread_pct - cost_pct

        if is_opportunity(net_pct, cfg["thresholds"]["min_spread_pct"]):
            result = simulate_trade(symbol=symbol, net_pct=net_pct, cfg=cfg)
            msg = f"✅ Opportunity {symbol}: net={net_pct:.3f}% | sim PnL=${result['pnl_usd']:.2f}"
            logger.info(msg)
            notify(msg)
        else:
            logger.info(f"[{symbol}] no-op: spread={spread_pct:.3f}% cost={cost_pct:.3f}% net={net_pct:.3f}%")

if __name__ == "__main__":
    main()
