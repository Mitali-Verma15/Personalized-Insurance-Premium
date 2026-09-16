import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# ==================================================
# LOAD DATA
# ==================================================

df = pd.read_csv("insurance_synthetic.csv")

X = df.drop(columns=["premium"])
y = df["premium"]

# ==================================================
# TRAIN TEST SPLIT
# ==================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# ==================================================
# PREPROCESSING
# ==================================================

cat_cols = X.select_dtypes(include="object").columns.tolist()

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            cat_cols
        )
    ],
    remainder="passthrough"
)

# ==================================================
# MODEL
# ==================================================

model = RandomForestRegressor(
    n_estimators=500,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", model)
])

# ==================================================
# TRAIN
# ==================================================

pipeline.fit(X_train, y_train)

# ==================================================
# EVALUATION
# ==================================================

predictions = pipeline.predict(X_test)

r2 = r2_score(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)

print("\nModel Performance")
print("-" * 30)
print(f"R² Score : {r2:.4f}")
print(f"MAE      : ₹{mae:.2f}")

# ==================================================
# SAVE MODEL
# ==================================================

joblib.dump(
    pipeline,
    "premium_model.pkl"
)

print("\nModel saved successfully!")
