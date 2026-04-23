from statsmodels.stats.contingency_tables import mcnemar
import json

with open("results_full.json") as f:
    all_results = json.load(f)

llama = {f"{r['project']}_{r['bug_id']}": r['verdict'] for r in all_results if r['model'] == 'llama3.2'}
mistral = {f"{r['project']}_{r['bug_id']}": r['verdict'] for r in all_results if r['model'] == 'mistral'}

ids = sorted(set(llama.keys()) & set(mistral.keys()))

b = sum(1 for i in ids if llama[i] == "correct" and mistral[i] != "correct")
c = sum(1 for i in ids if llama[i] != "correct" and mistral[i] == "correct")

table = [[0, b], [c, 0]]

result = mcnemar(table, exact=True)

print(f"--- McNemar Statistical Test ---")
print(f"LLaMA correct, Mistral wrong (b): {b}")
print(f"Mistral correct, LLaMA wrong (c): {c}")
print(f"Resulting p-value: {result.pvalue:.4f}")

if result.pvalue > 0.05:
    print("Conclusion: No statistically significant difference (p > 0.05)")
else:
    print("Conclusion: Statistically significant difference (p <= 0.05)")