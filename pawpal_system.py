"""
Logic layer and backend classes
"""

from dataclasses import dataclass, field

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    name: str
    duration: int
    priority: str
    category: str
    recurrence: str
    completed: bool = False

    def is_due_today(self) -> bool:
        """Return whether this task still needs to happen today."""
        if self.completed and self.recurrence == "once":
            return False
        return True

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's task list."""
        self.tasks.remove(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's tasks."""
        return self.tasks


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's list of pets."""
        self.pets.remove(pet)

    def get_pets(self) -> list[Pet]:
        """Return this owner's pets."""
        return self.pets

    def get_all_tasks(self) -> list[Task]:
        """Return the combined task list across all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def get_tasks_for_owner(self, owner: Owner) -> list[Task]:
        """Return all of the owner's tasks that are still due today."""
        return [task for task in owner.get_all_tasks() if task.is_due_today()]

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered from highest to lowest priority."""
        return sorted(tasks, key=lambda task: PRIORITY_ORDER.get(task.priority, len(PRIORITY_ORDER)))

    def filter_by_time(self, tasks: list[Task], available_minutes: int) -> list[Task]:
        """Greedily select tasks, in order, that fit within the available minutes."""
        scheduled = []
        remaining_minutes = available_minutes
        for task in tasks:
            if task.duration <= remaining_minutes:
                scheduled.append(task)
                remaining_minutes -= task.duration
        return scheduled

    def generate_plan(self, tasks: list[Task], available_minutes: int) -> list[Task]:
        """Build a schedule by prioritizing then filtering the given tasks to fit the available time."""
        prioritized = self.sort_by_priority(tasks)
        return self.filter_by_time(prioritized, available_minutes)

    def generate_plan_for_owner(self, owner: Owner) -> list[Task]:
        """Build today's schedule for an owner from all of their pets' due tasks."""
        due_tasks = self.get_tasks_for_owner(owner)
        return self.generate_plan(due_tasks, owner.available_minutes)

    def explain(self, task: Task) -> str:
        """Return a human-readable explanation for why a task was scheduled."""
        return f"{task.name} ({task.priority} priority, {task.duration} min) scheduled for {task.category}."
