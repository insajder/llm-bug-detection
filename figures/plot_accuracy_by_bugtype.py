import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict, Counter

with open('results_full.json') as f:
    data = json.load(f)

def classify_bug(buggy_lines, fixed_lines):
    buggy = ' '.join(buggy_lines).strip()
    fixed = ' '.join(fixed_lines).strip()
    if buggy == fixed:
        return 'Other/Complex'
    combined = (buggy + ' ' + fixed).lower()
    diff_b = set(buggy.split()) - set(fixed.split())
    diff_f = set(fixed.split()) - set(buggy.split())
    if any(op in str(diff_b) + str(diff_f) for op in ['__le__','__ge__','__lt__','__gt__','__eq__']):
        return 'Comparison Operator'
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

bug_types = {}
seen = set()
for item in data:
    key = (item['project'], item['bug_id'])
    if key not in seen:
        seen.add(key)
        bug_types[key] = classify_bug(item['buggy_lines'], item['fixed_lines'])

type_model_verdicts = defaultdict(lambda: defaultdict(list))
for item in data:
    key = (item['project'], item['bug_id'])
    btype = bug_types[key]
    type_model_verdicts[btype][item['model']].append(item['verdict'])

type_counts = Counter(bug_types.values())
ordered = [t for t, _ in sorted(type_counts.items(), key=lambda x: -x[1])]

llama_acc = []
mistral_acc = []
for btype in ordered:
    lv = type_model_verdicts[btype]['llama3.2']
    mv = type_model_verdicts[btype]['mistral']
    llama_acc.append(sum(1 for v in lv if v == 'correct') / len(lv) * 100 if lv else 0)
    mistral_acc.append(sum(1 for v in mv if v == 'correct') / len(mv) * 100 if mv else 0)

fig, ax = plt.subplots(figsize=(7, 4.2))
y = np.arange(len(ordered))
h = 0.35

ax.barh(y + h/2, llama_acc, h, label='Llama 3.2', color='#4CAF50')
ax.barh(y - h/2, mistral_acc, h, label='Mistral',   color='#FF9800')

for i, (la, ma) in enumerate(zip(llama_acc, mistral_acc)):
    ax.text(la + 0.8, i + h/2, f'{la:.1f}%', va='center', fontsize=7.5, color='#222')
    ax.text(ma + 0.8, i - h/2, f'{ma:.1f}%', va='center', fontsize=7.5, color='#222')

ax.set_yticks(y)
ax.set_yticklabels(ordered, fontsize=9)
ax.set_xlabel('Accuracy (%)', fontsize=9)
ax.set_xlim(0, 82)
ax.set_title('Bug detection accuracy by bug type', fontsize=10)
ax.legend(fontsize=8, loc='lower right')

plt.tight_layout()
plt.savefig('plot_accuracy_by_bugtype.png', dpi=180, bbox_inches='tight')
print("Saved.")