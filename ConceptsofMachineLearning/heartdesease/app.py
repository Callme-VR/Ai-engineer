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
    # Create a DataFrame with the user input (using proper column names)
    user_input = pd.DataFrame({
        'Age': [age],
        'Sex': [sex],
        'ChestPainType': [chest_pain],
        'RestingBP': [resting_bp],
        'Cholesterol': [cholesterol],
        'FastingBS': [fasting_bs],
        'RestingECG': [resting_ecg],
        'MaxHR': [max_hr],
        'ExerciseAngina': [exercise_angina],
        'Oldpeak': [oldpeak],
        'ST_Slope': [st_slope]
    })

    # One-hot encode categorical variables
    user_input = pd.get_dummies(user_input, columns=[
                                'Sex', 'ChestPainType', 'RestingECG', 'ExerciseAngina', 'ST_Slope'])

    # Ensure all expected columns are present (add missing columns with 0)
    for col in expected_columns:
        if col not in user_input.columns:
            user_input[col] = 0

    # Reorder columns to match the expected order
    user_input = user_input[expected_columns]

    # Scale the input
    user_input = scaler.transform(user_input)

    # Make prediction
    prediction = model.predict(user_input)

    # Display the prediction
    if prediction[0] == 1:
        st.write(
            "⚠️ Based on the provided details, you are at risk of having heart disease.")
    else:
        st.write(
            "✅ Based on the provided details, you are not at risk of having heart disease.")
