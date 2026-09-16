import joblib
import pandas as pd

model = joblib.load("premium_model.pkl")


def calculate_premium(
    age,
    gender,
    bmi,
    children,
    smoker,
    region,
    existing_disease
):

    input_df = pd.DataFrame({

        "age": [age],
        "gender": [gender],
        "bmi": [bmi],
        "children": [children],
        "smoker": [smoker],
        "region": [region],
        "existing_disease": [existing_disease]

    })

    premium = float(
        model.predict(input_df)[0]
    )

    risk = 0

    if age > 55:
        risk += 25
    elif age > 40:
        risk += 15

    if bmi > 30:
        risk += 25
    elif bmi > 25:
        risk += 15

    if smoker == "Yes":
        risk += 25

    if existing_disease == "Yes":
        risk += 25

    risk = min(risk, 100)

    if risk >= 70:
        category = "High Risk"

    elif risk >= 40:
        category = "Medium Risk"

    else:
        category = "Low Risk"

    recommendations = []

    if bmi > 30:
        recommendations.append(
            "Weight reduction program recommended."
        )

    if smoker == "Yes":
        recommendations.append(
            "Smoking cessation program recommended."
        )

    if age > 50:
        recommendations.append(
            "Annual preventive health checkup advised."
        )

    if children > 2:
        recommendations.append(
            "Family floater plan may be beneficial."
        )

    if not recommendations:
        recommendations.append(
            "Healthy profile detected."
        )

    if category == "Low Risk":
        plan = "Silver Health Plan"

    elif category == "Medium Risk":
        plan = "Gold Health Plan"

    else:
        plan = "Platinum Health Plan"

    savings = 0

    if smoker == "Yes":
        savings += 5000

    if bmi > 25:
        savings += 3000

    optimized = max(
        premium - savings,
        8000
    )

    return {

        "premium": round(premium),

        "risk_score": risk,

        "risk_category": category,

        "recommendations": recommendations,

        "recommended_plan": plan,

        "optimized_premium": round(optimized),

        "savings": savings

    }