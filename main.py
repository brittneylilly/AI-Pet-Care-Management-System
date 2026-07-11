"""Temporary testing ground for pawpal_system.py."""

from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner(name="Jordan", available_minutes=60)

biscuit = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age=3)
whiskers = Pet(name="Whiskers", species="cat", breed="Tabby", age=5)

biscuit.add_task(Task(name="Morning walk", duration=30, priority="high", category="walk", recurrence="daily"))
biscuit.add_task(Task(name="Feeding", duration=10, priority="high", category="feeding", recurrence="daily"))
whiskers.add_task(Task(name="Litter box cleaning", duration=15, priority="medium", category="grooming", recurrence="daily"))
whiskers.add_task(Task(name="Playtime", duration=20, priority="low", category="enrichment", recurrence="daily"))

owner.add_pet(biscuit)
owner.add_pet(whiskers)

scheduler = Scheduler()
plan = scheduler.generate_plan_for_owner(owner)

print(f"Today's Schedule for {owner.name} ({owner.available_minutes} minutes available)")
print("=" * 50)

if not plan:
    print("No tasks fit in the available time.")
else:
    total_minutes = 0
    for task in plan:
        total_minutes += task.duration
        print(f"- {task.name:<20} {task.duration:>3} min  [{task.priority} priority]  ({task.category})")
        print(f"    -> {scheduler.explain(task)}")

    print("-" * 50)
    print(f"Total scheduled time: {total_minutes} / {owner.available_minutes} minutes")

skipped = [t for t in owner.get_all_tasks() if t not in plan]
if skipped:
    print("\nSkipped (ran out of time):")
    for task in skipped:
        print(f"- {task.name} ({task.duration} min, {task.priority} priority)")
