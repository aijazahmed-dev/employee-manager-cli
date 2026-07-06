from dataclasses import dataclass
from typing import Optional


@dataclass
class Employee:
    full_name: str
    email: str
    department: str
    position: str
    salary: float
    joining_date: str
    id: Optional[int] = None