# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
My initial design had four building blocks: an Owner (the pet's person, with how much time they have each day), a Pet (name, species, breed, age), a Task (a chore like a walk or feeding, with how long it takes and how urgent it is), and a Scheduler (the "brain" that looks at all the tasks and figures out the day's plan). An owner can have multiple pets, and each pet can have multiple tasks. The Scheduler just borrows the tasks it needs, it doesn't own them itself.

**b. Design changes**

- Did your design change during implementation?
Yes, initially I had a 5th class called Plan which I intended to be used to show skipped tasks, however I decided it was simpler to incorporate this class' functionality into the Scheduler class.

- If yes, describe at least one change and why you made it.
Instead of having a separate "Plan" class, I eliminated this class and decided to put a generate_plan() method in the Scheduler class to handle
the functionality that was intended for the Plan class.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
The constraints that my scheduler considers is primarily constraints related to the Owner, such as their work and activity schedule and their sleep schedule.

- How did you decide which constraints mattered most?
Because this app is intended to help busy pet owners stay consistent with pet care, the owner's ability to manage their scheduling constraints while still maintaining their pet's care is the primary reason why someone would use this app.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
A tradeoff my scheduler makes is picking tasks one at a time in priority order and never reconsidering earlier choices, instead of checking every possible combination for the best fit.

- Why is that tradeoff reasonable for this scenario?
The tradeoff mentioned is reasonable for this scenario because the pet owner needs a quick and trustworthy daily plan, rather than a perfectly optimized one. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI to turn my UML diagram into starter code and then to fill in the logic for sorting, filtering, recurring tasks, and conflict detection. I also used it to write my tests. 

- What kinds of prompts or questions were most helpful?
The most helpful prompts were ones that asked "why," not just "do this", such as asking it to explain a tradeoff in plain language.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
One moment was when the AI flagged that its own conflict-detection code only compares each task to the one right next to it in time, meaning it could miss an overlap between three or more tasks in some cases. Instead of just accepting the offer to rewrite the algorithm right then, I chose to hold off, have it document the limitation clearly, and add a test for the specific case I actually cared about instead of a bigger rewrite I hadn't verified I needed.

- How did you evaluate or verify what the AI suggested?
I verified it by running things myself rather than just trusting explanations. I ran python -m pytest in my own terminal to confirm the tests actually passed, and had the AI show real terminal/main.py output after each change so I could check the actual behavior with real numbers.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
The behaviors tested were: building a daily schedule that picks the most important tasks first and stays within the time available, handling a pet with no tasks at all, handling a day with zero free minutes, automatically lining up the next occurrence of a daily task after finishing it, making sure a one-time task doesn't keep coming back, correctly treating a task as "due" on its exact due date, and catching two tasks that are accidentally scheduled for the same time.

- Why were these tests important?
These tests were important because these are the exact situations a real pet owner would run into — an empty task list, a packed day, a repeating chore, or a scheduling mistake — and if the app got any of them wrong, it would either crash or quietly give the owner a bad or confusing plan without them knowing why


**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
I'm confident that the schedular works work correctly for everyday situations and specific edge cases I've already tested, like building a normal day's plan, handling a pet with no tasks, and catching two tasks booked at the same time. I'm less sure about a few trickier situations I haven't tested yet. If I had more time, I'd check what happens with three or more overlapping tasks (the conflict checker might miss one that isn't right next to another in time), bad input like a typo in a time or an unrecognized priority (which could crash the app instead of showing a friendly message), a much busier day with dozens of tasks to make sure everything still runs smoothly, and tasks that span midnight, since times are currently only compared within a single day.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am most satisfied with how the recurring tasks work automatically. When you mark a daily or weekly task as done, the app doesn't just check it off, it immediately creates the next one for you (tomorrow for a daily task, next week for a weekly one), with the correct date figured out automatically. You also caught a sneaky bug this caused, where the app was mistakenly treating "today's finished task" and "tomorrow's new task" as if you'd accidentally entered the same task twice, and got that fixed before calling it done.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If I had another round, I'd fix the conflict checker so it catches overlaps between any two tasks, not just tasks that happen to be next to each other once sorted by time. Right now it can miss a conflict if three tasks overlap in a more complicated pattern.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
An important thing I learned is that AI can write code fast, but I need to run it, check the real output and detect where it covers the edge cases I actually care about.