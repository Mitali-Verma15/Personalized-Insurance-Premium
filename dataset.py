import pandas as pd
import numpy as np

np.random.seed(42)

n = 500

df = pd.DataFrame({
    "age": np.random.randint(18, 65, n),
    "gender": np.random.choice(["male", "female"], n),
    "bmi": np.round(np.random.uniform(18, 40, n), 1),
    "children": np.random.randint(0, 6, n),
    "smoker": np.random.choice(["yes", "no"], n, p=[0.2, 0.8]),
    "existing_disease": np.random.choice(["yes", "no"], n, p=[0.15, 0.85]),
    "region": np.random.choice(
        ["northeast", "northwest", "southeast", "southwest"], n)
})

premium = (
    2000
    + df["age"] * 120
    + df["bmi"] * 90
    + df["children"] * 400
    + np.where(df["smoker"] == "yes", 12000, 0)
    + np.where(df["existing_disease"] == "yes", 5000, 0)
    + np.random.normal(0, 1000, n)
)

df["premium"] = premium.astype(int)

df.to_csv("insurance_synthetic.csv", index=False)
print(df.head())