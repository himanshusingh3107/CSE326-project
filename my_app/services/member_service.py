from datetime import date
from typing import Any, Dict, List, Optional

from my_app.exceptions import DuplicateResourceException, ResourceNotFoundException
from my_app.models.member import Member
from my_app.models.plan import AVAILABLE_MEMBERSHIP_PLANS
from my_app.repositories.member_repository import MemberRepository
from my_app.schemas.member_schema import MemberCreateSchema, MemberUpdateSchema


class MemberService:
    def __init__(self, repository: MemberRepository) -> None:
        self.repository = repository

    def register_member(self, schema: MemberCreateSchema) -> Member:
        existing_member = self.repository.get_by_phone(schema.phone)
        if existing_member:
            raise DuplicateResourceException("Member", "phone number", schema.phone)

        assigned_trainer = schema.trainer
        if not assigned_trainer and schema.plan == "VIP Pro Plan":
            assigned_trainer = "Senior Coach Vikram"

        new_member = Member(
            id=None,
            name=schema.name.strip(),
            age=schema.age,
            gender=schema.gender,
            phone=schema.phone,
            email=schema.email,
            plan=schema.plan,
            batch=schema.batch,
            trainer=assigned_trainer,
            join_date=date.today().isoformat(),
            status=schema.status,
        )

        return self.repository.create(new_member)

    def list_members(
        self,
        search_query: Optional[str] = None,
        plan_filter: Optional[str] = None,
        fee_status: Optional[str] = None,
    ) -> List[Member]:
        return self.repository.get_all(
            search_query=search_query,
            plan_filter=plan_filter,
            fee_status=fee_status,
        )

    def get_member_by_id(self, member_id: int) -> Member:
        member = self.repository.get_by_id(member_id)
        if not member:
            raise ResourceNotFoundException("Member", member_id)
        return member

    def update_member(self, member_id: int, schema: MemberUpdateSchema) -> Member:
        member = self.get_member_by_id(member_id)

        if schema.phone and schema.phone != member.phone:
            existing_with_phone = self.repository.get_by_phone(schema.phone)
            if existing_with_phone and existing_with_phone.id != member_id:
                raise DuplicateResourceException("Member", "phone number", schema.phone)
            member.phone = schema.phone

        if schema.name is not None:
            member.name = schema.name.strip()
        if schema.age is not None:
            member.age = schema.age
        if schema.gender is not None:
            member.gender = schema.gender
        if schema.plan is not None:
            member.plan = schema.plan
        if schema.batch is not None:
            member.batch = schema.batch
        if schema.email is not None:
            member.email = schema.email
        if schema.trainer is not None:
            member.trainer = schema.trainer
        if schema.status is not None:
            member.status = schema.status

        return self.repository.update(member)

    def update_member_fee_status(self, member_id: int, new_status: str) -> Member:
        self.get_member_by_id(member_id)
        self.repository.update_fee_status(member_id, new_status)
        return self.get_member_by_id(member_id)

    def delete_member(self, member_id: int) -> bool:
        self.get_member_by_id(member_id)
        return self.repository.delete(member_id)

    def get_dashboard_metrics(self) -> Dict[str, Any]:
        stats = self.repository.get_summary_statistics()
        all_members = self.repository.get_all()

        total_collected_inr = 0
        total_pending_inr = 0

        for member in all_members:
            plan_info = AVAILABLE_MEMBERSHIP_PLANS.get(member.plan)
            plan_price = plan_info.monthly_price_inr if plan_info else 0

            if member.status.lower() == "paid":
                total_collected_inr += plan_price
            else:
                total_pending_inr += plan_price

        stats["financials"] = {
            "total_revenue_collected_inr": total_collected_inr,
            "total_revenue_pending_inr": total_pending_inr,
            "currency": "INR",
        }
        return stats
