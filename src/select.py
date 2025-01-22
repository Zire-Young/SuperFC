#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：FC_data_selector 
@File    ：select.py
@IDE     ：PyCharm 
@Author  ：young
@Date    ：2024/10/21 9:36
'''
import json
import argparse
import os
import logging
from utils.constants import THRESHOLD

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataSelector:
    def __init__(self, dataset_path, scores_path, output_path, thresholds):
        self.dataset_path = dataset_path
        self.scores_path = scores_path
        self.output_path = output_path
        self.thresholds = thresholds

    def load_data(self):
        try:
            if not os.path.exists(self.dataset_path):
                raise FileNotFoundError(f"Dataset file not found: {self.dataset_path}")
            with open(self.dataset_path, "r", encoding="utf-8") as f:
                self.dataset = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Error loading dataset: {e}")
            raise

        try:
            if not os.path.exists(self.scores_path):
                raise FileNotFoundError(f"Scores file not found: {self.scores_path}")
            with open(self.scores_path, "r", encoding="utf-8") as f:
                self.data_scores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Error loading scores: {e}")
            raise

    def select_subset(self):
        self.subset = []
        self.scores = [0] * (len(self.thresholds) + 1)  # Add an extra bin for scores == 10

        for item in self.data_scores:
            score = item["avg_score"]
            for i, threshold in enumerate(self.thresholds):
                if i == 0 and score <= threshold:
                    self.scores[i] += 1
                    break
                elif i == len(self.thresholds) - 1 and score > self.thresholds[i]:
                    if score >= THRESHOLD:
                        self.subset.append(self.dataset[item["id"]])
                        self.scores[i + 1] += 1
                    else:
                        self.scores[i] += 1
                    break
                elif threshold < score <= self.thresholds[i + 1]:
                    self.scores[i + 1] += 1
                    break

    def save_results(self):
        try:
            logging.info(f"Scores: {self.scores}")
            logging.info(f"Subset length: {len(self.subset)}")
            with open(self.output_path, "w", encoding="utf-8") as f:
                json.dump(self.subset, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logging.error(f"Error saving results: {e}")
            raise

    def main(self):
        try:
            self.load_data()
            self.select_subset()
            self.save_results()
        except Exception as e:
            logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Select a subset of data based on scores.")
    parser.add_argument('--dataset_path', type=str, required=True, help='Path to the dataset JSON file.')
    parser.add_argument('--scores_path', type=str, required=True, help='Path to the scores JSON file.')
    parser.add_argument('--output_path', type=str, required=True, help='Path to the output JSON file.')
    parser.add_argument('--thresholds', type=float, nargs='+', required=True, help='List of score thresholds.')
    args = parser.parse_args()

    # Validate the thresholds list
    if len(args.thresholds) < 1 or not all(args.thresholds[i] < args.thresholds[i + 1] for i in range(len(args.thresholds) - 1)):
        logging.error("Thresholds must be a non-empty list in ascending order.")
        exit(1)

    selector = DataSelector(args.dataset_path, args.scores_path, args.output_path, args.thresholds)
    selector.main()
