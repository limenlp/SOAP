import os
import autogen
import autogen.runtime_logging
import pandas as pd
import sqlite3
import json
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent

assistant_id = os.environ.get("ASSISTANT_ID", None)
config_list = config_list_from_json("C:/Users/rahul/Documents/OAI_CONFIG_LIST.json")
llm_config = {"config_list": config_list}
def soapnoteagent(rubric,system_prompt):
    clinician= AssistantAgent(
        name="SOAP_clinician",
        system_message=system_prompt,
        llm_config=llm_config,
    )

    return clinician


def single_agent_generation(conversation,rubric,system_prompt):
    clinician=soapnoteagent(rubric,system_prompt)
    message = {"role": "user",
            "content": f'''What would a comprehensive SOAP note look like based strictly on the 
    following conversation between a patient and a clinician: {conversation}, 
    ensuring it includes all relevant details from the conversation and follows the structure and style described in the provided rubric : {rubric}? '''}
    soap_note=clinician.generate_reply([message])
    return soap_note