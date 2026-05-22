FEW_SHOT_EXAMPLES = """
Example 1: Vague input with no context

User:
Is this app idea good?

Assistant:
I need a little more context before judging it. What is the app idea, who is it for, and what problem does it solve?

---

Example 2: Vague input with existing context

Business context:
Idea: habit tracker for university students
Target users: students aged 18-25
Geography: Lithuania
Monetization: freemium subscription

User:
Is this good?

Assistant:
Potentially, but it is not automatically a strong business. The main issue is differentiation: habit trackers are common, so the idea needs a sharper niche.

For students, the strongest angle may be study routines, exam preparation, reminders, and social accountability rather than generic habit tracking.

I would validate:
- whether students already use Notion, Google Calendar, or existing habit apps
- whether they would pay for student-specific features
- whether retention stays high after the first 2-3 weeks

My initial view: continue only if the MVP focuses on a specific student pain, not a generic tracker.

---

Example 3: Tool-needed competitor question

User:
Are there similar apps already?

Assistant behavior:
Use retrieve_csv_context to look for comparable app-store categories, ratings, installs, pricing, and competitor signals.

Assistant:
There are likely comparable apps, so the question is not whether competitors exist, but whether your positioning is distinct enough.

Based on the app-store context, I would compare competitors across:
- target audience
- pricing model
- review complaints
- missing features
- retention hooks

A good MVP should focus on one underserved use case rather than trying to compete with broad productivity apps.
"""