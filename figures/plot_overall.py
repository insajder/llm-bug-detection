import os
import json
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

script_name = os.path.basename(__file__)
file_name_no_ext = os.path.splitext(script_name)[0]
output_path = os.path.join(os.path.dirname(__file__), f"{file_name_no_ext}.png")

with open(json_path) as f:
    results = json.load(f)

models = ["llama3.2", "mistral"]
model_labels = ["LLaMA 3.2", "Mistral"]

categories = ["correct", "partial", "wrong"]
category_labels = ["Correct", "Partial", "Wrong"]
colors = ["#4CAF50", "#FF9800", "#F44336"]

x = np.arange(len(models))
width = 0.25

fig, ax = plt.subplots(figsize=(12, 9))

for i, (category, label, color) in enumerate(zip(categories, category_labels, colors)):
    values = []
    for model in models:
        model_results = [r for r in results if r["model"] == model]
        total = len(model_results)
        
        if total == 0:
            values.append(0)
        else:
            count = sum(1 for r in model_results if r["verdict"] == category)
            values.append(round(count / total * 100, 1))

    ax.bar(x + i * width, values, width, label=label, color=color)

ax.set_xlabel("Model", labelpad=15)
ax.set_ylabel("Percentage (%)", labelpad=15)
ax.set_title("Overall Bug Detection Results by Model", pad=25)

ax.set_xticks(x + width)
ax.set_xticklabels(model_labels)

ax.legend(loc='upper right', frameon=True, shadow=True)
ax.set_ylim(0, 110)

for bars in ax.containers:
    ax.bar_label(bars, fmt="%.1f%%", padding=5, fontsize=16)

plt.tight_layout()

plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.close("all")

print(f"Saved")
print("Done!")