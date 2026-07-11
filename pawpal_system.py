"""
Logic layer and backend classes
"""

from dataclasses import dataclass, field


@dataclass
class Task:
    name: str
    duration: int
    priority: str
    category: str
    recurrence: str

    def is_due_today(self) -> bool:
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass

    def get_pets(self) -> list[Pet]:
        pass


class Planner:
    def generate_plan(self, tasks: list[Task], available_minutes: int) -> list[Task]:
        pass

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        pass

    def filter_by_time(self, tasks: list[Task], available_minutes: int) -> list[Task]:
        pass

    def explain(self, task: Task) -> str:
        pass
