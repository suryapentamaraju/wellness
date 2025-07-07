import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Workplace Wellness Risk Monitor", layout="wide")
st.title("🏥 Workplace Wellness Risk Monitor")

# --- Risk Assessment Logic ---
def assess_risk(row):
    score = 0
    reasons = []

    if row['heart_rate'] > 90:
        score += 1
        reasons.append("High HR")
    if row['stress'] > 7:
        score += 1
        reasons.append("High Stress")
    if row['sleep_hours'] < 5:
        score += 1
        reasons.append("Poor Sleep")

    if score == 0:
        return "Low", "-"
    elif score == 1:
        return "Moderate", reasons[0]
    else:
        return "High", ", ".join(reasons)

def suggest_intervention(risk_level):
    return {
        "Low": "✅ Keep up the good work!",
        "Moderate": "🧘 Try meditation or short breaks.",
        "High": "🚨 Consult wellness coach, prioritize rest, reduce stress.",
    }[risk_level]

# --- Upload Section ---
uploaded_file = st.file_uploader("📂 Upload CSV file with health data", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if set(['id', 'heart_rate', 'stress', 'sleep_hours']).issubset(df.columns):
        df[['risk_level', 'risk_reason']] = df.apply(assess_risk, axis=1, result_type="expand")
        df['intervention'] = df['risk_level'].apply(suggest_intervention)

        # --- Show Table ---
        st.subheader("📊 Risk Analysis Table")
        st.dataframe(df[['id', 'heart_rate', 'stress', 'sleep_hours', 'risk_level', 'risk_reason', 'intervention']], use_container_width=True)

        # --- Plot ---
        st.subheader("📈 Stress vs Heart Rate Risk Plot")
        colors = {"Low": "green", "Moderate": "orange", "High": "red"}
        df['color'] = df['risk_level'].map(colors)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(df['stress'], df['heart_rate'], s=80, c=df['color'])
        for _, row in df.iterrows():
            ax.text(row['stress'] + 0.1, row['heart_rate'] + 0.1, row['id'], fontsize=8)
        ax.set_xlabel("Stress Level")
        ax.set_ylabel("Heart Rate")
        ax.set_title("Employee Risk Clustering")
        ax.grid(True)
        st.pyplot(fig)

        # --- Download Results ---
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Download Risk Report as CSV", csv, "risk_report.csv", "text/csv")
    else:
        st.error("❌ CSV must contain: id, heart_rate, stress, sleep_hours")
else:
    st.info("Upload a CSV to begin.")