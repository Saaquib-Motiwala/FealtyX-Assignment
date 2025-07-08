from typing import Dict
from dataclasses import dataclass
from datetime import datetime

students_data: Dict[int, Dict] = {}
next_id = 1


@dataclass
class Student:
    id: int
    name: str
    age: int
    email: str
    created_at: str = None
    updated_at: str = None

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = datetime.now().isoformat()


def get_next_id() -> int:
    global next_id
    current_id = next_id
    next_id += 1
    return current_id
