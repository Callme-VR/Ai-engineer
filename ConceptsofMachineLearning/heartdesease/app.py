import streamlit as st
import pandas as pd
import joblib

model = joblib.load('Logistic_heart.pkl')
scaler = joblib.load('scaler_heart.pkl')
expected_columns = joblib.load('columns_heart.pkl')


# for the title of the model page and let says app which is used for the heaert desases predictions


st.title('Heart Disease Prediction App 💖')
st.markdown('Provide the Following details to predict the heart disease')


# Collect user input
age = st.slider("Age", 18, 100, 40)
sex = st.selectbox("Sex", ["M", "F"])
chest_pain = st.selectbox("Chest Pain Type", ["ATA", "NAP", "TA", "ASY"])
resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", 80, 200, 120)
cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, 200)
fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", [0, 1])
resting_ecg = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"])
max_hr = st.slider("Max Heart Rate", 60, 220, 150)
exercise_angina = st.selectbox("Exercise-Induced Angina", ["Y", "N"])
oldpeak = st.slider("Oldpeak (ST Depression)", 0.0, 6.0, 1.0)
st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])


# When Predict is clicked
if st.button("Predict"):
