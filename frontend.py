import streamlit as st
import requests
import base64

API_URL = "http://localhost:8000/predict"

st.set_page_config(page_title="Insurance Premium Predictor", layout="centered")

def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

image_path = "Insurance.png"
image_base64 = get_base64(image_path)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{image_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Insurance Premium Category Predictor")
st.markdown("Enter your personal details here...")

age = st.number_input("Age",min_value=1,max_value=119,value=20)
height = st.number_input("Height (m)",min_value=0.5,max_value=3.0,value=1.65)
weight = st.number_input("Weight (kg)",min_value=10,value=60)
income_lpa = st.number_input("Income (LPA)",min_value=0.1,value=10.0)
smoker = st.selectbox("Are you a smoker?",options=["True","False"])
city = st.text_input("City",value="Mumbai")
occupation = st.selectbox("ocuupation", options=["Software Engineer", "Doctor", "Farmer", "Electrician", "Nurse", "Civil Engineer", "Shopkeeper", "Student", "Driver", "Banker", "Chef", "Graphic Designer", "Mechanical Engineer", "Lawyer", "Artist", "Clerk", "Police Officer", "Architect", "Scientist", "Pharmacist", "Receptionist", "Construction Worker", "Data Analyst", "Content Writer", "Marketing Executive"])

if st.button("Predict Preium Category"):
    input_data = {"age":age,"height":height,"weight":weight,"income_lpa":income_lpa,"smoker":smoker,"city":city,"occupation":occupation}

    try:
        Response = requests.post(url=API_URL,json=input_data)
        if Response.status_code == 200:
            result = Response.json()
            st.success(f"Premium Predicted Category: **{result["Predicted_Category"]}**")
        else:
            st.error(f"API error: {Response.status_code} - {Response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Couldn't connect to the API server. Make sure it's running on port 8000.")

st.markdown(
    """
    <style>
    .made-in-bharat {
        position: fixed;
        left: 10px;
        bottom: 10px;
        font-size: 14px;
        color: #888888;
        z-index: 9999;
    }
    </style>
    <div class="made-in-bharat">Made in Bharat 🇮🇳</div>
    """,
    unsafe_allow_html=True
)
