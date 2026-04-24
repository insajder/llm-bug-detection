import json
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict, Counter

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

script_name = os.path.basename(__file__)
file_name_no_ext = os.path.splitext(script_name)[0]
output_path = os.path.join(os.path.dirname(__file__), f"{file_name_no_ext}.png")

with open(json_path) as f:
    results = json.load(f)

# ---------- CLASSIFICATION ----------
def classify_bug(buggy_lines, fixed_lines):
    buggy = ' '.join(buggy_lines).strip()
    fixed = ' '.join(fixed_lines).strip()
    
    if buggy == fixed:
        return 'Other/Complex'
    
    combined = (buggy + ' ' + fixed).lower()
    
    # Tvoja diff logika
    diff_b = set(buggy.split()) - set(fixed.split())
    diff_f = set(fixed.split()) - set(buggy.split())
    
    if any(op in str(diff_b) + str(diff_f) for op in ['__le__','__ge__','__lt__','__gt__','__eq__']):
        return 'Comparison Operator'
    
    # Ostale kategorije po tvom redosledu
    if any(k in combined for k in ['none','is none','is not none']):
        return 'Null/None Check'
    if any(k in combined for k in ['return','yield']):
        return 'Return Value'
    if any(k in combined for k in ['index','[0]','[-1]','len(']):
        return 'Indexing'
    if any(k in combined for k in ['except','try:','raise','error','exception']):
        return 'Error Handling'
    if any(k in combined for k in ['if ','elif ','else:']):
        return 'Conditional Logic'
    if any(k in combined for k in ['for ','while ','break','continue']):
        return 'Loop Logic'
    if any(k in combined for k in ['str(','int(','float(','bool(','list(','dict(']):
        return 'Type Conversion'
        
    return 'Other/Complex'

# ---------- DATA PROCESSING ----------
bug_types = {}
seen = set()

for item in results:
    key = (item['project'], item['bug_id'])
    if key not in seen:
        seen.add(key)
        bug_types[key] = classify_bug(item['buggy_lines'], item['fixed_lines'])

type_model_verdicts = defaultdict(lambda: defaultdict(list))

for item in results:
    key = (item['project'], item['bug_id'])
    btype = bug_types[key]
    type_model_verdicts[btype][item['model']].append(item['verdict'])

type_counts = Counter(bug_types.values())
ordered = [t for t, _ in sorted(type_counts.items(), key=lambda x: -x[1])]

# ---------- ACCURACY CALCULATION ----------
llama_acc = []
mistral_acc = []

for btype in ordered:
    lv = type_model_verdicts[btype]['llama3.2']
    mv = type_model_verdicts[btype]['mistral']

    llama_acc.append(sum(v == 'correct' for v in lv) / len(lv) * 100 if lv else 0)
    mistral_acc.append(sum(v == 'correct' for v in mv) / len(mv) * 100 if mv else 0)

# ---------- PLOT ----------
fig, ax = plt.subplots(figsize=(12, 11))

y = np.arange(len(ordered))
height = 0.35

bars1 = ax.barh(y - height/2, llama_acc, height, label='LLaMA 3.2', color='#4CAF50')
bars2 = ax.barh(y + height/2, mistral_acc, height, label='Mistral', color='#FF9800')

# ---------- LABELS ----------
def add_labels(bars):
    for bar in bars:
        w = bar.get_width()
        if w >= 0:
            ax.text(
                w + 1, 
                bar.get_y() + bar.get_height()/2,
                f'{w:.1f}%', 
                va='center', 
                ha='left',
                fontsize=15
            )

add_labels(bars1)
add_labels(bars2)

ax.set_yticks(y)
ax.set_yticklabels(ordered)
ax.invert_yaxis()
ax.set_xlabel('Accuracy (%)', labelpad=15)
ax.set_ylabel('Bug Type', labelpad=15)
ax.set_title('Bug Detection Accuracy: LLaMA 3.2 vs. Mistral', pad=25)

ax.set_xlim(0, 125) 
ax.legend(loc='lower right', frameon=True, shadow=True)

plt.tight_layout()
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"Grafik uspešno generisan: {output_path}")