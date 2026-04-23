import json
import matplotlib.pyplot as plt
import numpy as np

with open("results_full.json") as f:
    results = json.load(f)

models = ["llama3.2", "mistral"]
projects = sorted(set(r["project"] for r in results))

project_data = {}
for project in projects:
    project_data[project] = {}
    for model in models:
        model_results = [
            r for r in results
            if r["model"] == model and r["project"] == project
        ]
        total = len(model_results)
        if total == 0:
            project_data[project][model] = 0
        else:
            correct = sum(1 for r in model_results if r["verdict"] == "correct")
            project_data[project][model] = round(correct / total * 100, 1)

projects = sorted(projects, key=lambda p: project_data[p]["llama3.2"], reverse=True)

values_llama = [project_data[p]["llama3.2"] for p in projects]
values_mistral = [project_data[p]["mistral"] for p in projects]

y = np.arange(len(projects))
height = 0.4

fig, ax = plt.subplots(figsize=(10, 9))

bars1 = ax.barh(y - height/2, values_llama, height, label="Llama 3.2", color="#4CAF50")
bars2 = ax.barh(y + height/2, values_mistral, height, label="Mistral", color="#FF9800")

ax.set_xlabel("Accuracy (%)")
ax.set_title("Bug detection accuracy by project")

ax.set_yticks(y)
ax.set_yticklabels(projects)

ax.invert_yaxis()
ax.legend()

ax.set_xlim(0, 110)

for bar in bars1:
    width = bar.get_width()
    ax.text(
        width + 1,
        bar.get_y() + bar.get_height()/2,
        f"{width:.1f}%",
        va="center",
        fontsize=8
    )

for bar in bars2:
    width = bar.get_width()
    ax.text(
        width + 1,
        bar.get_y() + bar.get_height()/2,
        f"{width:.1f}%",
        va="center",
        fontsize=8
    )

plt.tight_layout()
plt.savefig("plot_by_project.png", dpi=150)
plt.close()

print("Saved plot_by_project.png")