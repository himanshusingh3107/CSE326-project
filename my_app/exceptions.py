from typing import Any, Dict, Optional


class AppException(Exception):
    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_SERVER_ERROR",
        status_code: int = 500,
        payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.payload = payload or {}

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "success": False,
            "error": {
                "code": self.error_code,
                "message": self.message,
            },
        }
        if self.payload:
            result["error"]["details"] = self.payload
        return result


class ResourceNotFoundException(AppException):
    def __init__(self, resource_name: str, identifier: Any) -> None:
        super().__init__(
            message=f"{resource_name} with identifier '{identifier}' was not found.",
            error_code="RESOURCE_NOT_FOUND",
            status_code=404,
        )


class DuplicateResourceException(AppException):
    def __init__(self, resource_name: str, field_name: str, value: Any) -> None:
        super().__init__(
            message=f"{resource_name} with {field_name} '{value}' already exists.",
            error_code="DUPLICATE_RESOURCE",
            status_code=409,
        )


class ValidationException(AppException):
    def __init__(self, message: str, payload: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=422,
            payload=payload,
        )


class DatabaseConnectionException(AppException):
    def __init__(self, message: str = "Failed to establish or execute database transaction.") -> None:
        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            status_code=500,
        )
