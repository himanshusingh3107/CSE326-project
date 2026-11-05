from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class MembershipPlan:
    code: str
    name: str
    monthly_price_inr: int
    features: List[str]
    includes_trainer: bool
    is_popular: bool = False


AVAILABLE_MEMBERSHIP_PLANS = {
    "Basic Plan": MembershipPlan(
        code="BASIC",
        name="Basic Plan",
        monthly_price_inr=999,
        features=[
            "General Fitness Area",
            "Locker & Changing Room",
            "Cardio Equipment",
        ],
        includes_trainer=False,
    ),
    "Standard Plan": MembershipPlan(
        code="STANDARD",
        name="Standard Plan",
        monthly_price_inr=1799,
        features=[
            "Full Gym Access (All Equipment)",
            "Locker & Shower Facility",
            "Cardio & CrossFit Arena",
            "General Trainer Assistance",
        ],
        includes_trainer=False,
        is_popular=True,
    ),
    "VIP Pro Plan": MembershipPlan(
        code="VIP_PRO",
        name="VIP Pro Plan",
        monthly_price_inr=2999,
        features=[
            "24/7 Unlimited Gym Access",
            "Dedicated Personal Trainer",
            "Personalized Diet Chart",
            "Steam & Sauna Access",
            "Free Gym Shaker & T-Shirt",
        ],
        includes_trainer=True,
    ),
}
