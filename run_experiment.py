import ollama
import os
import json
import urllib.request

COMMON_WORDS = {
    "the", "a", "an", "is", "in", "to", "and", "or", "if", "for",
    "of", "this", "that", "it", "be", "as", "at", "by", "we", "on",
    "with", "from", "not", "but", "are", "was", "have", "has", "had",
    "self", "return", "true", "false", "none", "#"
}

REPOS = {
    "ansible": "ansible/ansible",
    "black": "psf/black",
    "cookiecutter": "cookiecutter/cookiecutter",
    "fastapi": "tiangolo/fastapi",
    "httpie": "httpie/cli",
    "keras": "keras-team/keras",
    "luigi": "spotify/luigi",
    "matplotlib": "matplotlib/matplotlib",
    "pandas": "pandas-dev/pandas",
    "PySnooper": "cool-RR/PySnooper",
    "sanic": "sanic-org/sanic",
    "scrapy": "scrapy/scrapy",
    "spacy": "explosion/spaCy",
    "thefuck": "nvbn/thefuck",
    "tornado": "tornadoweb/tornado",
    "tqdm": "tqdm/tqdm",
    "youtube-dl": "ytdl-org/youtube-dl"
}

def read_bug_info(info_path):
    info = {}
    with open(info_path, "r") as f:
        for line in f:
            line = line.strip()
            if "=" in line:
                key, value = line.split("=", 1)
                info[key] = value.strip('"')
    return info

def read_patch(patch_path):
    with open(patch_path, "r") as f:
        content = f.read()
    
    buggy_lines = []
    fixed_lines = []
    filepath = None
    
    for line in content.splitlines():
        if line.startswith("diff --git"):
            filepath = line.split(" b/")[-1]
        if line.startswith("-") and not line.startswith("---"):
            buggy_lines.append(line[1:].strip())
        if line.startswith("+") and not line.startswith("+++"):
            fixed_lines.append(line[1:].strip())
    
    return filepath, buggy_lines, fixed_lines

def fetch_file(repo, commit, filepath):
    url = f"https://raw.githubusercontent.com/{repo}/{commit}/{filepath}"
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode("utf-8")
    except:
        return None

def extract_function(code, buggy_line):
    lines = code.splitlines()
    bug_index = None
    
    for i, line in enumerate(lines):
        if buggy_line in line:
            bug_index = i
            break
    
    if bug_index is None:
        return None
    
    start = bug_index
    while start > 0:
        if lines[start].startswith("def ") or lines[start].startswith("class "):
            break
        start -= 1
    
    end = bug_index + 1
    while end < len(lines):
        if end != bug_index + 1:
            if lines[end].startswith("def ") or lines[end].startswith("class "):
                break
        end += 1
    
    return "\n".join(lines[start:end])

def ask_model(function_code, model_name):
    prompt = f"""Here is a Python function. It contains a bug. Find the bug and explain how to fix it.

{function_code}"""

    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.message.content

def get_key_words(buggy_lines, fixed_lines):
    buggy_words = set()
    fixed_words = set()
    
    for line in buggy_lines:
        for word in line.split():
            buggy_words.add(word.strip("(),"))
    
    for line in fixed_lines:
        for word in line.split():
            word = word.strip("(),")
            if len(word) > 3 and word.lower() not in COMMON_WORDS:
                fixed_words.add(word)
    
    new_words = fixed_words - buggy_words
    return new_words

def evaluate_response(response, buggy_lines, fixed_lines):
    key_words = get_key_words(buggy_lines, fixed_lines)
    response_lower = response.lower()
    
    found_keywords = []
    for word in key_words:
        if word.lower() in response_lower:
            found_keywords.append(word)
    
    mentions_bug = any(phrase in response_lower for phrase in [
        "bug", "issue", "problem", "error", "fix", "missing", "incorrect"
    ])
    
    if found_keywords:
        return "correct"
    elif mentions_bug:
        return "partial"
    else:
        return "wrong"

def run_experiment(project, repo, model_name, max_bugs=20):
    results = []
    bugs_path = f"BugsInPy/projects/{project}/bugs"
    
    if not os.path.exists(bugs_path):
        return results
    
    bug_ids = sorted([
        int(d) for d in os.listdir(bugs_path)
        if d.isdigit()
    ])[:max_bugs]
    
    for i, bug_id in enumerate(bug_ids):
        patch_path = f"{bugs_path}/{bug_id}/bug_patch.txt"
        info_path = f"{bugs_path}/{bug_id}/bug.info"
        
        if not os.path.exists(patch_path):
            continue
        
        print(f"  [{i+1}/{len(bug_ids)}] Bug {bug_id}...")
        
        info = read_bug_info(info_path)
        commit = info.get("buggy_commit_id")
        filepath, buggy, fixed = read_patch(patch_path)
        
        if not filepath or not buggy or not commit:
            continue
        
        code = fetch_file(repo, commit, filepath)
        if not code:
            continue
        
        function_code = extract_function(code, buggy[0])
        if not function_code:
            continue
        
        answer = ask_model(function_code, model_name)
        verdict = evaluate_response(answer, buggy, fixed)
        
        results.append({
            "project": project,
            "bug_id": bug_id,
            "model": model_name,
            "buggy_lines": buggy,
            "fixed_lines": fixed,
            "verdict": verdict
        })
    
    return results

models = ["llama3.2", "mistral"]
all_results = []

for model in models:
    print(f"\n=== Testing {model} ===")
    for project, repo in REPOS.items():
        print(f"\n{project}:")
        results = run_experiment(project, repo, model, max_bugs=9999)
        all_results.extend(results)
        
        correct = sum(1 for r in results if r["verdict"] == "correct")
        total = len(results)
        if total > 0:
            print(f"  -> {correct}/{total} correct")

with open("results_full.json", "w") as f:
    json.dump(all_results, f, indent=2)

print("\n\n=== FINAL RESULTS ===")
for model in models:
    model_results = [r for r in all_results if r["model"] == model]
    correct = sum(1 for r in model_results if r["verdict"] == "correct")
    partial = sum(1 for r in model_results if r["verdict"] == "partial")
    wrong = sum(1 for r in model_results if r["verdict"] == "wrong")
    total = len(model_results)
    if total > 0:
        pct = round(correct / total * 100, 1)
        print(f"\n{model} ({total} bugs):")
        print(f"  Correct: {correct} ({pct}%)")
        print(f"  Partial: {partial}")
        print(f"  Wrong:   {wrong}")

