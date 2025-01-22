#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：FC_data_selector 
@File    ：constants.py
@IDE     ：PyCharm 
@Author  ：young
@Date    ：2024/10/21 19:19
'''

# Constants
PARSE_ERROR_PROMPT_TEMPLATE = '''
You are a professional data analysis expert, the following function call data may have some data quality issues, 
please classify the following data quality issues. There are five analogies to choose from. They are:
1. Wrong understanding of user intent
2. Parameters are missing or wrong
3. Incomplete information
4. The function call does not match the function description
5. Restrictions are not followed

Don't return anything other than the number that corresponds to your classification.
If you think the data doesn't have any of the above five problems, but there are other types of problems, please return 6.
If you think there's nothing wrong with this data, please return 0.

The data you need to process is as follows:
{data}
'''

DIMENSIONS = '''
Alignment with User Intent: The degree to which the response addresses the actual needs and expectations of the user as inferred from the query.
Argument Correction: The ability to correct or refine arguments within the query, if necessary, to ensure accurate and meaningful function calls.
Completeness: Whether the response includes all relevant information and components required for a fully functional call.
Consistency: The consistency of the information provided in the answer with the available tools and any previous interactions.
Adherence to Limitations: Respect for any constraints or limitations specified by the user or inherent in the available tools.
'''

SCORING_PROMPT_TEMPLATE = '''
You are tasked with evaluating the performance of an AI assistant focused on generating function calls in response to user queries.

Please review the following information:

User Query: {data["query"]}
Available Tools: {data["tools"]}
Generated Answers: {data["answers"]}
Evaluate the response based on the following dimensions:

{DIMENSIONS}

Rate the performance on a scale from 0 to 10 for each dimension, where 10 represents the highest level of adherence to the evaluated dimension. Scores should be assigned judiciously, avoiding extremes without clear justification.

Output only the numerical scores separated by commas, ensuring no additional text or bias is introduced.
'''

SYSTEM_PROMPT = SCORING_PROMPT_TEMPLATE.format(DIMENSIONS=DIMENSIONS)

API_RETRY_DELAY = 60  # seconds
MAX_WORKERS = 5
THRESHOLD = 9.5
