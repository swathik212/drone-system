# Drone Navigation Project Notes

This file is the current handoff note for future AI agents working in `C:\\drone-system`.

## Scope Boundary

Project focus:

- autonomous drone navigation in a simulated 3D urban environment

Explicitly out of scope:

- workforce scheduling
- CSP logic

This scope change came from instructor feedback after Progress Report 1.

## Report Files

Two report sets now exist in `docs`:

- `progress-report-2_complete_report.md`
- `progress-report-2_complete_report.docx`
- `progress-report-2_complete_report.pdf`

These preserve the earlier polished version that reads more like a near-final report.

- `progress-report-2.md`
- `progress-report-2.docx`
- `progress-report-2.pdf`

These should be treated as the current interim Progress Report 2 set.

Also preserved:

- `skill_complete_report.md`

This is the older snapshot of the project handoff notes before the report split.

## Current Architecture

### Backend

- Language: Python
- API: FastAPI
- Core files:
  - `backend/algorithms.py`
  - `backend/models.py`
  - `backend/main.py`

Implemented behavior:

- 3D grid state representation with `s = (x, y, z)`
- obstacles and no-fly zones treated as impassable
- movement costs:
  - horizontal = 1
  - downward = 1
  - upward = 2
- algorithms:
  - `ucs`
  - `astar_manhattan`
  - `astar_euclidean`
  - `astar_building`

### Frontend

- Language: TypeScript
- Framework: React + Vite
- 3D stack: Three.js + `@react-three/fiber` + `@react-three/drei`
- API client: Axios

Core files:

- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/components/Controls.tsx`
- `frontend/src/components/DroneMap.tsx`
- `frontend/src/main.tsx`

Implemented behavior:

- visualizes the 3D grid
- renders obstacles and no-fly zones
- animates the drone path
- allows algorithm selection
- allows start/goal edits
- supports random obstacle generation

## Verified State on 2026-04-03

- FastAPI `/pathfind` endpoint returned `200` in smoke testing.
- Search runs completed for UCS and all A* options.
- Frontend `npm run build` passed after removing unused React imports and one unused error variable.

## Benchmark Snapshot

These values were used in the reports and were collected during implementation.

### Open Grid

- UCS: cost `22`, nodes `530`, runtime about `13.704 ms`
- A* Manhattan: cost `22`, nodes `368`, runtime about `6.950 ms`
- A* Euclidean: cost `22`, nodes `405`, runtime about `13.053 ms`
- A* Building-Aware: cost `22`, nodes `386`, runtime about `9.807 ms`

### Single Building Column

- UCS: cost `36`, nodes `1309`, runtime about `33.487 ms`
- A* Manhattan: cost `36`, nodes `1158`, runtime about `30.433 ms`
- A* Euclidean: cost `36`, nodes `1224`, runtime about `33.415 ms`
- A* Building-Aware: cost `36`, nodes `1180`, runtime about `26.721 ms`

### Dense Urban Blocks

- UCS: cost `28`, nodes `981`, runtime about `19.973 ms`
- A* Manhattan: cost `28`, nodes `641`, runtime about `15.103 ms`
- A* Euclidean: cost `28`, nodes `721`, runtime about `10.819 ms`
- A* Building-Aware: cost `28`, nodes `641`, runtime about `16.495 ms`

## Known Issues

### Building-aware heuristic is still experimental

Current formula in `backend/algorithms.py`:

`d_xy + max(0, h_obs - z)`

Counterexample found:

- heuristic value = `16`
- true optimal remaining cost from UCS = `12`

So it can overestimate and is not yet safely admissible.

### UI support for no-fly zones is incomplete

The backend model supports no-fly zones and the scene can render them, but the UI controls are still limited.

### Bundle size warning exists

The frontend builds successfully, but Vite warns about large bundle size because of 3D dependencies.

## Export Notes

The current report exports can be regenerated from `docs/progress-report-2.md`.

- `.docx` generation uses `.venv` Python with `python-docx`, `markdown`, and `beautifulsoup4`
- `.pdf` generation uses a styled HTML export printed through Microsoft Edge headless

## Suggested Next Steps

1. refine or replace the building-aware heuristic
2. expand benchmarks and add charts
3. improve no-fly-zone controls in the frontend
4. capture screenshots for the report and demo
5. keep the interim and complete-report tracks separate so future edits do not overwrite the preserved snapshot
