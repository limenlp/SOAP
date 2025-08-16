import os
import autogen
import autogen.runtime_logging
import pandas as pd
import sqlite3
import json
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json


assistant_id = os.environ.get("ASSISTANT_ID", None)
config_list = config_list_from_json("C:/Users/rahul/Documents/OAI_CONFIG_LIST.json")
llm_config = {"config_list": config_list,"temperature":0}

def multi_class_classifier(example):
    return autogen.AssistantAgent(
        name="multi_classifier",
        system_message=f"You are an expert clinician specializing in identifying the different categories of conversation breakdown from the followng examples: {example}. Only classify from the entire conversation instance and do not single out a line",
        llm_config=llm_config
    )

def multi_class_classification(conversation,example):
    classifier_agent=multi_class_classifier(example)
    message = {"role": "user",
            "content":f"""TASK: Review the patient conversation and identify the multiple classes of communication breakdown from the categories and 
            respective examples given below:
            
            CONVERSATION:
            {conversation}

            EXAMPLE:
            {example}
        Give me all  instances of communication breakdown within the conversation transcript along with the category it belongs to. Keep in mind, it should only be the direct or indirect conversation between the patient and Alexa that should be categorized.
        Also look at the entire communication between the patient and Alexa before classifying it for breakdown. Don't just classify it because of one line. If there is no requirement for a classification, do not classify.

"""}

    classification_result=classifier_agent.generate_reply([message])
    return classification_result

def syntactic_classifier(example):
    return autogen.AssistantAgent(
        name="syntactic_classifier",
        system_message=f"You are an expert clinician specializing in identifying the different categories of conversation breakdown from the followng examples: {example}. Only classify from the entire conversation instance and do not single out a line",
        llm_config=llm_config
    )
