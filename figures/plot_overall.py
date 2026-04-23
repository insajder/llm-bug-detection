import json
import matplotlib.pyplot as plt
import numpy as np

with open("results_full.json") as f:
    results = json.load(f)

models = ["llama3.2", "mistral"]
model_labels = ["Llama 3.2", "Mistral"]

projects = sorted(set(r["project"] for r in results))

fig, ax = plt.subplots(figsize=(8, 5))

categories = ["correct", "partial", "wrong"]
category_labels = ["Correct", "Partial", "Wrong"]
colors = ["#4CAF50", "#FF9800", "#F44336"]

x = np.arange(len(models))
width = 0.25

for i, (category, label, color) in enumerate(zip(categories, category_labels, colors)):
    values = []
    for model in models:
        model_results = [r for r in results if r["model"] == model]
        total = len(model_results)

        count = sum(1 for r in model_results if r["verdict"] == category)
        values.append(round(count / total * 100, 1))

    ax.bar(x + i * width, values, width, label=label, color=color)

ax.set_xlabel("Model")
ax.set_ylabel("Percentage (%)")
ax.set_title("Overall bug detection results by model")
ax.set_xticks(x + width)
ax.set_xticklabels(model_labels)
ax.legend()
ax.set_ylim(0, 100)

for bars in ax.containers:
    ax.bar_label(bars, fmt="%.1f%%", padding=3, fontsize=9)

plt.tight_layout()
plt.savefig("plot_overall.png", dpi=150)

print("Saved plot_overall.png")

fig, ax = plt.subplots(figsize=(14, 6))

categories = ["llama3.2", "mistral"]
colors = ["#4CAF50", "#FF9800"] 

x = np.arange(len(projects))
width = 0.35

plt.close("all")
print("Done!")