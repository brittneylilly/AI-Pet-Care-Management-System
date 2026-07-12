# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
A tradeoff my scheduler makes is picking tasks one at a time in priority order and never reconsidering earlier choices, instead of checking every possible combination for the best fit.

- Why is that tradeoff reasonable for this scenario?
The tradeoff mentioned is reasonable for this scenario because the pet owner needs a quick and trustworthy daily plan, rather than a perfectly optimized one. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
