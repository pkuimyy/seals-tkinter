import csv
from nltk.metrics.distance import edit_distance
from collections import defaultdict
from tqdm import tqdm
from pprint import pprint
import json
import csv

if __name__ == "__main__":
    raw_target_similarity_path = "../data/clean/raw_target_similarity.csv"
    raw_list_path = "../data/raw/raw_list.txt"
    target_list_path = "../data/raw/target_list.csv"

    raw_list = []
    target_list = []
    with open(raw_list_path, mode="r", encoding="utf-8") as f:
        for line in f.readlines():
            raw_list.append(line.strip())
    with open(target_list_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for line in reader:
            target_list.append(line["学校名称"])

    raw_target_similarity_table = []
    for i, j in tqdm([(i, j) for i in raw_list for j in target_list]):
        if i in j or j in i:
            distance = 1
        else:
            distance = edit_distance(i, j)
        raw_target_similarity_table.append({
            "raw": i,
            "target": j,
            "distance": distance
        })

    with open(raw_target_similarity_path, mode="w", encoding="utf-8", newline="") as f:
        header = ["raw", "target", "distance"]
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        writer.writerows(raw_target_similarity_table)
