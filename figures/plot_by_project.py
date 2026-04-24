import json
import os
import matplotlib.pyplot as plt
import numpy as np

# ---------- IEEE STYLE OPTIMIZED ----------
plt.rcParams.update({
    'font.size': 18,
    'axes.titlesize': 22,
    'axes.labelsize': 20,
    'xtick.labelsize': 18,
    'ytick.labelsize': 18,
    'legend.fontsize': 18
})

# ---------- PATHS ----------
base_dir = os.path.dirname(os.path.dirname(__file__))
json_path = os.path.join(base_dir, "results_full.json")
output_path = os.path.join(os.path.dirname(__file__), "plot_by_project.png")

with open(json_path) as f:
    results = json.load(f)

# ---------- DATA ----------
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
            correct = sum(r["verdict"] == "correct" for r in model_results)
            project_data[project][model] = round(correct / total * 100, 1)

# Sortiranje po Llama 3.2 performansama
projects = sorted(projects, key=lambda p: project_data[p]["llama3.2"], reverse=True)

values_llama = [project_data[p]["llama3.2"] for p in projects]
values_mistral = [project_data[p]["mistral"] for p in projects]

# ---------- PLOT ----------
# Povećana visina na 16 jer imamo 17 projekata x 2 modela = 34 bara
fig, ax = plt.subplots(figsize=(12, 16))

y = np.arange(len(projects))
height = 0.35 # Debljina barova

# Zelena za Llama, Narandžasta za Mistral (kao u prethodnim)
bars1 = ax.barh(y - height/2, values_llama, height, label="LLaMA 3.2", color="#4CAF50")
bars2 = ax.barh(y + height/2, values_mistral, height, label="Mistral", color="#FF9800")

ax.set_xlabel("Accuracy (%)", labelpad=15)
ax.set_ylabel("Project", labelpad=15)
ax.set_title("Bug Detection Accuracy: LLaMA 3.2 vs. Mistral", pad=25)

ax.set_yticks(y)
ax.set_yticklabels(projects)

ax.invert_yaxis() # Da najbolji projekti budu na vrhu

# Proširen x-limit da legenda i procenti imaju mesta
ax.set_xlim(0, 125) 
ax.legend(loc="lower right", frameon=True, shadow=True)

# ---------- LABELS ----------
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
                fontsize=15
            )

add_labels(bars1)
add_labels(bars2)

plt.tight_layout()

# Visok DPI za finalnu verziju rada
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"Saved")
print("Done!")