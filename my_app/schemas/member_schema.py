import re
from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator


class MemberCreateSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    phone: str = Field(..., description="10-digit primary mobile number")
    age: int = Field(..., ge=15, le=70)
    gender: Literal["Male", "Female", "Other"]
    plan: Literal["Basic Plan", "Standard Plan", "VIP Pro Plan"]
    batch: Literal[
        "Morning (06:00 AM - 08:00 AM)",
        "Evening (05:00 PM - 07:00 PM)",
        "Night (07:30 PM - 09:30 PM)",
    ]
    email: Optional[str] = Field(default=None, max_length=120)
    trainer: Optional[str] = Field(default=None, max_length=60)
    status: Literal["Paid", "Pending"] = Field(default="Pending")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, phone_value: str) -> str:
        clean_digits = re.sub(r"\D", "", phone_value)
        if len(clean_digits) != 10:
            raise ValueError("Phone number must contain exactly 10 numeric digits.")
        return clean_digits

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, email_value: Optional[str]) -> Optional[str]:
        if email_value is None or not email_value.strip():
            return None
        trimmed_email = email_value.strip().lower()
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, trimmed_email):
            raise ValueError("Invalid email address format.")
        return trimmed_email


class MemberUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=100)
    phone: Optional[str] = None
    age: Optional[int] = Field(default=None, ge=15, le=70)
    gender: Optional[Literal["Male", "Female", "Other"]] = None
    plan: Optional[Literal["Basic Plan", "Standard Plan", "VIP Pro Plan"]] = None
    batch: Optional[
        Literal[
            "Morning (06:00 AM - 08:00 AM)",
            "Evening (05:00 PM - 07:00 PM)",
            "Night (07:30 PM - 09:30 PM)",
        ]
    ] = None
    email: Optional[str] = None
    trainer: Optional[str] = None
    status: Optional[Literal["Paid", "Pending"]] = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, phone_value: Optional[str]) -> Optional[str]:
        if phone_value is None:
            return None
        clean_digits = re.sub(r"\D", "", phone_value)
        if len(clean_digits) != 10:
            raise ValueError("Phone number must contain exactly 10 numeric digits.")
        return clean_digits


class FeeStatusUpdateSchema(BaseModel):
    status: Literal["Paid", "Pending"]
