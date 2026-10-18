# Agenda Math

Agenda timing arithmetic. An agenda adds up, and the gaps between the items count too.

## What it computes

- **The end truth** - a start time plus minutes: 09:30 plus 90 minutes is 11:00, and past midnight carries the day.
- **The run truth** - start and end of every item in a running order, with a gap between items.
- **The fit truth** - a running order against its window: 155 minutes needed in a 180-minute window is 25 spare.

## Boundary

Arithmetic only. Agenda Math adds the times, durations and gaps you type, in whole minutes on a 24-hour clock. It does not say how long an item should take, whether a plan is realistic, or what anyone has agreed to. You decide that.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (36 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/agendamath/
Repo: https://github.com/iLanis-agent/agendamath
