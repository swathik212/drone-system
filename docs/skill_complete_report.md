# Drone Navigation Project Notes

This file is a persistent handoff note for future AI agents working in `C:\\drone-system`.

## Project Purpose

Build an AI system for autonomous drone navigation in a simulated 3D urban environment.

Important scope boundary:

- Do include informed search, 3D environment modeling, simulation, benchmarking, and UI visualization.
- Do not include workforce scheduling or any CSP logic.

This scope reduction came from instructor feedback after Progress Report 1.

## Current Architecture

### Backend

- Language: Python
- API: FastAPI
- Core files:
  - `backend/algorithms.py`
  - `backend/models.py`
  - `backend/main.py`

Responsibilities:

- Represent the environment as a bounded 3D grid.
- Treat obstacles and no-fly zones as impassable.
- Support movement in horizontal, upward, and downward directions.
- Enforce asymmetric costs:
  - horizontal = 1
  - downward = 1
  - upward = 2
- Run `ucs`, `astar_manhattan`, `astar_euclidean`, and `astar_building`.
- Return `path`, `cost`, `nodes_expanded`, and `runtime`.

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

Responsibilities:

- Show a 3D urban grid and animate the drone path.
- Let the user select the algorithm.
- Let the user edit start and goal coordinates.
- Generate random obstacles.
- Display path metrics returned by the backend.

## Simulation Answer to Professor Question

The drone environment is simulated as a discrete 3D urban grid.

- The backend models the state space and computes optimal paths.
- The frontend renders the environment visually in 3D.
- The frontend sends environment data to FastAPI and animates the returned coordinates.

Earlier notes mentioned Unity, but the actual implementation uses React + Three.js instead. Keep documentation consistent with the codebase unless the user explicitly wants a Unity migration.

## Verified Commands

Backend benchmark example:

```powershell
@'
from algorithms import Environment, search
from models import Coordinate

def c(x, y, z):
    return Coordinate(x=x, y=y, z=z)

env = Environment(
    bounds=(10,10,10),
    start=c(0,0,0),
    goal=c(9,9,9),
    obstacles=[c(5,5,z) for z in range(6)],
    no_fly_zones=[]
)

for alg in ['ucs', 'astar_manhattan', 'astar_euclidean', 'astar_building']:
    result = search(env, alg)
    print(alg, result['cost'], result['nodes_expanded'], result['runtime'])
'@ | python -
```

Backend API smoke test:

```powershell
@'
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
req = {
    'bounds': [10, 10, 10],
    'start': {'x': 0, 'y': 0, 'z': 0},
    'goal': {'x': 9, 'y': 9, 'z': 9},
    'obstacles': [{'x': 5, 'y': 5, 'z': z} for z in range(6)],
    'no_fly_zones': [],
    'algorithm': 'astar_manhattan'
}
res = client.post('/pathfind', json=req)
print(res.status_code)
print(res.json())
'@ | python -
```

Frontend build:

```powershell
npm run build
```

Run locations:

- Backend commands: `C:\\drone-system\\backend`
- Frontend commands: `C:\\drone-system\\frontend`

## Verified Project State on 2026-04-03

- FastAPI `/pathfind` endpoint returned `200` in a smoke test.
- Search engine produced valid paths for UCS and all three A* modes.
- Frontend production build passed after removing unused React imports and one unused error variable.

## Benchmark Snapshot

These numbers were collected during report preparation and are safe to reuse in documentation unless the code changes significantly.

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

## Known Issues and Caveats

### 1. Building-aware heuristic is not yet fully validated

The current formula in `backend/algorithms.py` is:

`d_xy + max(0, h_obs - z)`

A counterexample was found where:

- heuristic value = `16`
- true optimal remaining cost from UCS = `12`

So this heuristic can overestimate in some maps and is not safely admissible yet. Treat it as experimental until revised.

### 2. Frontend no-fly-zone editing is incomplete

The frontend state model supports `noFlyZones`, and the 3D scene renders them, but the controls UI does not yet expose strong editing tools for them.

### 3. Bundle size warning

`npm run build` passes, but Vite warns that the frontend bundle is large because of 3D dependencies. This is not blocking for the course project but may be worth mentioning as an optimization item.

### 4. Repo state

This workspace is not currently a Git repository root, so `git status` and other git commands do not work here.

## Important Files

- `docs/project-technical-guide.pdf`: original technical guide, includes both navigation and CSP context
- `docs/progress-report-1.pdf`: previous report with the overly broad scope
- `docs/progress-report-2-guidelines.docx`: requirements for the second report
- `docs/progress-report-2.md`: current report draft generated from the implemented system
- `docs/progress-report-2.docx`: Word export of the report
- `docs/progress-report-2.pdf`: PDF export of the report
- `docs/skill.md`: this handoff file

## Report Export Notes

On 2026-04-03, the report was exported successfully to both Word and PDF.

- `.docx` was generated from the markdown source using `.venv` Python with `python-docx`, `markdown`, and `beautifulsoup4`.
- `.pdf` was generated from styled HTML using Microsoft Edge headless print-to-PDF.

If future agents need to refresh the exports after editing `docs/progress-report-2.md`, regenerate both formats rather than editing the binary files directly.

## Recommended Next Steps

1. Revise the building-aware heuristic or replace it with a provably admissible alternative.
2. Add stronger benchmark automation and charts for the final submission.
3. Improve frontend controls for no-fly-zone editing and richer scenario generation.
4. Capture final screenshots for the report and presentation.
5. Add automated tests around algorithm correctness and API behavior.
