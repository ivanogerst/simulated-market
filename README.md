# Simulated Market

This is a small simulation I made of a simplified market where buyers and sellers negotiate prices over time.

## 🧠 What it does

- There are buyers and sellers, each with their own expected prices.
- Every day, they try to make deals.
- If they agree on a price, the transaction happens and both sides get some surplus (basically, profit).
- If they don’t, they adjust their expectations.
- There's also inflation, so prices can slowly increase over time.

## 📁 Main files

- `main.py` — the core simulation loop, where the market runs day by day.
- `functions.py` — contains helper functions like inflation logic and price negotiation.
- `README.md` — you're reading it 🙂

## 📊 Output

- Plots showing:
  - Average transaction price over time
  - Buyer/seller surplus each day
  - How many sellers didn’t sell / buyers didn’t buy

## 🚀 How to run it

Just run:

python main.py
