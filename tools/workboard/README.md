# Expansion Team Workboard

Live page: https://claude.ai/artifact/PL4PTJCsE9VVVFH42uLyoV

Tracks every Expansion and Fleet Ops project and program with health, owners, milestones,
blockers and 1:1 notes. Data lives in the artifact's shared database (`projects` collection),
not in this file. It was seeded on 2026-09-25 from Notion: Special Projects Tracker,
Market Expansion Sprint Priorities, and Expansion Actions.

`workboard.html` is the page source. It loads `mnkyjane-variable.woff2` (Jetson brand font),
which is published alongside the page and falls back to system fonts if missing.

## Project document shape

name, stream (Special Projects | Expansion | Fleet), kind (Project | Program), owners[],
sponsor, health (green | yellow | red | hold | done), target (YYYY-MM-DD), goal, nextStep,
blockers, notion, milestones[{id, title, due, done, doneOn}], notes[{id, date, text}], updatedAt
