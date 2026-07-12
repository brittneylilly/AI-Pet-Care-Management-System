from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_status():
    task = Task(name="Feeding", duration=10, priority="high", category="feeding", recurrence="daily")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age=3)
    assert len(pet.get_tasks()) == 0

    task = Task(name="Morning walk", duration=30, priority="high", category="walk", recurrence="daily")
    pet.add_task(task)

    assert len(pet.get_tasks()) == 1


def test_generate_plan_prioritizes_and_fits_available_time():
    tasks = [
        Task(name="Playtime", duration=20, priority="low", category="enrichment", recurrence="daily"),
        Task(name="Feeding", duration=10, priority="high", category="feeding", recurrence="daily"),
        Task(name="Grooming", duration=30, priority="medium", category="grooming", recurrence="daily"),
    ]

    scheduled, skipped = Scheduler().generate_plan(tasks, available_minutes=35)

    assert [task.name for task in scheduled] == ["Feeding", "Playtime"]
    assert [task.name for task in skipped] == ["Grooming"]


def test_generate_plan_with_no_tasks_returns_empty_plan():
    scheduled, skipped = Scheduler().generate_plan([], available_minutes=60)

    assert scheduled == []
    assert skipped == []


def test_filter_by_time_skips_everything_when_no_minutes_available():
    tasks = [
        Task(name="Feeding", duration=10, priority="high", category="feeding", recurrence="daily"),
        Task(name="Walk", duration=5, priority="high", category="walk", recurrence="daily"),
    ]

    scheduled, skipped = Scheduler().filter_by_time(tasks, available_minutes=0)

    assert scheduled == []
    assert [task.name for task in skipped] == ["Feeding", "Walk"]


def test_mark_task_complete_schedules_next_occurrence_one_day_later():
    pet = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age=3)
    task = Task(name="Feeding", duration=10, priority="high", category="feeding", recurrence="daily")
    pet.add_task(task)
    today = date(2026, 7, 12)

    pet.mark_task_complete(task, today=today)

    assert len(pet.get_tasks()) == 2
    next_task = pet.get_tasks()[1]
    assert next_task.completed is False
    assert next_task.due_date == today + timedelta(days=1)


def test_mark_task_complete_does_not_recur_for_one_time_tasks():
    pet = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age=3)
    task = Task(name="Vet checkup", duration=15, priority="high", category="health", recurrence="once")
    pet.add_task(task)

    pet.mark_task_complete(task)

    assert len(pet.get_tasks()) == 1


def test_is_due_today_is_true_when_due_date_is_exactly_today():
    today = date(2026, 7, 12)
    task = Task(
        name="Grooming", duration=30, priority="medium", category="grooming", recurrence="weekly", due_date=today
    )

    assert task.is_due_today(today=today) is True


def test_sort_by_time_returns_tasks_in_chronological_order():
    tasks = [
        Task(name="Evening walk", duration=20, priority="medium", category="walk", recurrence="daily", scheduled_time="18:00"),
        Task(name="Morning walk", duration=30, priority="high", category="walk", recurrence="daily", scheduled_time="07:30"),
        Task(name="Feeding", duration=10, priority="high", category="feeding", recurrence="daily", scheduled_time="08:00"),
    ]

    sorted_tasks = Scheduler().sort_by_time(tasks)

    assert [task.name for task in sorted_tasks] == ["Morning walk", "Feeding", "Evening walk"]


def test_find_time_conflicts_detects_tasks_at_the_exact_same_start_time():
    tasks = [
        Task(
            name="Morning walk",
            duration=15,
            priority="high",
            category="walk",
            recurrence="daily",
            scheduled_time="08:00",
        ),
        Task(
            name="Feeding",
            duration=10,
            priority="high",
            category="feeding",
            recurrence="daily",
            scheduled_time="08:00",
        ),
    ]

    conflicts = Scheduler().find_time_conflicts(tasks)

    assert len(conflicts) == 1
    assert "Morning walk" in conflicts[0]
    assert "Feeding" in conflicts[0]
