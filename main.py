from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, computed_field, Field
from typing import List, Dict, Literal, Annotated
import pickle
import pandas as pd
import numpy as np


with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()


tier_1 = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Bhagyanagar", "Pune"]
tier_2 = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Prayagraj"
]

# Pydantic model to validate incoming data
class User_input(BaseModel):
    age: Annotated[int, Field(...,gt=0, lt=120, description="age of the user")]
    weight: Annotated[float, Field(...,gt=0, description="weight of the user")]
    height: Annotated[float, Field(...,gt=0, lt=2.5, description="height of the user")]
    income_lpa: Annotated[float, Field(...,gt=0, description="income_lpa of the user")]
    smoker: Annotated[bool, Field(..., description="is user a smoker")]
    city: Annotated[str, Field(..., description="the city user belongs to")]
    occupation: Annotated[Literal["Software Engineer", "Teacher", "Doctor", "Farmer", "Electrician", "Nurse", "Civil Engineer",
    "Shopkeeper", "Student", "Driver", "Banker", "Chef", "Graphic Designer", "Mechanical Engineer",
    "Lawyer", "Artist", "Clerk", "Police Officer", "Architect", "Scientist", "Pharmacist",
    "Receptionist", "Construction Worker", "Data Analyst", "Content Writer", "Marketing Executive"
    ], Field(..., description="occupation of the user")]

    @computed_field
    @property
    def BMI(self) -> float:
        return self.weight/(self.height**2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.BMI > 30:
            return "high"
        elif self.smoker or self.BMI > 27:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        else:
            return "senior"


    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1:
            return 1
        elif self.city in tier_2:
            return 2
        else:
            return 3

@app.post("/predict")
def predict_premium(data: User_input):

    input_df = pd.DataFrame([{
        "BMI": data.BMI,
        "age_group": data.age_group,
        "city_tier": data.city_tier,
        "lifestyle_risk": data.lifestyle_risk,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation,
    }])

    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={"Predicted_Category": prediction})
