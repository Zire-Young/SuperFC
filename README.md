# SuperFC
<p align="center">
    <img src="assets\SuperFC.png" width=200 />
</p>


This repo contains rating and filtering codes and the high-quality function-calling dataset for SuperFC, a sustainable and strong function-calling agent.

Paper: [SuperFC: Selective Data Utilization for a Sustainable and Effective Function-Calling Agent](./Yang%20等%20-%20SuperFC%20Selective%20Data%20Utilization%20for%20a%20Sustainable%20and%20Effective%20Function-Calling%20Agent.pdf)


## 📣 Introduction
<p align="center">
    <img src="assets\workflow.png"/>
</p>



The function-calling agent is obtained by performing agent tuning the large language model (LLM) on function-calling dataset. However, even state-of-the-art datasets (e.g., xlam-function-calling-60k datasets) still contain numerous misleading examples of low-quality data, wasting significant computational resources and contribute to an unnecessary carbon footprint. Furthermore, such inductive bad data negatively impacts the performance of the agent. In this paper, we propose a set of scoring criteria specifically tailored to evaluate function-calling data and use these criteria to develop a data screening framework. By applying this framework to filter out low-quality data, we fine-tuned SuperFC, which demonstrates substantial improvements in both sustainability and performance. The SuperFC-7B training process reduced training time from 455 minutes to 85 minutes, resulting in a 80.02% reduction in carbon footprint. Simultaneously, fine-tuning on high-quality data subsets led to performance improvements of up to 3.68%. Additionally, we provide an in-depth analysis of the causes behind the low quality of synthetic function-calling data, offering valuable insights for future data synthesis in this domain.

<p align="center">
    <img src="assets\dimensions.png" width=500 />
</p>

<p align="center">
    <img src="assets\case_study.png"/>
</p>


## How to Run

### Score

The script accepts three mandatory arguments via the command line:

| Argument       | Type   | Required | Description                                                                 |
|----------------|--------|----------|-----------------------------------------------------------------------------|
| `--dataset_path` | str   | Yes      | Path to the dataset JSON file containing the data to be scored.             |
| `--model`       | str   | Yes      | Name of the model used for scoring.                                         |
| `--output_path` | str   | Yes      | Directory path where the output files will be saved.                        |

#### Example Command

To run the score script, use the following format:
```bash
bash python score_aysc.py --dataset_path <path_to_dataset> --model <your_model> --output_path <output_file_path>
```


#### Output Files

After execution, the script generates the following outputs in the specified `output_path` directory:

1. **score_by_\<model\>.json**: Contains the scores generated by the model.
2. **\<raw_dataset\>_with_score_by\_\<model\>.json**: Updated dataset file with added scores.
3. **logs/score_log_by_\<model\>.txt**: Logs of the scoring process for each data entry.


### Select

The script accepts four mandatory arguments via the command line:

| Argument       | Type   | Required | Description                                                                 |
|----------------|--------|----------|-----------------------------------------------------------------------------|
| `--dataset_path` | str   | Yes      | Path to the dataset JSON file containing the full data.                     |
| `--scores_path`  | str   | Yes      | Path to the scores JSON file containing average scores for each data item.  |
| `--output_path`  | str   | Yes      | Path where the filtered subset will be saved as a JSON file.               |
| `--threshold`    | float  | Yes      | The score thresholds used to filter the data. |

#### Example Command

To run the script, use the following format:
```bash
python select.py --dataset_path <path_to_dataset> --scores_path <path_to_scores> --output_path <output_file_path> --threshold <threshold>
```

#### Output Files

After execution, the script generates the following output:

**subset.json**: A JSON file located at the specified `output_path`, containing the filtered subset of data.
