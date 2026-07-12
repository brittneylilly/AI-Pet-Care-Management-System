"""
Logic layer and backend classes
"""

from dataclasses import dataclass, field
from datetime import date, timedelta

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
RECURRENCE_INTERVAL_DAYS = {"once": None, "daily": 1, "weekly": 7}


@dataclass
class Task:
    name: str
    duration: int
    priority: str
    category: str
    recurrence: str
    completed: bool = False
    due_date: date | None = None
    scheduled_time: str | None = None  # "HH:MM", e.g. "08:00"

    def is_due_today(self, today: date | None = None) -> bool:
        """Return whether this task still needs to happen today."""
        today = today or date.today()
        if self.completed:
            return False
        if self.due_date is None:
            return True
        return self.due_date <= today

    def mark_complete(self, today: date | None = None) -> "Task | None":
        """Mark this task complete and return its next occurrence, if it recurs."""
        today = today or date.today()
        self.completed = True
        self.due_date = today
        return self._next_occurrence(today)

    def _next_occurrence(self, completed_date: date) -> "Task | None":
        """Build the next occurrence of this task, computed with timedelta, or None if it doesn't recur."""
        interval_days = RECURRENCE_INTERVAL_DAYS.get(self.recurrence)
        if interval_days is None:
            return None
        return Task(
            name=self.name,
            duration=self.duration,
            priority=self.priority,
            category=self.category,
            recurrence=self.recurrence,
            completed=False,
            due_date=completed_date + timedelta(days=interval_days),
            scheduled_time=self.scheduled_time,
        )


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

    def mark_task_complete(self, task: Task, today: date | None = None) -> None:
        """Complete a task and automatically add its next occurrence if it recurs."""
        next_task = task.mark_complete(today=today)
        if next_task is not None:
            self.add_task(next_task)


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

    def get_tasks_for_pet(self, pet: Pet) -> list[Task]:
        """Return just one pet's tasks that are still due today."""
        return [task for task in pet.get_tasks() if task.is_due_today()]

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered by priority, then by duration (shortest first) to fit more tasks per tier."""
        return sorted(
            tasks,
            key=lambda task: (PRIORITY_ORDER.get(task.priority, len(PRIORITY_ORDER)), task.duration),
        )

    def sort_by_duration(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered from shortest to longest, ignoring priority."""
        return sorted(tasks, key=lambda task: task.duration)

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered by scheduled_time ("HH:MM"), earliest first. Untimed tasks sort last."""
        return sorted(tasks, key=lambda task: (task.scheduled_time is None, self._start_minutes(task)))

    def _start_minutes(self, task: Task) -> int:
        """Convert a task's scheduled_time ("HH:MM") to minutes since midnight. Untimed tasks sort as 0."""
        if task.scheduled_time is None:
            return 0
        hours, minutes = task.scheduled_time.split(":")
        return int(hours) * 60 + int(minutes)

    def filter_by_status(self, tasks: list[Task], completed: bool) -> list[Task]:
        """Return tasks matching the given completion status."""
        return [task for task in tasks if task.completed == completed]

    def filter_by_pet_name(self, owner: Owner, pet_name: str) -> list[Task]:
        """Return all tasks belonging to the pet with the given name."""
        for pet in owner.get_pets():
            if pet.name == pet_name:
                return pet.get_tasks()
        return []

    def filter_by_time(self, tasks: list[Task], available_minutes: int) -> tuple[list[Task], list[Task]]:
        """Greedily select tasks, in order, that fit within the available minutes.

        Returns (scheduled, skipped) so the owner can see what didn't make the cut.
        """
        scheduled = []
        skipped = []
        remaining_minutes = available_minutes
        for task in tasks:
            if task.duration <= remaining_minutes:
                scheduled.append(task)
                remaining_minutes -= task.duration
            else:
                skipped.append(task)
        return scheduled, skipped

    def find_duplicate_tasks(self, tasks: list[Task]) -> list[Task]:
        """Return tasks that share the same name and category as an earlier task in the list."""
        seen = set()
        duplicates = []
        for task in tasks:
            key = (task.name, task.category)
            if key in seen:
                duplicates.append(task)
            else:
                seen.add(key)
        return duplicates

    def find_time_conflicts(self, tasks: list[Task]) -> list[str]:
        """Return warnings for tasks whose scheduled_time windows overlap, across any pets.

        Lightweight sort-and-sweep: sort by start time, then only compare each
        task to the very next one, since an overlap must involve neighbors once sorted.
        Untimed tasks are ignored rather than raising an error.
        """
        timed_tasks = self.sort_by_time([task for task in tasks if task.scheduled_time])

        conflicts = []
        for earlier, later in zip(timed_tasks, timed_tasks[1:]):
            earlier_end = self._start_minutes(earlier) + earlier.duration
            if self._start_minutes(later) < earlier_end:
                conflicts.append(
                    f"Time conflict: '{earlier.name}' ({earlier.scheduled_time}, {earlier.duration} min) "
                    f"overlaps with '{later.name}' ({later.scheduled_time}, {later.duration} min)"
                )
        return conflicts

    def find_overloaded_priority(self, tasks: list[Task], available_minutes: int) -> str | None:
        """Return a warning if high-priority tasks alone exceed the available time."""
        high_priority_minutes = sum(task.duration for task in tasks if task.priority == "high")
        if high_priority_minutes > available_minutes:
            return (
                f"High-priority tasks need {high_priority_minutes} min, "
                f"but only {available_minutes} min are available."
            )
        return None

    def detect_conflicts(self, tasks: list[Task], available_minutes: int) -> list[str]:
        """Return human-readable warnings about duplicates, time overlaps, or an unmeetable schedule.

        Only tasks still due today are considered — completed history and its
        auto-scheduled next occurrence would otherwise look like false duplicates.
        """
        due_today = [task for task in tasks if task.is_due_today()]

        conflicts = [f"Duplicate task: '{task.name}' ({task.category})" for task in self.find_duplicate_tasks(due_today)]
        conflicts.extend(self.find_time_conflicts(due_today))

        overload_warning = self.find_overloaded_priority(due_today, available_minutes)
        if overload_warning:
            conflicts.append(overload_warning)

        return conflicts

    def generate_plan(self, tasks: list[Task], available_minutes: int) -> tuple[list[Task], list[Task]]:
        """Build a schedule by prioritizing then filtering the given tasks to fit the available time."""
        prioritized = self.sort_by_priority(tasks)
        return self.filter_by_time(prioritized, available_minutes)

    def generate_plan_for_owner(self, owner: Owner) -> tuple[list[Task], list[Task]]:
        """Build today's schedule for an owner from all of their pets' due tasks."""
        due_tasks = self.get_tasks_for_owner(owner)
        return self.generate_plan(due_tasks, owner.available_minutes)

    def explain(self, task: Task) -> str:
        """Return a human-readable explanation for why a task was scheduled."""
        return f"{task.name} ({task.priority} priority, {task.duration} min) scheduled for {task.category}."
