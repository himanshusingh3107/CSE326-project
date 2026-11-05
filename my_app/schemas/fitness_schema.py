from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class BMICalculationInputSchema(BaseModel):
    height_cm: float = Field(..., ge=50.0, le=250.0, description="Height in centimeters")
    weight_kg: float = Field(..., ge=20.0, le=300.0, description="Weight in kilograms")
    age: Optional[int] = Field(default=None, ge=10, le=100)
    gender: Optional[str] = None


class BMIResultSchema(BaseModel):
    bmi_score: float
    category: str
    risk_level: str
    target_healthy_weight_min_kg: float
    target_healthy_weight_max_kg: float
    workout_advice: str
    dietary_advice: str
    action_items: List[str]
