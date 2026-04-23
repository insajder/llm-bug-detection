import json

def get_key_words(buggy_lines, fixed_lines):
    buggy_words = set()
    fixed_words = set()
    COMMON_WORDS = {"the", "a", "is", "in", "to", "and", "self", "return"}
    
    for line in buggy_lines:
        for word in line.split():
            buggy_words.add(word.strip("(),"))
    for line in fixed_lines:
        for word in line.split():
            word = word.strip("(),")
            if len(word) > 3 and word.lower() not in COMMON_WORDS:
                fixed_words.add(word)
    return fixed_words - buggy_words

try:
    with open("results_full.json") as f:
        results = json.load(f)
except FileNotFoundError:
    print("Error: results_full.json not found!")
    results = []

print(f"{'Bug ID':>7} | {'Model':>10} | {'Verdict':>10} | {'Project'}")
print("-" * 60)

for r in results:
    bug_id = r.get("bug_id", "N/A")
    model = r.get("model", "N/A")
    verdict = r.get("verdict", "N/A")
    project = r.get("project", "N/A")

    print(f"{bug_id:>7} | {model:>10} | {verdict:>10} | {project}")

print("-" * 60)
print(f"Total: {len(results)}")
