# LLM-Based Bug Detection: A Comparative Study (LLaMA 3.2 vs. Mistral) 

This repository contains the source code, experimental data, and results for a research project focused on automated bug detection using local Large Language Models (LLMs). The study evaluates and compares the performance of **LLaMA 3.2** and **Mistral** in identifying software defects at the function level.

## 📊 Research Overview
The experiment was conducted using **349 real-world bugs** sourced from the `BugsInPy` dataset, covering 17 diverse Python projects (e.g., *pandas, ansible, fastapi, matplotlib*).

### Key Findings:
- **Accuracy:** Both models were tested on their ability to identify the cause of a bug given the function context.
- **Statistical Significance:** A **McNemar test** was performed, yielding a p-value of **0.6844**, indicating no statistically significant difference in the overall detection accuracy between LLaMA 3.2 and Mistral.
- **Context Matters:** Function-level extraction proved to be the "sweet spot" for local LLM performance compared to line-level or file-level approaches.

## 📁 Project Structure

- `run_experiment.py`: The main execution script. It automates code fetching, function extraction, and handles communication with the Ollama API.
- `evaluate.py`: Implements the evaluation logic to score model responses based on fix-related keywords.
- `analyse.py`: Processes `results_full.json` to generate performance tables grouped by project.
- `statistical_analysis.py`: Runs the McNemar statistical test to compare the two models.
- `results_full.json`: The complete dataset containing all 349 test cases and model verdicts.
- `figures/`: Visualization scripts used to generate the research charts.
- `requirements.txt`: List of necessary Python dependencies.

## 🚀 Getting Started

### Prerequisites
1. Install [Ollama](https://ollama.ai/).
2. Pull the required models:
   ```bash
   ollama pull llama3.2
   ollama pull mistral

### Installation
Clone the repository and install the dependencies:

`pip install -r requirements.txt`

 ### Dataset
The project uses the **BugsInPy** dataset. Ensure it is cloned into the root directory:

`git clone https://github.com/soarsmu/BugsInPy`

### Usage
Run the experiment:

`python run_experiment.py`

Running the Analysis:

`python analyse.py`

`python statistical_analysis.py`

`python evaluate.py`

Generate plots:

`python plot_overall.py`

`python plot_by_project.py`

`python plot_distribution_llama3.2.py`

`python plot_distribution_mistral.py`

`python plot_accuracy_by_bugtype.py`

### Key Results

| Model      | Correct     | Partial | Wrong   | Accuracy | 
| ---------- | ----------- | ------- | ------- |  ------- | 
| Llama 3.2  | 151 (43.3%) | 171     | 27      | 43.3%    |
| Mistral    | 155 (44.4%) | 161     | 33      | 44.4%    |

## 🎓 Author
**Jelena Ilić Vulićević**

Master of Electrical and Computer Engineering | Software Engineer


## Citation

If you use this research or code in your work, please cite it as follows:

```bibtex
@misc{ilicvulicevic2026empirical,
      title={An Empirical Evaluation of Locally Deployed LLMs for Bug Detection in Python Code}, 
      author={Jelena Ilić Vulićević},
      year={2026},
      eprint={2604.23361},
      archivePrefix={arXiv},
      primaryClass={cs.SE},
      url={[https://arxiv.org/abs/2604.23361](https://arxiv.org/abs/2604.23361)}
}
