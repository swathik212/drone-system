"""
Full benchmark suite: 6 algorithms × 7 scenarios.
Outputs:
  - Prints results table to stdout
  - Saves 3 charts to ../docs/assets/
"""

import sys
import os
import json
import matplotlib
matplotlib.use('Agg')  # non-interactive backend for file output
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from algorithms import Environment, search
from models import Coordinate

ALGORITHMS = [
    ("ucs",              "UCS"),
    ("astar_manhattan",  "A* Manhattan"),
    ("astar_euclidean",  "A* Euclidean"),
    ("astar_building",   "A* Building-Aware"),
    ("idastar",          "IDA*"),
    ("weighted_astar",   "Weighted A* (w=1.5)"),
]

def c(x, y, z):
    return Coordinate(x=x, y=y, z=z)

SCENARIOS = [
    {
        "name": "Open Grid (small)",
        "bounds": (8, 8, 6),
        "start": c(0, 0, 0),
        "goal":  c(7, 7, 4),
        "obstacles": [],
        "no_fly_zones": [],
    },
    {
        "name": "Open Grid (medium)",
        "bounds": (10, 10, 8),
        "start": c(0, 0, 0),
        "goal":  c(9, 9, 5),
        "obstacles": [],
        "no_fly_zones": [],
    },
    {
        "name": "Single Building Column",
        "bounds": (10, 10, 10),
        "start": c(0, 0, 0),
        "goal":  c(9, 9, 9),
        "obstacles": [c(5, 5, z) for z in range(6)],
        "no_fly_zones": [],
    },
    {
        "name": "Dense Urban Blocks",
        "bounds": (10, 10, 8),
        "start": c(0, 0, 0),
        "goal":  c(9, 9, 5),
        "obstacles": (
            [c(3, 3, z) for z in range(5)] +
            [c(3, 4, z) for z in range(5)] +
            [c(4, 3, z) for z in range(5)] +
            [c(7, 6, z) for z in range(4)] +
            [c(7, 7, z) for z in range(4)]
        ),
        "no_fly_zones": [c(5, 5, z) for z in range(3)],
    },
    {
        "name": "No-Fly Zone Corridor",
        "bounds": (10, 10, 8),
        "start": c(0, 0, 0),
        "goal":  c(9, 9, 4),
        "obstacles": [c(3, x, z) for x in range(10) for z in range(4)],
        "no_fly_zones": [c(7, y, z) for y in range(10) for z in range(3)],
    },
    {
        "name": "High Altitude Goal",
        "bounds": (10, 10, 10),
        "start": c(0, 0, 0),
        "goal":  c(5, 5, 9),
        "obstacles": [c(5, 5, z) for z in range(5)],
        "no_fly_zones": [],
    },
    {
        "name": "Maze-Like (high density)",
        "bounds": (10, 10, 6),
        "start": c(0, 0, 0),
        "goal":  c(9, 9, 3),
        "obstacles": (
            [c(2, y, z) for y in range(8) for z in range(3)] +
            [c(5, y, z) for y in range(2, 10) for z in range(3)] +
            [c(8, y, z) for y in range(8) for z in range(3)]
        ),
        "no_fly_zones": [],
    },
]

# IDA* re-expands nodes exponentially in 3D grids (branching factor 6, depth ~20+).
# Even small grids exceed practical runtime. We exclude it from the benchmark suite
# and document this as a known limitation. Smoke test data (bounds 10x10x5) is in skill.md.
IDA_SKIP_BENCHMARK = True

def run_scenario(scenario):
    env = Environment(
        bounds=scenario["bounds"],
        start=scenario["start"],
        goal=scenario["goal"],
        obstacles=scenario["obstacles"],
        no_fly_zones=scenario["no_fly_zones"],
    )
    results = {}
    for key, label in ALGORITHMS:
        if key == "idastar" and IDA_SKIP_BENCHMARK:
            results[label] = {"cost": "N/A", "nodes": "N/A", "runtime_ms": "N/A"}
            continue
        r = search(env, key)
        results[label] = {
            "cost": r["cost"],
            "nodes": r["nodes_expanded"],
            "runtime_ms": round(r["runtime"] * 1000, 2),
        }
    return results

# ── Run benchmarks ──────────────────────────────────────────────────────────
print("Running benchmarks...\n")
all_results = {}
for s in SCENARIOS:
    print(f"  {s['name']}...", flush=True)
    all_results[s["name"]] = run_scenario(s)

# ── Print table ─────────────────────────────────────────────────────────────
print("\n" + "=" * 110)
print(f"{'Scenario':<32} {'Algorithm':<22} {'Cost':>8} {'Nodes':>10} {'Runtime(ms)':>12}")
print("=" * 110)
for sname, res in all_results.items():
    for label, vals in res.items():
        cost = str(vals["cost"])
        nodes = str(vals["nodes"])
        rt = str(vals["runtime_ms"])
        print(f"{sname:<32} {label:<22} {cost:>8} {nodes:>10} {rt:>12}")
    print("-" * 110)

