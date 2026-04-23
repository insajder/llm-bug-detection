import json
import matplotlib.pyplot as plt
import numpy as np

with open("results_full.json") as f:
    results = json.load(f)

model = "mistral"
projects = sorted(set(r["project"] for r in results))


data = {}
for project in projects:
    model_results = [
        r for r in results
        if r["model"] == model and r["project"] == project
    ]
    total = len(model_results)

    if total == 0:
        data[project] = (0, 0, 0)
    else:
        correct = sum(1 for r in model_results if r["verdict"] == "correct")
        partial = sum(1 for r in model_results if r["verdict"] == "partial")
        wrong   = sum(1 for r in model_results if r["verdict"] == "wrong")

        data[project] = (
            round(correct / total * 100, 1),
            round(partial / total * 100, 1),
            round(wrong / total * 100, 1),
        )

projects = sorted(projects, key=lambda p: data[p][0], reverse=False)

correct_vals = [data[p][0] for p in projects]
partial_vals = [data[p][1] for p in projects]
wrong_vals   = [data[p][2] for p in projects]


fig, ax = plt.subplots(figsize=(12, 12))

y = np.arange(len(projects))
height = 0.3

bars1 = ax.barh(y - height, correct_vals, height, label="Correct", color="#4CAF50")
bars2 = ax.barh(y,          partial_vals, height, label="Partial", color="#FF9800")
bars3 = ax.barh(y + height, wrong_vals,   height, label="Wrong",   color="#F44336")

ax.set_xlabel("Percentage (%)")
ax.set_ylabel("Project")
ax.set_title(f"{model.upper()} – Score Distribution by Project")

ax.set_yticks(y)
ax.set_yticklabels(projects, fontsize=14)

ax.set_xlim(0, 110)
ax.legend()


for bars in [bars1, bars2, bars3]:
    for bar in bars:
        width = bar.get_width()
        if width > 0:
            ax.text(
                width + 1,
                bar.get_y() + bar.get_height()/2,
                f"{width:.1f}%",
                va="center",
                fontsize=12
            )

plt.tight_layout()
plt.savefig(f"plot_distribution_{model}.png", dpi=150)
plt.close()

print("Saved!")