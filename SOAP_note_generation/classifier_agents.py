import os
import autogen
import autogen.runtime_logging
import pandas as pd
import sqlite3
import json
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

def multi_class_classifier(llm_config,system_prompt):
    return autogen.AssistantAgent(
        name="multi_classifier",
        system_message=system_prompt,
        llm_config=llm_config
    )

def multi_class_classification(conversation,example,llm_config,system_prompt):
    classifier_agent=multi_class_classifier(llm_config,system_prompt)
    message = {"role": "user",
            "content":f"""CONVERSATION: {conversation}
CATEGORIES OF COMMUNICATION BREAKDOWN WITH EXAMPLES: {example}
Instructions:
Analyze all patient-AI interactions. Evaluate entire communication patterns, not single lines. Identify both successful interactions and breakdowns using the provided categories.
Output:
Successful #[X]: [Evidence] - [Context]
Breakdown #[X]: [Category] - [Evidence] - [Context]

"""}

    classification_result=classifier_agent.generate_reply([message])
    return classification_result
