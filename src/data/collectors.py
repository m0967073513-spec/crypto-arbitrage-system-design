import random
import time

def get_mock_quotes(symbols):
    quotes = []
    for s in symbols:
        base = random.uniform(100, 50000)
        buy = base * (1 + random.uniform(-0.001, 0.001))
        sell = base * (1 + random.uniform(-0.001, 0.001))
        latency_ms = random.randint(200, 2500)
        quotes.append({
            "symbol": s,
            "buy": min(buy, sell),
            "sell": max(buy, sell),
            "latency_ms": latency_ms,
            "ts": int(time.time())
        })
    return quotes
