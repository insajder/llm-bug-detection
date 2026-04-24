import json
import os
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'font.size': 18,
    'axes.titlesize': 22,
    'axes.labelsize': 20,
    'xtick.labelsize': 18,
    'ytick.labelsize': 18,
    'legend.fontsize': 18
})

base_dir = os.path.dirname(os.path.dirname(__file__))
json_path = os.path.join(base_dir, "results_full.json")
model_name = "llama3.2"
output_path = os.path.join(os.path.dirname(__file__), f"plot_distribution_{model_name}.png")

with open(json_path) as f:
    results = json.load(f)

model = model_name
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
        correct = sum(r["verdict"] == "correct" for r in model_results)
        partial = sum(r["verdict"] == "partial" for r in model_results)
        wrong   = sum(r["verdict"] == "wrong" for r in model_results)

        data[project] = (
            round(correct / total * 100, 1),
            round(partial / total * 100, 1),
            round(wrong / total * 100, 1),
        )

projects = sorted(projects, key=lambda p: data[p][0])

correct_vals = [data[p][0] for p in projects]
partial_vals = [data[p][1] for p in projects]
wrong_vals   = [data[p][2] for p in projects]

fig, ax = plt.subplots(figsize=(12, 18))

group_gap = 2.0  
y = np.arange(len(projects)) * group_gap
height = 0.5     

bars1 = ax.barh(y - height, correct_vals, height, label="Correct", color="#4CAF50")
bars2 = ax.barh(y,          partial_vals, height, label="Partial", color="#FF9800")
bars3 = ax.barh(y + height, wrong_vals,   height, label="Wrong",   color="#F44336")

ax.set_xlabel("Percentage (%)", labelpad=15)
ax.set_ylabel("Project", labelpad=15)
ax.set_title(f"{model.upper().replace('LLAMA', 'LLaMA ')} – Score Distribution by Project", pad=20)

ax.set_yticks(y)
ax.set_yticklabels(projects)

ax.set_xlim(0, 125) 

ax.legend(loc='lower right', frameon=True, shadow=True)

def add_labels(bars):
    for bar in bars:
        w = bar.get_width()
        if w >= 0:
            ax.text(
                w + 1, 
                bar.get_y() + bar.get_height()/2,
                f"{w:.1f}%",
                va="center",
                ha="left",   
                fontsize=16  
            )

add_labels(bars1)
add_labels(bars2)
add_labels(bars3)

plt.tight_layout()

plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"Saved")
print("Done!")
