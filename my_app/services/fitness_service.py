from typing import Dict, List, Tuple
from my_app.schemas.fitness_schema import BMICalculationInputSchema, BMIResultSchema


class FitnessService:
    @staticmethod
    def calculate_bmi(input_data: BMICalculationInputSchema) -> BMIResultSchema:
        height_in_meters = input_data.height_cm / 100.0
        calculated_bmi = round(input_data.weight_kg / (height_in_meters ** 2), 1)

        category, risk_level, workout_advice, dietary_advice, action_items = (
            FitnessService._evaluate_bmi_category(calculated_bmi)
        )

        min_healthy_weight = round(18.5 * (height_in_meters ** 2), 1)
        max_healthy_weight = round(24.9 * (height_in_meters ** 2), 1)

        return BMIResultSchema(
            bmi_score=calculated_bmi,
            category=category,
            risk_level=risk_level,
            target_healthy_weight_min_kg=min_healthy_weight,
            target_healthy_weight_max_kg=max_healthy_weight,
            workout_advice=workout_advice,
            dietary_advice=dietary_advice,
            action_items=action_items,
        )

    @staticmethod
    def _evaluate_bmi_category(
        bmi_score: float,
    ) -> Tuple[str, str, str, str, List[str]]:
        if bmi_score < 18.5:
            return (
                "Underweight",
                "Increased risk of nutritional deficiency",
                "Focus on progressive hypertrophy training and compound strength exercises (squats, bench press, deadlifts). Avoid excessive cardio.",
                "High-protein caloric surplus diet with complex carbohydrates and healthy fats.",
                [
                    "Train 4 days/week focusing on compound movements",
                    "Target 1.6g to 2.0g protein per kg of body weight",
                    "Maintain a daily caloric surplus of 300-500 kcal",
                ],
            )
        elif 18.5 <= bmi_score <= 24.9:
            return (
                "Normal",
                "Lowest risk profile",
                "Maintain athletic conditioning with balanced 5-day push/pull/legs split and moderate cardio.",
                "Iso-caloric maintenance diet with balanced macros (40% carbs, 30% protein, 30% healthy fats).",
                [
                    "Engage in 150 minutes of moderate activity weekly",
                    "Incorporate progressive overload in resistance workouts",
                    "Stay hydrated and maintain consistent sleep hygiene",
                ],
            )
        elif 25.0 <= bmi_score <= 29.9:
            return (
                "Overweight",
                "Mildly elevated cardiovascular risk",
                "Incorporate High-Intensity Interval Training (HIIT) paired with resistance training to preserve lean mass while mobilizing fat stores.",
                "Caloric deficit of 400-600 kcal/day, focusing on high-satiety fibrous vegetables and lean proteins.",
                [
                    "Add 20-30 minutes of Zone 2 cardio post-lift",
                    "Eliminate refined sugars and sugary beverages",
                    "Track daily caloric intake using a fitness tracker",
                ],
            )
        else:
            return (
                "Obese",
                "Elevated metabolic and cardiovascular risk",
                "Low-impact resistance training (machines, cable systems) and steady-state cycling/incline walking to minimize joint compression.",
                "Structured medically-guided hypocaloric nutrition plan prioritizing lean protein and zero liquid calories.",
                [
                    "Consult gym medical officer before max-effort lifting",
                    "Perform low-impact aerobic activity daily",
                    "Gradually build stamina with 30-minute supervised sessions",
                ],
            )
