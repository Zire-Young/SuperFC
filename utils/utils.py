#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：FC_data_selector 
@File    ：utils.py
@IDE     ：PyCharm 
@Author  ：young
@Date    ：2024/10/21 19:12
'''
import re
import time
from openai import OpenAI
from utils.gpt_api import get_answer

def extract_number(s):
    # Use regular expressions to match numbers
    match = re.findall(r'\d+', s)
    if match:
        return [int(x) for x in match]
    return None

def get_answer_robustly(prompt):
    try:
        response = get_answer(prompt)
        return response
    except Exception as e:
        print("API call failed, the program will sleep for one minute and then retry:", e)
        time.sleep(60)
        return get_answer_robustly()