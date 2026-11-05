from dataclasses import dataclass, asdict
from datetime import date
from typing import Any, Dict, Optional


@dataclass
class Member:
    id: Optional[int]
    name: str
    age: int
    gender: str
    phone: str
    email: Optional[str]
    plan: str
    batch: str
    trainer: Optional[str]
    join_date: str
    status: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data_dict: Dict[str, Any]) -> "Member":
        mobile_value = data_dict.get("phone") or data_dict.get("mobile", "")
        fee_status_value = data_dict.get("status") or data_dict.get("feeStatus", "Pending")
        join_date_value = data_dict.get("join_date") or date.today().isoformat()

        return cls(
            id=data_dict.get("id"),
            name=str(data_dict.get("name", "")).strip(),
            age=int(data_dict.get("age", 0)),
            gender=str(data_dict.get("gender", "")).strip(),
            phone=str(mobile_value).strip(),
            email=str(data_dict.get("email")).strip() if data_dict.get("email") else None,
            plan=str(data_dict.get("plan", "")).strip(),
            batch=str(data_dict.get("batch", "")).strip(),
            trainer=str(data_dict.get("trainer")).strip() if data_dict.get("trainer") else None,
            join_date=str(join_date_value),
            status=str(fee_status_value).strip(),
        )

