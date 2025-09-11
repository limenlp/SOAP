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

def presence_agent():
    return autogen.AssistantAgent(
        name="check_presence",
        system_message="You are an expert clinician who specializes in analyzing SOAP notes for documentation of communication breakdowns and patient-AI interactions",
        llm_config=llm_config
    )

def check_presence(instances, soap_note):
    instance_agent = presence_agent()
    message = {"role": "user",
            "content": f"""TASK: Count all reference instances of communication breakdown or Alexa interactions documented in the OBJECTIVE section of this SOAP note.

SOAP NOTE:
{soap_note}

REFERENCE INSTANCES TO LOOK FOR:
{instances}

INSTRUCTIONS:
1. Focus ONLY on the OBJECTIVE section of the SOAP note
2. Count each documented instance of:
   - Communication breakdown between patient and Alexa
   - Any interaction with Alexa (successful or failed)
   - Technology-related communication issues
3. Return your answer in this exact format:
   - Total instances found: [number]
   - Details: [list each instance found with brief description]

IMPORTANT: Only count instances that are explicitly documented in the OBJECTIVE section and are part of the REFERENCE INSTANCES to look for. Do not infer or add instances not mentioned in the documentation."""}

    instance_result = instance_agent.generate_reply([message])
    return instance_result