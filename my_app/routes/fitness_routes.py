from typing import Any, Dict, Tuple
from flask import Blueprint, Response, jsonify, request
from pydantic import ValidationError

from my_app.exceptions import ValidationException
from my_app.schemas.fitness_schema import BMICalculationInputSchema
from my_app.services.fitness_service import FitnessService

fitness_api_bp = Blueprint("fitness_api", __name__, url_prefix="/api/v1/fitness")


def _format_validation_errors(validation_error: ValidationError) -> Dict[str, Any]:
    return {
        str(".".join(str(location) for location in error.get("loc", [])) or "field"): str(error.get("msg", "Invalid value"))
        for error in validation_error.errors()
    }


@fitness_api_bp.route("/bmi", methods=["POST"])
def calculate_bmi_endpoint() -> Tuple[Response, int]:
    payload = request.get_json(silent=True)
    if not payload:
        raise ValidationException("Body payload required with height_cm and weight_kg.")

    try:
        validated_input = BMICalculationInputSchema(**payload)
    except ValidationError as err:
        raise ValidationException(
            "BMI inputs failed validation.",
            payload=_format_validation_errors(err),
        )

    result = FitnessService.calculate_bmi(validated_input)

    return (
        jsonify({
            "success": True,
            "data": result.model_dump(),
        }),
        200,
    )
