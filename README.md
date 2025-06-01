# Simulated Market

This is a small simulation I made of a simplified market where buyers and sellers negotiate prices over time.

## 🧠 What it does

- There are buyers and sellers, each with their own expected prices.
- Every day, they try to make deals.
- If they agree on a price, the transaction happens and both sides get some surplus (basically, profit).
- If they don’t, they adjust their expectations up or down depending on how things went.
- Inflation is also part of the model, so prices can rise slowly over time.

## 🎯 What's the point?

The goal of this simulation is to show how a **free market** works over time and how agents (buyers and sellers) adapt. The focus is on:

- **Optimizing surplus** on both sides (everyone wants to make the best deal possible).
- **Minimizing the number of unsatisfied agents** — people who didn’t manage to buy or sell.
- Showing how agents who are too far from the market (buyers with too low max prices or sellers with too high minimums) eventually get "pushed out" or stop making deals.

In short, it tries to reflect how mismatched expectations naturally get filtered out and how a market self-balances over time.

## 📁 Main files

- `main.py` — the core simulation loop, where the market runs day by day.
- `functions.py` — contains helper functions like inflation logic and price negotiation.
- `README.md` — you're reading it 🙂

## 📊 What it shows

- Average transaction price over time
- Buyer and seller surplus per day
- Number of unsatisfied buyers and sellers per day

## 🚀 How to run it

Just run:

```bash
python main.py
