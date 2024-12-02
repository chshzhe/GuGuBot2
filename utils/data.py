import json

from typing import List

from configs.path_config import TEXT_PATH

fortune: List[dict]
msg_of_day: List[dict]
atri_text: List[dict]
BOOK: List[str]
MORNING: List[str]
NIGHT: List[str]
Vegetables: List[str]

# with open(f"{TEXT_PATH}fortune.json", "r", encoding="utf-8") as file:
#     fortune = json.load(file)["data"]
#
# with open(f"{TEXT_PATH}msg_of_day.json", "r", encoding="utf-8") as file:
#     msg_of_day = json.load(file)["data"]
#
# with open(f"{TEXT_PATH}atri.json", "r", encoding="utf-8") as file:
#     atri_text = json.load(file)

with open(f"{TEXT_PATH}/answerbook/answerbook.json", "r", encoding="utf-8") as file:
    BOOK = json.load(file)
with open(f"{TEXT_PATH}/greeting/morning.json", "r", encoding="utf-8") as file:
    MORNING = json.load(file)
with open(f"{TEXT_PATH}/greeting/night.json", "r", encoding="utf-8") as file:
    NIGHT = json.load(file)
# with open(f"{TEXT_PATH}/sellvegetables/common.txt", "r", encoding="utf-8") as file:
#     Vegetables = file.read().splitlines()
#     Vegetables = list(filter(lambda c: '?' not in c, Vegetables))