# ── Save JSON ────────────────────────────────────────────────────────────────
out_json = os.path.join(os.path.dirname(__file__), "../docs/assets/benchmark_results.json")
os.makedirs(os.path.dirname(out_json), exist_ok=True)
with open(out_json, "w") as f:
    json.dump(all_results, f, indent=2)
print(f"\nJSON saved to {out_json}")

# ── Charts ───────────────────────────────────────────────────────────────────
assets_dir = os.path.join(os.path.dirname(__file__), "../docs/assets")
os.makedirs(assets_dir, exist_ok=True)

algo_labels = [label for _, label in ALGORITHMS]
scenario_names = [s["name"] for s in SCENARIOS]

def safe_val(v, fallback=0):
    return v if isinstance(v, (int, float)) else fallback

# ── Chart 1: Nodes Expanded (grouped bar, all scenarios) ────────────────────
fig, axes = plt.subplots(2, 4, figsize=(20, 10))
axes = axes.flatten()
colors = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#edc948"]

for i, sname in enumerate(scenario_names):
    ax = axes[i]
    nodes = [safe_val(all_results[sname][lbl]["nodes"]) for lbl in algo_labels]
    bars = ax.bar(range(len(algo_labels)), nodes, color=colors)
    ax.set_title(sname, fontsize=9, fontweight='bold')
    ax.set_xticks(range(len(algo_labels)))
    ax.set_xticklabels([l.replace(" ", "\n") for l in algo_labels], fontsize=7)
    ax.set_ylabel("Nodes Expanded", fontsize=8)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
    for bar, val in zip(bars, nodes):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                    f"{val:,}", ha='center', va='bottom', fontsize=6)

axes[-1].axis('off')  # hide unused 8th subplot
fig.suptitle("Nodes Expanded by Algorithm per Scenario", fontsize=14, fontweight='bold')
plt.tight_layout()
chart1_path = os.path.join(assets_dir, "chart_nodes_expanded.png")
plt.savefig(chart1_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"Chart 1 saved: {chart1_path}")

# ── Chart 2: Runtime comparison (grouped bar, all scenarios) ─────────────────
fig, axes = plt.subplots(2, 4, figsize=(20, 10))
axes = axes.flatten()

for i, sname in enumerate(scenario_names):
    ax = axes[i]
    rts = [safe_val(all_results[sname][lbl]["runtime_ms"]) for lbl in algo_labels]
    bars = ax.bar(range(len(algo_labels)), rts, color=colors)
    ax.set_title(sname, fontsize=9, fontweight='bold')
    ax.set_xticks(range(len(algo_labels)))
    ax.set_xticklabels([l.replace(" ", "\n") for l in algo_labels], fontsize=7)
    ax.set_ylabel("Runtime (ms)", fontsize=8)
    for bar, val in zip(bars, rts):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                    f"{val:.1f}", ha='center', va='bottom', fontsize=6)

axes[-1].axis('off')
fig.suptitle("Runtime (ms) by Algorithm per Scenario", fontsize=14, fontweight='bold')
plt.tight_layout()
chart2_path = os.path.join(assets_dir, "chart_runtime.png")
plt.savefig(chart2_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"Chart 2 saved: {chart2_path}")

# ── Chart 3: Path cost heatmap (algorithms × scenarios) ──────────────────────
cost_matrix = []
for lbl in algo_labels:
    row = []
    for sname in scenario_names:
        v = all_results[sname][lbl]["cost"]
        row.append(safe_val(v, np.nan))
    cost_matrix.append(row)

cost_matrix = np.array(cost_matrix, dtype=float)

fig, ax = plt.subplots(figsize=(14, 5))
im = ax.imshow(cost_matrix, aspect='auto', cmap='YlOrRd')
ax.set_xticks(range(len(scenario_names)))
ax.set_xticklabels(scenario_names, rotation=30, ha='right', fontsize=9)
ax.set_yticks(range(len(algo_labels)))
ax.set_yticklabels(algo_labels, fontsize=9)
plt.colorbar(im, ax=ax, label="Path Cost")
for r in range(len(algo_labels)):
    for col in range(len(scenario_names)):
        val = cost_matrix[r, col]
        txt = f"{int(val)}" if not np.isnan(val) else "N/A"
        ax.text(col, r, txt, ha='center', va='center', fontsize=8,
                color='black' if val < np.nanmax(cost_matrix) * 0.7 else 'white')
ax.set_title("Path Cost — Algorithm × Scenario", fontsize=13, fontweight='bold')
plt.tight_layout()
chart3_path = os.path.join(assets_dir, "chart_cost_heatmap.png")
plt.savefig(chart3_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"Chart 3 saved: {chart3_path}")

print("\nAll benchmarks and charts complete.")
