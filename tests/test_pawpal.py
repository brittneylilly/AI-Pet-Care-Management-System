from pawpal_system import Pet, Task


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
