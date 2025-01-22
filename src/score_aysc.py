#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：FC_data_selector 
@File    ：score_aysc.py
@IDE     ：PyCharm 
@Author  ：young
@Date    ：2024/10/14 14:55
'''
import concurrent
import json
import argparse
import time
import os
import logging
from utils.utils import get_answer, extract_number
from utils.constants import SYSTEM_PROMPT, API_RETRY_DELAY, MAX_WORKERS


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ScoreEvaluator:
    def __init__(self, dataset_path, model, output_path):
        self.dataset_path = dataset_path
        self.model = model
        self.output_path = output_path

    def load_data(self):
        try:
            if not os.path.exists(self.dataset_path):
                raise FileNotFoundError(f"Dataset file not found: {self.dataset_path}")
            with open(self.dataset_path, 'r', encoding='utf-8') as file:
                self.dataset = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Error loading dataset: {e}")
            raise

    def get_single_score(self, data):
        prompt = SYSTEM_PROMPT.format(data=data)
        while True:
            try:
                response = get_answer(prompt)
                break
            except Exception as e:
                logging.error(f"API call failed, the program will sleep for {API_RETRY_DELAY} seconds and then retry: {e}")
                time.sleep(API_RETRY_DELAY)

        log = f"id:{data['id']}\ninput:" + prompt + f"\noutput:{response}\n\n"
        logging.info(f"log_by_{self.model}:\n{log}")
        with open(f"{self.output_path}/logs/score_log_by_{self.model}.txt", "a", encoding="utf-8") as f:
            f.write(log)

        return response, data

    def get_scores_from_model(self):
        scores = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(self.get_single_score, data): data for data in self.dataset}
            for future in concurrent.futures.as_completed(futures):
                try:
                    response, data = future.result()
                    score = extract_number(response.split("\n")[0])
                    if score is not None:
                        scores.append({
                            "id": data["id"],
                            "scores": score,
                            "avg_score": sum(score) / len(score)
                        })
                except Exception as e:
                    logging.error(f"An error occurred: {e}")
        return scores

    def save_results(self, scores):
        try:
            logging.info(f"Saving scores to {self.output_path}/score_by_{self.model}.json")
            with open(f'{self.output_path}/score_by_{self.model}.json', 'w', encoding='utf-8') as file:
                json.dump(scores, file, ensure_ascii=False, indent=4)

            logging.info(f"Updating dataset with scores and saving to {self.output_path}/xlam_60k_with_score_by_{self.model}.json")
            for data in self.dataset:
                data[f"score_by_{self.model}"] = scores[data["id"]]["avg_score"]
            with open(f'{self.output_path}/xlam_60k_with_score_by_{self.model}.json', 'w', encoding='utf-8') as file:
                json.dump(self.dataset, file, ensure_ascii=False, indent=4)
        except Exception as e:
            logging.error(f"Error saving results: {e}")
            raise

    def main(self):
        try:
            self.load_data()
            logging.info(f"Dataset length: {len(self.dataset)}")

            logging.info(f"Scoring with {self.model}...")
            scores = self.get_scores_from_model()
            scores.sort(key=lambda x: x["id"], reverse=False)

            self.save_results(scores)
            logging.info(f"{self.model} scoring completed!")
        except Exception as e:
            logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Score AI assistant responses based on given criteria.")
    parser.add_argument('--dataset_path', type=str, required=True, help='Path to the dataset JSON file.')
    parser.add_argument('--model', type=str, required=True, help='Model name for scoring.')
    parser.add_argument('--output_path', type=str, required=True, help='Path to the output directory.')
    args = parser.parse_args()

    # Verify that the output path exists, create it if it doesn't
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)
        logging.info(f"Created output directory: {args.output_path}")

    evaluator = ScoreEvaluator(args.dataset_path, args.model, args.output_path)
    evaluator.main()
