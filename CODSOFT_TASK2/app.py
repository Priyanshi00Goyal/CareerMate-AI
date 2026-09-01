# ============================================================
# CODSOFT TASK 2
# CREDIT CARD FRAUD DETECTION
# Streamlit Application
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="💳",
    layout="wide"
)

# ------------------------------------------------------------
# Load Model
# ------------------------------------------------------------

@st.cache_resource
def load_model():

    base_dir = Path(__file__).resolve().parent

    model_path = (
        base_dir
        / "models"
        / "fraud_detection_model.pkl"
    )

    return joblib.load(model_path)

model = load_model()

# ------------------------------------------------------------
# Application Header
# ------------------------------------------------------------

st.title("💳 Credit Card Fraud Detection")

st.markdown("""
### Machine Learning Fraud Detection System

Enter transaction details below to estimate whether the transaction is
**legitimate** or potentially **fraudulent**.
""")

st.divider()

# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------

st.sidebar.title("About the Project")

st.sidebar.info("""
This project was developed as part of the
**CodSoft Machine Learning Internship**.

Models experimented with:

• Logistic Regression
• Decision Tree
• Random Forest

The final model was selected using
classification performance metrics.
""")

# ------------------------------------------------------------
# Transaction Information
# ------------------------------------------------------------

st.subheader("Transaction Information")

col1, col2 = st.columns(2)

with col1:

    amount = st.number_input(
        "Transaction Amount ($)",
        min_value=0.0,
        value=100.0,
        step=1.0
    )

    category = st.selectbox(
        "Transaction Category",
        [
            "grocery_pos",
            "shopping_pos",
            "entertainment",
            "gas_transport",
            "misc_pos",
            "shopping_net",
            "food_dining",
            "personal_care",
            "health_fitness",
            "home",
            "kids_pets",
            "travel",
            "misc_net"
        ]
    )

    gender = st.selectbox(
        "Gender",
        ["M", "F"]
    )

with col2:

    transaction_hour = st.slider(
        "Transaction Hour",
        min_value=0,
        max_value=23,
        value=12
    )

    transaction_day = st.slider(
        "Transaction Day",
        min_value=1,
        max_value=31,
        value=15
    )

    transaction_month = st.slider(
        "Transaction Month",
        min_value=1,
        max_value=12,
        value=6
    )

# ------------------------------------------------------------
# Location Information
# ------------------------------------------------------------

st.subheader("Location Information")

col1, col2, col3, col4 = st.columns(4)

with col1:
    latitude = st.number_input(
        "Customer Latitude",
        value=40.0
    )

with col2:
    longitude = st.number_input(
        "Customer Longitude",
        value=-75.0
    )

with col3:
    merchant_latitude = st.number_input(
        "Merchant Latitude",
        value=40.0
    )

with col4:
    merchant_longitude = st.number_input(
        "Merchant Longitude",
        value=-75.0
    )

# ------------------------------------------------------------
# Customer Information
# ------------------------------------------------------------

st.subheader("Customer Information")

col1, col2 = st.columns(2)

with col1:

    customer_age = st.number_input(
        "Customer Age",
        min_value=18.0,
        max_value=100.0,
        value=30.0
    )

with col2:

    merchant = st.text_input(
        "Merchant",
        value="merchant_example"
    )

# ------------------------------------------------------------
# Distance Calculation
# ------------------------------------------------------------

def haversine_distance(lat1, lon1, lat2, lon2):

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1)
        * np.cos(lat2)
        * np.sin(dlon / 2) ** 2
    )

    c = 2 * np.arcsin(np.sqrt(a))

    return 6371 * c

distance_km = haversine_distance(
    latitude,
    longitude,
    merchant_latitude,
    merchant_longitude
)

# ------------------------------------------------------------
# Derived Features
# ------------------------------------------------------------

transaction_dayofweek = 0

is_night = int(
    transaction_hour < 6
    or transaction_hour >= 22
)

log_amt = np.log1p(amount)

# ------------------------------------------------------------
# Prediction
# ------------------------------------------------------------

if st.button(
    "🔍 Check Transaction",
    use_container_width=True
):

    input_data = pd.DataFrame({
        "merchant": [merchant],
        "category": [category],
        "gender": [gender],
        "amt": [amount],
        "lat": [latitude],
        "long": [longitude],
        "merch_lat": [merchant_latitude],
        "merch_long": [merchant_longitude],
        "transaction_hour": [transaction_hour],
        "transaction_day": [transaction_day],
        "transaction_month": [transaction_month],
        "transaction_dayofweek": [transaction_dayofweek],
        "customer_age": [customer_age],
        "distance_km": [distance_km],
        "is_night": [is_night],
        "log_amt": [log_amt]
    })

    prediction = model.predict(input_data)[0]

    probability = None

    if hasattr(model, "predict_proba"):
        probability = model.predict_proba(
            input_data
        )[0][1]

    st.divider()

    if probability is not None:

        fraud_percentage = probability * 100

        if fraud_percentage >= 70:

            risk_level = "HIGH"
            st.error("🚨 High Fraud Risk")

        elif fraud_percentage >= 30:

            risk_level = "MEDIUM"
            st.warning("⚠️ Medium Fraud Risk")

        else:

            risk_level = "LOW"
            st.success("✅ Low Fraud Risk")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Fraud Probability",
                f"{fraud_percentage:.2f}%"
            )

        with col2:
            st.metric(
                "Risk Level",
                risk_level
            )

        st.progress(
            min(probability, 1.0),
            text=f"Fraud Risk: {fraud_percentage:.2f}%"
        )

    else:

        if prediction == 1:

            st.error(
                "🚨 Potential Fraudulent Transaction"
            )

        else:

            st.success(
                "✅ Transaction Classified as Legitimate"
            )

    st.info(
        f"📍 Customer-to-Merchant Distance: "
        f"{distance_km:.2f} km"
    )

# ------------------------------------------------------------
# Transaction Summary
# ------------------------------------------------------------

with st.expander("View Transaction Details"):

    st.write(
        {
            "Transaction Amount": amount,
            "Category": category,
            "Gender": gender,
            "Transaction Hour": transaction_hour,
            "Customer Age": customer_age,
            "Distance (km)": round(distance_km, 2),
            "Night Transaction": bool(is_night)
        }
    )

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------

st.divider()

st.caption(
    "Credit Card Fraud Detection | CodSoft ML Internship"
)