from dotenv import load_dotenv

from .logging_setup import setup_logging
from .config import load_config

from .data.collectors import get_mock_quotes
from .data.normalize import normalize_quote

from .signals.spread import calc_spread_pct
from .signals.fees import estimate_total_cost_pct
from .signals.filters import is_opportunity

from .risk.guards import check_latency

from .simulation.paper_trading import simulate_trade
from .simulation.pnl import pnl_usd

from .monitoring.telegram import notify
from .monitoring.metrics import metric_inc, metric_snapshot


def main():
    load_dotenv()
    logger = setup_logging()
    cfg = load_config()

    logger.info("Starting arbitrage pipeline (SIMULATION)")
    raw_quotes = get_mock_quotes(cfg["symbols"])

    for raw in raw_quotes:
        quote = normalize_quote(raw, source="mock")
        if quote is None:
            metric_inc("invalid_quotes")
            continue

        symbol = quote.symbol

        if not check_latency(quote.latency_ms, cfg["thresholds"]["max_latency_ms"]):
            logger.warning(f"[{symbol}] skipped: high latency {quote.latency_ms}ms")
            metric_inc("skipped_latency")
            continue

        spread_pct = calc_spread_pct(quote.buy, quote.sell)
        cost_pct = estimate_total_cost_pct(cfg["fees"])
        net_pct = spread_pct - cost_pct

        if is_opportunity(net_pct, cfg["thresholds"]["min_spread_pct"]):
            position_usd = cfg["simulation"]["max_position_usd"]
            pnl = pnl_usd(position_usd, net_pct)

            simulate_trade(symbol=symbol, net_pct=net_pct, cfg=cfg)

            msg = (
                f"✅ Opportunity {symbol}: "
                f"net={net_pct:.3f}% | sim PnL=${pnl:.2f}"
            )
            logger.info(msg)
            notify(msg)

            metric_inc("opportunities")
        else:
            logger.info(
                f"[{symbol}] no-op: "
                f"spread={spread_pct:.3f}% "
                f"cost={cost_pct:.3f}% "
                f"net={net_pct:.3f}%"
            )
            metric_inc("no_op")

    logger.info(f"Metrics snapshot: {metric_snapshot()}")


if __name__ == "__main__":
    main()
