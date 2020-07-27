import json
import sqlite3
import csv
import random


class SealsData:
    def __init__(self):
        self.raw_list_file = "./data/raw/raw_list.txt"
        self.target_list_file = "./data/raw/target_list.csv"
        self.pair_list_file = "./data/clean/pair_list.json"
        self.db_file = "./data/seals.db"
        self.raw_list_set = set()
        self.target_list_set = set()
        self.pair_list_dict = {}

        self.load_raw_list()
        self.load_target_list()
        self.load_pair_list()
        self.connect_db()

    def load_target_list(self):
        with open(self.target_list_file, encoding="utf-8", mode="r") as f:
            reader = csv.DictReader(f)
            for item in reader:
                self.target_list_set.add(item["学校名称"])

    def load_raw_list(self):
        with open(self.raw_list_file, encoding="utf-8", mode="r") as f:
            for line in f.readlines():
                self.raw_list_set.add(line.strip())

    def load_pair_list(self):
        with open(self.pair_list_file, encoding="utf-8", mode="r") as f:
            self.pair_list_dict = json.load(f)

    def connect_db(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def query_distance(self, raw):
        sql = (
            "SELECT target,distance FROM raw_target_similarity "
            f"WHERE raw = '{raw}' ORDER BY distance LIMIT 48;"
        )
        # print(sql)
        reader = self.cursor.execute(sql)
        result = []
        for target, distance in reader:
            result.append([target, distance])
        return result

    def close_db(self):
        self.conn.close()

    def pop_raw(self):
        intersection = self.raw_list_set - self.pair_list_dict.keys()
        return random.choice(list(intersection))

    def get_max_text_len(self):
        max = 0
        for raw in self.raw_list_set:
            if len(raw) > max:
                max = len(raw)
        print(max)
        max = 0
        for target in self.target_list_set:
            if len(target) > max:
                max = len(target)
        print(max)

    def save_pair_list(self):
        with open(self.pair_list_file, mode="w", encoding="utf-8")as f:
            json.dump(self.pair_list_dict, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    sd = SealsData()
    tmp = sd.pop_raw()
    print(tmp)
    result = sd.query_distance(tmp)
    print(result)
    sd.close_db()
    sd.get_max_text_len()
