import streamlit as st
import joblib
import numpy as np
import base64

# Function to set background image
def set_bg(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_img = base64.b64encode(img_data).decode()

    bg_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{b64_img}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Title Container */
    .title-container {{
        background-color: rgba(0, 10, 94, 0.8);
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        width: 80%;
        margin: auto;
        box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.2);
    }}

    .title-text {{
        background: -webkit-linear-gradient(45deg, #00E5FF, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 32px;
        font-weight: bold;
    }}
    
    /* Statement Container */
    .statement-container {{
        background-color: rgba(34, 34, 34, 0.8);
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        width: 70%;
        margin: 15px auto;
        box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.2);
    }}

    .statement-text {{
        color: #E0E0E0;
        font-size: 18px;
        font-weight: bold;
    }}


    /* Headings */
    h2, h3, h4, h5, h6 {{
        color: #AEEEEE !important;
        text-align: center;
    }}


    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: #1A237E !important;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.2);
    }}

    /* Input Container */
    .input-container {{
        background-color: rgba(179, 209, 255, 0.9);
        padding: 15px;
        border-radius: 12px;
        margin: 20px auto;
        width: 80%;
        box-shadow: 2px 2px 10px rgba(255, 255, 255, 0.2);
    }}

 .input-container h2 {{
        text-align: center;
        color: #002D72 !important; /* Dark Blue for contrast */
    }}


    /* Input Fields */
    div[data-testid="stTextInput"], div[data-testid="stNumberInput"], 
    div[data-testid="stSelectbox"], div[data-testid="stRadio"] {{
        background-color: #B3D1FF !important;  
        border-radius: 8px !important;
        border: 2px solid #5B9AFF !important;
        padding: 8px !important;
    }}
    
    
    /* Buttons */
    .stButton>button {{
        background: linear-gradient(90deg, #7D3C98, #FFD700);
        color: #FFF !important;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px;
        transition: 0.3s ease-in-out;
    }}

    .stButton>button:hover {{
        background: linear-gradient(90deg, #FFD700, #7D3C98);
        color: #000 !important;
    }}
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)

# Set Background
set_bg("OTP3.jpg")

# Title Section
st.markdown(
    """
    <div class='title-container'>
        <span class='title-text'>✨ AI Diagnosis ATD Scan: Blood & Hormone Health ✨</span>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar Navigation
st.sidebar.header("Navigation")
disease_option = st.sidebar.radio("Select Disease to Predict:", ["Anemia", "Thyroid Disease", "Diabetes"])

# Load Models
anemia_model = joblib.load("anemia_model.joblib")
thyroid_model = joblib.load("thyroid_model.joblib")
diabetes_model = joblib.load("logreg_diabetes.joblib")

# Input Section
st.markdown("<div class='input-container'>", unsafe_allow_html=True)

if disease_option == "Anemia":
    st.subheader("🔴 Anemia Prediction")
    gender = st.selectbox("Select Gender", ["Male", "Female"])
    gender = 0 if gender == "Male" else 1  

    hemoglobin = st.number_input("Hemoglobin Level (g/dL)", min_value=5.0, max_value=20.0, step=0.1, value=13.5, help="Normal: Male 13-17 g/dL, Female 12-15 g/dL.")
    mch = st.number_input("Mean Corpuscular Hemoglobin (pg)", min_value=10.0, max_value=40.0, step=0.1, value=27.0, help="Average hemoglobin per red blood cell.")
    mchc = st.number_input("Mean Corpuscular Hemoglobin Concentration (g/dL)", min_value=20.0, max_value=40.0, step=0.1, value=33.0, help="Concentration of hemoglobin in red blood cells.")
    mcv = st.number_input("Mean Corpuscular Volume (fL)", min_value=50.0, max_value=110.0, step=0.1, value=85.0, help="Normal range: 80-100 fL.")

    if st.button("Predict Anemia"):
        input_data = np.array([[gender, hemoglobin, mch, mchc, mcv]])
        prediction = anemia_model.predict(input_data)[0]
        st.success("✅ Anemia Detected" if prediction == 1 else "❌ No Anemia Detected")

elif disease_option == "Thyroid Disease":
    st.subheader("🦋 Thyroid Disease Prediction")
    age = st.number_input("Age (years)", min_value=1, max_value=100, step=1, value=30, help="Your age in years.")
    gender = st.selectbox("Select Gender", ["Male", "Female"])
    gender = 0 if gender == "Male" else 1  

    on_thyroxine = st.radio("On Thyroxine Medication?", ["No", "Yes"])
    on_thyroxine = 0 if on_thyroxine == "No" else 1

    tsh = st.number_input("Thyroid Stimulating Hormone (mIU/L)", min_value=0.0, max_value=10.0, step=0.1, value=2.5, help="Normal: 0.4-4.0 mIU/L.")
    t3 = st.number_input("Triiodothyronine (T3, ng/dL)", min_value=0.0, max_value=10.0, step=0.1, value=1.2, help="Normal: 0.8-2.0 ng/dL.")
    tt4 = st.number_input("Total Thyroxine (TT4, mcg/dL)", min_value=0.0, max_value=300.0, step=0.1, value=100.0, help="Total thyroid hormone level.")
    t4u = st.number_input("Thyroxine Uptake (T4U)", min_value=0.0, max_value=3.0, step=0.01, value=1.2, help="Normal: 0.7-1.8.")
    fti = st.number_input("Free Thyroxine Index (FTI)", min_value=0.0, max_value=300.0, step=1.0, value=100.0, help="FTI = TT4 * T4U. Normal: 80-150.")

    if st.button("Predict Thyroid Disease"):
        input_data = np.array([[age, gender, on_thyroxine, tsh, t3, tt4, t4u, fti]])
        prediction = thyroid_model.predict(input_data)[0]
        st.success("✅ Thyroid Disease Detected" if prediction == 1 else "❌ No Thyroid Disease Detected")

if disease_option == "Diabetes":
    st.subheader("🩸 Diabetes Prediction")
    pregnancies = st.number_input("Number of Pregnancies", min_value=0, max_value=20, step=1, value=1, help="Total number of times you have been pregnant.")
    glucose = st.number_input("Glucose Level (mg/dL)", min_value=50, max_value=300, step=1, value=100, help="Blood sugar level after fasting. Normal: 70-100 mg/dL.")
    blood_pressure = st.number_input("Blood Pressure (mmHg)", min_value=40, max_value=200, step=1, value=80, help="Normal: 90-120 mmHg.")
    skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0, max_value=100, step=1, value=20, help="Thickness of skin fold, related to body fat.")
    insulin = st.number_input("Insulin Level (μU/mL)", min_value=0, max_value=1000, step=1, value=80, help="Normal range: 16-166 μU/mL.")
    bmi = st.number_input("Body Mass Index (BMI)", min_value=10.0, max_value=50.0, step=0.1, value=25.0, help="Normal: 18.5-24.9.")
    dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=2.5, step=0.01, value=0.5, help="Diabetes risk based on family history.")
    age = st.number_input("Age (years)", min_value=1, max_value=100, step=1, value=30, help="Your current age in years.")

    if st.button("Predict Diabetes"):
        input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]])
        prediction = diabetes_model.predict(input_data)[0]
        st.success("✅ Diabetes Detected" if prediction == 1 else "❌ No Diabetes Detected")

st.markdown("</div>", unsafe_allow_html=True)