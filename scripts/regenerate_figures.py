#!/usr/bin/env python3
"""Regenerate the four root synthesis figures from public evidence."""
from pathlib import Path
import json
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)


def load(exp, name="summary.json"):
    return json.loads((ROOT / "experiments" / f"{exp:03d}" / "evidence" / name).read_text())


def save(name):
    plt.tight_layout()
    plt.savefig(OUT / name, dpi=220, bbox_inches="tight")
    plt.close()


# 1. Research arc
x = [15, 16, 17, 18]
y = [
    2.1838203220693897,
    load(16)["primary_result"]["final_oracle_tok_s_per_user"],
    load(17)["primary_result"]["oracle_tok_s_per_user"],
    load(18)["headline"]["tok_s_per_user"],
]
plt.figure(figsize=(10.8, 6.1))
ax = plt.gca()
ax.plot(x, y, marker="o", linewidth=2.5)
ax.axhline(5, linestyle="--", linewidth=1.5)
ax.set_xticks(x, [f"E{i:03d}" for i in x])
ax.set_ylabel("Admissible / validated tok/s/user")
ax.set_title("The research arc: local optimization hit a ceiling, scheduling changed the shape", pad=24)
ax.text(0.5, 1.01, "E018 is a validated independent-resource model, not a physical multi-GPU result.", transform=ax.transAxes, ha="center", va="bottom", fontsize=9)
for xi, yi in zip(x, y):
    ax.annotate(f"{yi:.2f}", (xi, yi), xytext=(0, 10), textcoords="offset points", ha="center", fontweight="bold")
ax.text(17.98, 5.08, "5 tok/s target", ha="right", va="bottom")
save("01-research-arc.png")


# 2. Timing-model repair
s21 = load(21)["model_validation"]
r22 = json.loads((ROOT / "experiments" / "022" / "evidence" / "run-result.json").read_text())["model_validation"]["ordered_validation"]
labels = ["Median", "p90", "Maximum"]
a = [s21["median_error"] * 100, s21["p90_error"] * 100, s21["maximum_error"] * 100]
b = [r22["median_percent"], r22["p90_percent"], r22["maximum_percent"]]
xx = np.arange(3)
w = 0.36
plt.figure(figsize=(10.8, 6.1))
ax = plt.gca()
ax.bar(xx - w / 2, a, w, label="E021")
ax.bar(xx + w / 2, b, w, label="E022")
ax.set_xticks(xx, labels)
ax.set_ylabel("Absolute timing-model error (%)")
ax.set_title("A bad model was invalidated, then rebuilt without a correction multiplier", pad=24)
ax.text(0.5, 1.01, "E022 held-out ordered-DAG validation, normalization_applied=false.", transform=ax.transAxes, ha="center", va="bottom", fontsize=9)
ax.legend()
ax.set_ylim(0, 108)
for i, v in enumerate(a):
    ax.text(i - w / 2, v + 1.5, f"{v:.2f}%", ha="center")
for i, v in enumerate(b):
    ax.text(i + w / 2, v + 1.5, f"{v:.2f}%", ha="center", fontweight="bold")
save("02-model-validation-repair.png")


# 3. Capacity unlocks
s = load(22)["statistics"]
vals = [s["a_feasible_inventory_count"], s["capacity_unlocks"]]
cats = ["Whole-layer feasible", "Sub-layer-only feasible"]
plt.figure(figsize=(10.8, 6.1))
ax = plt.gca()
bars = ax.bar(cats, vals)
ax.set_ylabel("Frozen E022 inventories")
ax.set_title("Sub-layer placement changed feasibility, not throughput, in the frozen 27-inventory suite", pad=24)
ax.text(0.5, 1.01, "Diagnostic planner result: 0% throughput uplift on all 21 whole-layer-feasible inventories.", transform=ax.transAxes, ha="center", va="bottom", fontsize=9)
for bar, v in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 0.35, str(v), ha="center", fontweight="bold", fontsize=13)
ax.set_ylim(0, 24)
save("03-capacity-unlocks.png")


# 4. E019 capacity/correctness evidence card
r = json.loads((ROOT / "experiments" / "019" / "evidence" / "correctness" / "full-93-sharded-receipt.public.json").read_text())
plt.figure(figsize=(10.8, 6.1))
ax = plt.gca()
ax.axis("off")
ax.set_title("E019: what was actually proved before the timing model failed", pad=18, fontsize=18)
items = [
    (0.25, 0.67, "1.56 TB", "Kimi K3 checkpoint payload\n497,220 tensors / 93 layers"),
    (0.75, 0.67, "376", "Independent worker placement units\n8 GiB-cap candidate"),
    (0.25, 0.36, "4.495 GiB", "Maximum accounted worker peak\nin that placement"),
    (0.75, 0.36, f"{r['maximum_relative_l2_error']:.2e}", "Maximum relative L2 error\nfull 93-layer shard traversal"),
]
for x0, y0, big, small in items:
    ax.text(x0, y0, big, ha="center", va="center", fontsize=26, fontweight="bold", transform=ax.transAxes)
    ax.text(x0, y0 - 0.105, small, ha="center", va="top", fontsize=11, linespacing=1.35, transform=ax.transAxes)
ax.text(0.5, 0.12, "Routes exact: YES   •   greedy token match: YES   •   single RTX 5090 sequential shard execution", ha="center", fontsize=11, transform=ax.transAxes)
ax.text(0.5, 0.035, "20.8836 tok/s is excluded: serial reconstruction missed by 103.9%, so the timing model was invalid.", ha="center", fontsize=10, fontweight="bold", transform=ax.transAxes)
save("04-e019-capacity-correctness.png")

print("Regenerated figures in", OUT)
