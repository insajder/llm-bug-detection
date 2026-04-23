import json

with open("results_full.json") as f:
    results = json.load(f)

models = ["llama3.2", "mistral"]
projects = sorted(set(r["project"] for r in results))

print(f"{'Project':<20} {'llama3.2':>10} {'mistral':>10} {'Diff':>8}")
print("-" * 52)

for project in projects:
    row = {}
    for model in models:
        model_results = [
            r for r in results
            if r["model"] == model and r["project"] == project
        ]
        total = len(model_results)
        if total == 0:
            row[model] = None
            continue
        correct = sum(1 for r in model_results if r["verdict"] == "correct")
        row[model] = round(correct / total * 100, 1)
    
    if row["llama3.2"] is None or row["mistral"] is None:
        continue
    
    diff = round(row["llama3.2"] - row["mistral"], 1)
    diff_str = f"+{diff}%" if diff > 0 else f"{diff}%"
    print(f"{project:<20} {row['llama3.2']:>9}% {row['mistral']:>9}% {diff_str:>8}")

