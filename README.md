# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output from running `python main.py`:

```
Today's Schedule for Jordan (60 minutes available)
==================================================
- Vet checkup           15 min  [high priority]  (health)
    -> Vet checkup (high priority, 15 min) scheduled for health.
- Morning walk          30 min  [high priority]  (walk)
    -> Morning walk (high priority, 30 min) scheduled for walk.
- Litter box cleaning   15 min  [medium priority]  (grooming)
    -> Litter box cleaning (medium priority, 15 min) scheduled for grooming.
--------------------------------------------------
Total scheduled time: 60 / 60 minutes

Skipped (ran out of time):
- Evening walk (20 min, medium priority)
- Playtime (20 min, low priority)

Conflicts:
- Time conflict: 'Playtime' (09:00, 20 min) overlaps with 'Vet checkup' (09:15, 15 min)

==================================================
Sorted by time of day:
- 07:30  Morning walk (30 min)
- 08:00  Feeding (10 min)
- 08:00  Feeding (10 min)
- 09:00  Playtime (20 min)
- 09:15  Vet checkup (15 min)
- 12:00  Litter box cleaning (15 min)
- 18:00  Evening walk (20 min)

Incomplete tasks (filter_by_status):
- Evening walk
- Morning walk
- Vet checkup
- Feeding
- Litter box cleaning
- Playtime

Biscuit's tasks (filter_by_pet_name):
- Evening walk
- Feeding
- Morning walk
- Vet checkup
- Feeding

All of Biscuit's Feeding occurrences (completing spawns the next one):
- completed=True, due_date=2026-07-12
- completed=False, due_date=2026-07-13
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe app in numbered steps so a reader can follow along without watching a video

1. Open the app and type in your name and how many minutes you have today for pet care.
2. Add a pet by typing its name and picking its species.
3. Pick that pet from the list and add a task for it (like "Morning walk"), along with how long it takes and how important it is.
4. Repeat step 3 for as many tasks and pets as you'd like.
5. Click "Generate schedule" to see today's plan, built from your most important and best-fitting tasks.
6. If something doesn't fit or two tasks are scheduled at the same time, the app warns you instead of just leaving it out silently.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

## Smarter Scheduling:

Document each feature implemented and name the method it implements:

- **Sorting behavior** (`Scheduler.sort_by_priority()`, `Scheduler.sort_by_duration()`, `Scheduler.sort_by_time()`) — puts the most important tasks first, and among equally important tasks, puts the quicker ones first so more tasks fit in the day. You can also sort by how long a task takes or by what time of day it happens.

- **Filtering behavior** (`Scheduler.filter_by_status()`, `Scheduler.filter_by_pet_name()`, `Scheduler.get_tasks_for_owner()`, `Scheduler.get_tasks_for_pet()`) — lets you view just one pet's tasks, just finished or unfinished tasks, or only the tasks that actually need doing today.

- **Conflict detection logic** (`Scheduler.detect_conflicts()`) — warns you if the same task got added twice by accident, if two tasks are scheduled for the same time, or if you have more "must-do" tasks than you have time for today.

- **Recurring task logic** (`Task.mark_complete()` and `Pet.mark_task_complete()`) — when you finish a daily or weekly task, the app automatically lines up the next one for tomorrow (or next week) so you don't have to re-add it yourself.
