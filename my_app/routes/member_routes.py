from typing import Any, Dict, Tuple
from flask import Blueprint, Response, current_app, jsonify, request
from pydantic import ValidationError

from my_app.exceptions import ValidationException
from my_app.schemas.member_schema import (
    FeeStatusUpdateSchema,
    MemberCreateSchema,
    MemberUpdateSchema,
)
from my_app.services.member_service import MemberService

member_api_bp = Blueprint("member_api", __name__, url_prefix="/api/v1/members")


def _get_service() -> MemberService:
    return current_app.extensions["member_service"]


def _format_validation_errors(validation_error: ValidationError) -> Dict[str, Any]:
    return {
        str(".".join(str(location) for location in error.get("loc", [])) or "payload"): str(error.get("msg", "Invalid input"))
        for error in validation_error.errors()
    }


@member_api_bp.route("", methods=["GET"])
def get_all_members() -> Tuple[Response, int]:
    search_query = request.args.get("search")
    plan_filter = request.args.get("plan")
    fee_status = request.args.get("fee_status")

    service = _get_service()
    members = service.list_members(
        search_query=search_query,
        plan_filter=plan_filter,
        fee_status=fee_status,
    )

    return (
        jsonify({
            "success": True,
            "count": len(members),
            "data": [member.to_dict() for member in members],
        }),
        200,
    )


@member_api_bp.route("/<int:member_id>", methods=["GET"])
def get_member_by_id(member_id: int) -> Tuple[Response, int]:
    service = _get_service()
    member = service.get_member_by_id(member_id)

    return jsonify({"success": True, "data": member.to_dict()}), 200


@member_api_bp.route("", methods=["POST"])
def register_member() -> Tuple[Response, int]:
    payload = request.get_json(silent=True)
    if not payload:
        raise ValidationException("Request payload cannot be empty.")

    try:
        validated_schema = MemberCreateSchema(**payload)
    except ValidationError as err:
        raise ValidationException(
            "Member registration failed validation.",
            payload=_format_validation_errors(err),
        )

    service = _get_service()
    created_member = service.register_member(validated_schema)

    return (
        jsonify({
            "success": True,
            "message": f"Member '{created_member.name}' registered successfully.",
            "data": created_member.to_dict(),
        }),
        201,
    )


@member_api_bp.route("/<int:member_id>", methods=["PUT"])
def update_member(member_id: int) -> Tuple[Response, int]:
    payload = request.get_json(silent=True)
    if not payload:
        raise ValidationException("Request payload cannot be empty.")

    try:
        validated_schema = MemberUpdateSchema(**payload)
    except ValidationError as err:
        raise ValidationException(
            "Member update failed validation.",
            payload=_format_validation_errors(err),
        )

    service = _get_service()
    updated_member = service.update_member(member_id, validated_schema)

    return (
        jsonify({
            "success": True,
            "message": "Member details updated successfully.",
            "data": updated_member.to_dict(),
        }),
        200,
    )


@member_api_bp.route("/<int:member_id>/fee-status", methods=["PATCH"])
def update_fee_status(member_id: int) -> Tuple[Response, int]:
    payload = request.get_json(silent=True)
    if not payload:
        raise ValidationException("Request payload cannot be empty.")

    try:
        validated_schema = FeeStatusUpdateSchema(**payload)
    except ValidationError as err:
        raise ValidationException(
            "Fee status update failed validation.",
            payload=_format_validation_errors(err),
        )

    service = _get_service()
    updated_member = service.update_member_fee_status(member_id, validated_schema.status)

    return (
        jsonify({
            "success": True,
            "message": f"Fee status for member '{updated_member.name}' updated to '{updated_member.status}'.",
            "data": updated_member.to_dict(),
        }),
        200,
    )


@member_api_bp.route("/<int:member_id>", methods=["DELETE"])
def delete_member(member_id: int) -> Tuple[Response, int]:
    service = _get_service()
    service.delete_member(member_id)

    return (
        jsonify({
            "success": True,
            "message": f"Member ID {member_id} has been permanently deleted.",
        }),
        200,
    )
