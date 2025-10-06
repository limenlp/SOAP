import os
import autogen
import autogen.runtime_logging
import pandas as pd
import sqlite3
import json
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json


def presence_agent(llm_config):
    return autogen.AssistantAgent(
        name="check_presence",
        system_message="You are an expert clinician who specializes in analyzing SOAP notes for documentation of communication breakdowns and patient-AI interactions",
        llm_config=llm_config
    )

def check_presence(instances, soap_note,llm_config):
    instance_agent = presence_agent(llm_config)
    message = {"role": "user",
            "content": f"""TASK: Count all instances of patient-AI interactions from the conversation  from the OBJECTIVE section of this SOAP note.

SOAP NOTE:
{soap_note}

INSTANCES TO LOOK FOR:
{instances}

INSTRUCTIONS:
1. Focus ONLY on the OBJECTIVE section of the SOAP note
2. Count each documented instance of:
   - Communication breakdown between patient and Alexa
   - Any interaction with AI (successful or failed)
   - Technology-related communication issues
3. Return your answer in this exact format:
   - Total instances found: [number]
   - Details: [list each instance found with brief description]

IMPORTANT: Only count instances that are explicitly documented in the OBJECTIVE section and are part of the INSTANCES to look for. Do not infer or add instances not mentioned in the documentation."""}

    instance_result = instance_agent.generate_reply([message])
    return instance_result