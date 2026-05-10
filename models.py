from dataclasses import dataclass
from typing import Optional


@dataclass
class Expense:
    id: int
    user_id: int
    amount: int
    drink: str
    coffee_shop: Optional[str]
    created_at: str
