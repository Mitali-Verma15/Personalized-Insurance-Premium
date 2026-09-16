import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from model import calculate_premium

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Personalized Insurance Premium Advisor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>
.main > div {
    padding-top: 0.5rem;
}

.stApp {
    background-color: #f8fafc;
}

[data-testid="stMetric"] {
    background:white;
    border-radius:14px;
    padding:15px;
    border-left:5px solid #2563eb;
    box-shadow:0px 2px 8px rgba(0,0,0,0.08);
}

.block-container {
    padding-top:1rem;
    padding-bottom:1rem;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():
    return pd.read_csv("insurance_synthetic.csv")

df = load_data()

# ==================================================
# HEADER
# ==================================================

st.title("🏥 Personalized Insurance Premium Advisor")

# ==================================================
# SESSION STATE
# ==================================================

if "result" not in st.session_state:
    st.session_state.result = calculate_premium(
        30,
        "Male",
        24.0,
        0,
        "No",
        "North",
        "No"
    )

# ==================================================
# TABS
# ==================================================

tab1, tab2, tab3 = st.tabs([
    "📊 Dashboard",
    "🧮 Premium Calculator",
    "🚦 Risk Assessment"
])

# ==================================================
# TAB 1 : DASHBOARD
# ==================================================

with tab1:

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Customers", f"{len(df):,}")
    c2.metric("Revenue", f"₹{int(df['premium'].sum()):,}")
    c3.metric("Avg Premium", f"₹{int(df['premium'].mean()):,}")
    c4.metric("Avg BMI", round(df["bmi"].mean(), 1))

    row1_left, row1_right = st.columns([2, 1])

    with row1_left:

        fig1 = px.histogram(
            df,
            x="premium",
            nbins=20,
            title="Premium Distribution"
        )

        fig1.update_layout(height=320)

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with row1_right:

        smoker_premium = (
            df.groupby("smoker")["premium"]
            .mean()
            .reset_index()
        )

        fig2 = px.bar(
            smoker_premium,
            x="smoker",
            y="premium",
            color="smoker",
            title="Smoking Impact"
        )

        fig2.update_layout(height=320)

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    row2_left, row2_right = st.columns(2)

    with row2_left:

        disease_df = (
            df.groupby("existing_disease")["premium"]
            .mean()
            .reset_index()
        )

        fig3 = px.bar(
            disease_df,
            x="existing_disease",
            y="premium",
            color="existing_disease",
            title="Disease Impact"
        )

        fig3.update_layout(height=320)

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    with row2_right:

        age_df = (
            df.groupby("age")["premium"]
            .mean()
            .reset_index()
        )

        fig4 = px.line(
            age_df,
            x="age",
            y="premium",
            markers=True,
            title="Premium vs Age"
        )

        fig4.update_layout(height=320)

        st.plotly_chart(
            fig4,
            use_container_width=True
        )


    with st.expander("Customer Dataset Preview"):

        st.dataframe(
            df.head(20),
            use_container_width=True,
            height=350
        )

# ==================================================
# TAB 2 : PREMIUM CALCULATOR
# ==================================================

with tab2:

    st.subheader("Premium Calculator")

    col1, col2 = st.columns(2)

    with col1:

        age = st.slider("Age", 18, 80, 30)

        bmi = st.slider(
            "BMI",
            15.0,
            45.0,
            24.0
        )

        children = st.slider(
            "Children",
            0,
            6,
            0
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )

    with col2:

        smoker = st.selectbox(
            "Smoker",
            ["No", "Yes"]
        )

        existing_disease = st.selectbox(
            "Existing Disease",
            ["No", "Yes"]
        )

        region = st.selectbox(
            "Region",
            ["North", "South", "East", "West"]
        )

    if st.button(
        "Calculate Premium",
        type="primary"
    ):

        st.session_state.result = calculate_premium(
            age,
            gender,
            bmi,
            children,
            smoker,
            region,
            existing_disease
        )

    result = st.session_state.result

    st.success(
        f"Predicted Premium: ₹{result['premium']:,}"
    )


    report_df = pd.DataFrame({
        "Metric": [
            "Predicted Premium",
            "Risk Score",
            "Risk Category",
            "Recommended Plan",
            "Optimized Premium",
            "Potential Savings"
        ],
        "Value": [
            result["premium"],
            result["risk_score"],
            result["risk_category"],
            result["recommended_plan"],
            result["optimized_premium"],
            result["savings"]
        ]
    })

    st.download_button(
        label="📥 Download Prediction Report",
        data=report_df.to_csv(index=False),
        file_name="insurance_prediction_report.csv",
        mime="text/csv"
    )

    age_factor = min(age / 80, 1)
    bmi_factor = min(abs(bmi - 22) / 20, 1)
    smoker_factor = 1 if smoker == "Yes" else 0.3
    disease_factor = 1 if existing_disease == "Yes" else 0.2

    total_factor = (
        age_factor +
        bmi_factor +
        smoker_factor +
        disease_factor
    )

    breakdown = pd.DataFrame({
        "Component": [
            "Age Impact",
            "BMI Impact",
            "Smoking Impact",
            "Disease Impact"
        ],
        "Value": [
            result["premium"] * age_factor / total_factor,
            result["premium"] * bmi_factor / total_factor,
            result["premium"] * smoker_factor / total_factor,
            result["premium"] * disease_factor / total_factor
        ]
    })

    pie = px.pie(
        breakdown,
        values="Value",
        names="Component",
        hole=0.70,
        title="Premium Breakdown"
    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )

# ==================================================
# TAB 3 : RISK ASSESSMENT
# ==================================================

with tab3:

    result = st.session_state.result

    col1, col2 = st.columns(2)

    with col1:

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=result["risk_score"],
                title={"text": "Health Risk Score"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "steps": [
                        {"range": [0, 40], "color": "green"},
                        {"range": [40, 70], "color": "orange"},
                        {"range": [70, 100], "color": "red"}
                    ]
                }
            )
        )

        gauge.update_layout(height=320)

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

    with col2:

        radar = go.Figure()

        radar.add_trace(
            go.Scatterpolar(
                r=[
                    age,
                    min(bmi * 2, 100),
                    100 if smoker == "Yes" else 20,
                    100 if existing_disease == "Yes" else 20,
                    children * 15
                ],
                theta=[
                    "Age",
                    "BMI",
                    "Smoking",
                    "Disease",
                    "Dependents"
                ],
                fill="toself"
            )
        )

        radar.update_layout(
            height=320,
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=False
        )

        st.plotly_chart(
            radar,
            use_container_width=True
        )

    if result["risk_category"] == "Low Risk":
        st.success(
            f"Risk Category: {result['risk_category']}"
        )

    elif result["risk_category"] == "Medium Risk":
        st.warning(
            f"Risk Category: {result['risk_category']}"
        )

    else:
        st.error(
            f"Risk Category: {result['risk_category']}"
        )

    st.subheader("🤖 Health Recommendations")

    for rec in result["recommendations"]:
        st.success(rec)

    st.subheader("🛡 Recommended Plan")

    st.info(
        result["recommended_plan"]
    )

    st.subheader("💰 Premium Optimization")

    a, b, c = st.columns(3)

    a.metric(
        "Current Premium",
        f"₹{result['premium']:,}"
    )

    b.metric(
        "Optimized Premium",
        f"₹{result['optimized_premium']:,}"
    )

    c.metric(
        "Potential Savings",
        f"₹{result['savings']:,}"
    )
