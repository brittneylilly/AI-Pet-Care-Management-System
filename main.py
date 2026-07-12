"""Temporary testing ground for pawpal_system.py."""

from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner(name="Jordan", available_minutes=60)

biscuit = Pet(name="Biscuit", species="dog", breed="Golden Retriever", age=3)
whiskers = Pet(name="Whiskers", species="cat", breed="Tabby", age=5)

# Tasks are added out of order (by scheduled_time) to prove sort_by_time actually sorts.
biscuit.add_task(Task(name="Evening walk", duration=20, priority="medium", category="walk", recurrence="daily", scheduled_time="18:00"))
biscuit.add_task(Task(name="Feeding", duration=10, priority="high", category="feeding", recurrence="daily", scheduled_time="08:00"))
biscuit.add_task(Task(name="Morning walk", duration=30, priority="high", category="walk", recurrence="daily", scheduled_time="07:30"))
whiskers.add_task(Task(name="Litter box cleaning", duration=15, priority="medium", category="grooming", recurrence="daily", scheduled_time="12:00"))
whiskers.add_task(Task(name="Playtime", duration=20, priority="low", category="enrichment", recurrence="daily", scheduled_time="09:00"))

# Overlaps with Whiskers' Playtime (09:00-09:20), across two different pets, to test time-conflict detection.
biscuit.add_task(Task(name="Vet checkup", duration=15, priority="high", category="health", recurrence="once", scheduled_time="09:15"))

owner.add_pet(biscuit)
owner.add_pet(whiskers)

# Mark one task complete. Since it's "daily", this automatically schedules the next occurrence.
biscuit.mark_task_complete(biscuit.get_tasks()[1])

scheduler = Scheduler()
plan, skipped = scheduler.generate_plan_for_owner(owner)

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

if skipped:
    print("\nSkipped (ran out of time):")
    for task in skipped:
        print(f"- {task.name} ({task.duration} min, {task.priority} priority)")

conflicts = scheduler.detect_conflicts(owner.get_all_tasks(), owner.available_minutes)
if conflicts:
    print("\nConflicts:")
    for conflict in conflicts:
        print(f"- {conflict}")

print("\n" + "=" * 50)
print("Sorted by time of day:")
for task in scheduler.sort_by_time(owner.get_all_tasks()):
    print(f"- {task.scheduled_time}  {task.name} ({task.duration} min)")

print("\nIncomplete tasks (filter_by_status):")
for task in scheduler.filter_by_status(owner.get_all_tasks(), completed=False):
    print(f"- {task.name}")

print("\nBiscuit's tasks (filter_by_pet_name):")
for task in scheduler.filter_by_pet_name(owner, "Biscuit"):
    print(f"- {task.name}")

print("\nAll of Biscuit's Feeding occurrences (completing spawns the next one):")
for task in biscuit.get_tasks():
    if task.name == "Feeding":
        print(f"- completed={task.completed}, due_date={task.due_date}")
