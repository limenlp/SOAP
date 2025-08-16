import os
import autogen
import autogen.runtime_logging
import pandas as pd
import sqlite3
import json
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json


assistant_id = os.environ.get("ASSISTANT_ID", None)
config_list = config_list_from_json("C:/Users/rahul/Documents/OAI_CONFIG_LIST.json")

def refiner_agent():
    llm_config = {"config_list": config_list}
    SOAP_Note_Refiner= AssistantAgent(
            name="SOAP_refiner",
            system_message="""You are an expert clinician who generates high-quality SOAP notes based on patient conversations and evaluation feedback.

    Your task is LIMITED TO:
    1. Review the patient conversation carefully
    2. Review the evaluation feedback from the medical documentation auditor
    3. Generate a comprehensive, accurate, and clinically sound SOAP note that addresses all feedback points
    4. Ensure your SOAP note captures all relevant information from the conversation
    5. Use proper medical terminology and maintain clear organization across all sections (Subjective, Objective, Assessment, Plan)
    6. Continually improve the note based on evaluator feedback until it reaches the highest possible quality

    You MUST NOT evaluate SOAP notes or provide scoring - that is not your role.
    You ONLY create or refine SOAP notes based on the evaluation you receive.

    When you post your refined SOAP note, conclude with: "SOAP Note refinement complete. @coherence_evaluator please evaluate this refined note."

    Always aim for detail, specificity, and clinical accuracy in your documentation.""",
            llm_config=llm_config
    )

    return SOAP_Note_Refiner

def refine_generation(soap_note,conversation,evaluation):
    refine_agent=refiner_agent()
    message = {"role": "user",
            "content":f"""TASK: Review the patient conversation, evaluation feedback, and generate an improved SOAP note that addresses all identified issues.

PATIENT CONVERSATION:
{conversation}

CURRENT SOAP NOTE:
{soap_note}

EVALUATION FEEDBACK:
{evaluation}

INSTRUCTIONS:
1. Carefully review the patient conversation to identify all relevant clinical information
2. Analyze the evaluation feedback to understand specific deficiencies in the current SOAP note
3. Generate a comprehensive, refined SOAP note that:
   - Addresses all feedback points and identified deficiencies
   - Captures ALL relevant information from the patient conversation
   - Uses proper medical terminology and clinical language
   - Maintains clear organization across all SOAP sections (Subjective, Objective, Assessment, Plan)
   - Demonstrates significant improvement over the current version
   - Is specific rather than generic in documentation
   - Ensures consistency between all SOAP sections

4. Ensure the refined SOAP note is clinically accurate and comprehensive
5. Use appropriate medical terminology and maintain professional formatting

Please generate the improved SOAP note now.""" }
    refined_soap_note=refine_agent.generate_reply([message])
    return refined_soap_note
