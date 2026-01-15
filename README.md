# Crypto Arbitrage System Design (Simulation)

Educational portfolio project that demonstrates **how to design a crypto arbitrage pipeline** with a strong focus on **architecture, automation, and risk-aware system design**.

Pipeline overview:  
**data collection → normalization → opportunity detection → risk checks → simulation → monitoring**

⚠️ **Live trading is intentionally disabled.**  
This repository showcases engineering decisions and system design — **not financial execution or profit optimization**.

---

## What This Project Demonstrates

- Modular Python architecture for trading-like systems
- Clean separation of concerns (data, signals, risk, simulation, monitoring)
- Spread and fee modeling with net-edge calculation
- Risk guards and capital management logic
- Paper trading (simulation-only, no real orders)
- Logging and basic observability
- Optional Telegram notifications

This project is designed to resemble **production-grade structure**, while remaining safe and educational.

---

## What Is Intentionally Excluded

- ❌ Exchange API keys or credentials  
- ❌ Order execution or market-making logic  
- ❌ Profit-optimized or real trading parameters  
- ❌ Financial advice  

The goal is to demonstrate **engineering maturity**, not to expose sensitive or commercial logic.

---

## Tech Stack

- Python 3.10+
- requests
- pyyaml
- python-dotenv
- Telegram Bot API (optional, for notifications)

---

## Risk Controls & Safety Design

This project intentionally emphasizes **risk-aware design**, even in simulation mode.

### Implemented safeguards

#### 1. Latency Guard
- Quotes with latency above a configurable threshold are skipped.
- Prevents acting on stale or delayed market data.

#### 2. Fee-Aware Opportunity Filtering
- Spread is evaluated **after accounting for fees and fixed costs**.
- Avoids false-positive opportunities with negative net edge.

#### 3. Position Limits
- Each simulated trade is constrained by:
  - Maximum position size
  - Available balance after reserve
- Prevents over-allocation to a single opportunity.

#### 4. Capital Reserve
- A configurable cash reserve is always kept untouched.
- Simulates conservative capital management.

#### 5. Simulation-Only Execution
- No real exchange connections or order execution.
- Paper trading is used to validate logic safely.

#### 6. Observability
- Minimal runtime metrics are collected:
  - opportunities
  - skipped due to latency
  - blocked by limits
  - no-op evaluations
- Metrics snapshot is logged at the end of each run.

---

## Project Status

🚧 **In progress** — architecture-first implementation.  
The system is intentionally built step by step to keep design decisions explicit and traceable.

---

## Roadmap

- Add more realistic slippage model
- Add backtesting on historical snapshots
- Extend monitoring and metrics
- Improve simulation accuracy
- Add architecture diagram and documentation
