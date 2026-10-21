"""Generate reproducible synthetic payment transactions for coursework."""
import json
import numpy as np
import pandas as pd

SEED = 42
N = 20000

def main():
    rng = np.random.default_rng(SEED)
    amount = np.round(rng.lognormal(mean=3.4, sigma=1.0, size=N), 2)
    hour = rng.integers(0, 24, N)
    distance = np.round(rng.gamma(shape=2.0, scale=35.0, size=N), 2)
    account_age = rng.integers(1, 3650, N)
    device_change = rng.binomial(1, 0.12, N)
    international = rng.binomial(1, 0.08, N)
    merchant = rng.choice(
        ["grocery", "electronics", "travel", "food", "fashion", "digital"],
        size=N, p=[.22, .15, .10, .22, .18, .13]
    )
    # Synthetic label: deliberately rule-based for reproducibility, not real fraud ground truth.
    logit = (
        -4.1
        + 0.0015 * np.clip(amount, 0, 3000)
        + 0.9 * (hour <= 4)
        + 0.012 * np.clip(distance, 0, 300)
        + 1.0 * device_change
        + 1.15 * international
        + 0.55 * (account_age < 30)
    )
    probability = 1 / (1 + np.exp(-logit))
    fraud = rng.binomial(1, probability)
    df = pd.DataFrame({
        "transaction_id": [f"TX{i:07d}" for i in range(N)],
        "customer_id": [f"C{v:06d}" for v in rng.integers(1, 5001, N)],
        "amount": amount,
        "hour": hour,
        "distance_km": distance,
        "account_age_days": account_age,
        "device_change": device_change,
        "international": international,
        "merchant_category": merchant,
        "latitude": np.round(rng.uniform(-55, 70, N), 5),
        "longitude": np.round(rng.uniform(-170, 170, N), 5),
        "is_fraud": fraud.astype(int),
    })
    df.to_csv("transactions.csv", index=False)
    df.to_json("transactions.json", orient="records", lines=True)
    print(f"Created {len(df):,} synthetic transactions.")
    print(f"Synthetic positive-label rate: {df.is_fraud.mean():.2%}")
    print("Files: transactions.csv, transactions.json")
    print("Important: labels are synthetic and rule-generated; do not claim real-world fraud accuracy.")

if __name__ == "__main__":
    main()
