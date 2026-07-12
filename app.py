import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, available_minutes=60)
else:
    st.session_state.owner.name = owner_name

owner = st.session_state.owner
owner.available_minutes = st.number_input(
    "Available minutes today", min_value=1, max_value=600, value=owner.available_minutes
)

st.divider()

st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    owner.add_pet(Pet(name=pet_name, species=species, breed="", age=0))
    st.success(f"Added {pet_name} ({species}).")

if owner.get_pets():
    st.write("Current pets:")
    st.table([{"name": p.name, "species": p.species} for p in owner.get_pets()])
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Add a Task")

if owner.get_pets():
    pet_names = [p.name for p in owner.get_pets()]
    selected_pet_name = st.selectbox("Pet", pet_names)
    selected_pet = next(p for p in owner.get_pets() if p.name == selected_pet_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    col4, col5 = st.columns(2)
    with col4:
        recurrence = st.selectbox("Repeats", ["once", "daily", "weekly"], index=1)
    with col5:
        task_time = st.time_input("Time of day", value=None)

    if st.button("Add task"):
        selected_pet.add_task(
            Task(
                name=task_title,
                duration=int(duration),
                priority=priority,
                category="general",
                recurrence=recurrence,
                scheduled_time=task_time.strftime("%H:%M") if task_time else None,
            )
        )
        st.success(f"Added '{task_title}' to {selected_pet.name}.")

    scheduler = Scheduler()
    all_tasks = owner.get_all_tasks()

    if all_tasks:
        st.write("Current tasks:")

        col1, col2 = st.columns(2)
        with col1:
            sort_choice = st.selectbox("Sort by", ["Priority", "Duration", "Time of day"])
        with col2:
            status_choice = st.selectbox("Show", ["All", "Incomplete", "Completed"])

        view_tasks = all_tasks
        if status_choice == "Incomplete":
            view_tasks = scheduler.filter_by_status(view_tasks, completed=False)
        elif status_choice == "Completed":
            view_tasks = scheduler.filter_by_status(view_tasks, completed=True)

        if sort_choice == "Priority":
            view_tasks = scheduler.sort_by_priority(view_tasks)
        elif sort_choice == "Duration":
            view_tasks = scheduler.sort_by_duration(view_tasks)
        else:
            view_tasks = scheduler.sort_by_time(view_tasks)

        pet_by_task_name = {t.name: p.name for p in owner.get_pets() for t in p.get_tasks()}
        st.table(
            [
                {
                    "pet": pet_by_task_name.get(t.name, ""),
                    "task": t.name,
                    "time": t.scheduled_time or "—",
                    "duration_minutes": t.duration,
                    "priority": t.priority,
                    "status": "done" if t.completed else "pending",
                }
                for t in view_tasks
            ]
        )

        incomplete_tasks = scheduler.filter_by_status(all_tasks, completed=False)
        if incomplete_tasks:
            task_to_complete = st.selectbox(
                "Mark a task complete", [t.name for t in incomplete_tasks], key="complete_task_select"
            )
            if st.button("Mark complete"):
                task_obj = next(t for t in incomplete_tasks if t.name == task_to_complete)
                owning_pet = next(p for p in owner.get_pets() if task_obj in p.get_tasks())
                owning_pet.mark_task_complete(task_obj)
                st.success(f"Marked '{task_to_complete}' complete. If it repeats, the next one is already scheduled.")
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Add a pet first before adding tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generates today's plan from all pets' tasks using the Scheduler.")

if st.button("Generate schedule"):
    scheduler = Scheduler()
    due_today = scheduler.get_tasks_for_owner(owner)

    duplicates = scheduler.find_duplicate_tasks(due_today)
    if duplicates:
        names = ", ".join(f"'{task.name}'" for task in duplicates)
        st.warning(f"🔁 Duplicate task(s) — you may have added these by accident: {names}")

    for message in scheduler.find_time_conflicts(due_today):
        st.warning(f"⏰ {message}")

    overload_warning = scheduler.find_overloaded_priority(due_today, owner.available_minutes)
    if overload_warning:
        st.warning(f"⌛ {overload_warning} Consider freeing up more time or lowering a task's priority.")

    plan, skipped = scheduler.generate_plan(due_today, owner.available_minutes)

    if plan:
        st.write(f"Today's Schedule for {owner.name} ({owner.available_minutes} minutes available):")
        st.table(
            [
                {"time": t.scheduled_time or "—", "task": t.name, "duration_minutes": t.duration, "priority": t.priority}
                for t in plan
            ]
        )
        for task in plan:
            st.caption(scheduler.explain(task))
        st.success(f"Scheduled {sum(t.duration for t in plan)} of {owner.available_minutes} available minutes.")
    else:
        st.warning("No tasks fit in the available time. Add tasks or increase available minutes.")

    if skipped:
        st.write("Skipped (ran out of time):")
        st.table([{"task": t.name, "duration_minutes": t.duration, "priority": t.priority} for t in skipped])
