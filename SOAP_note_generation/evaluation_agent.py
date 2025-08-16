import os
import autogen
import autogen.runtime_logging
import pandas as pd
import sqlite3
import json
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json


assistant_id = os.environ.get("ASSISTANT_ID", None)
config_list = config_list_from_json("C:/Users/rahul/Documents/OAI_CONFIG_LIST.json")


def evaluator_agent(rubric,demo_conversation,demo_SOAP_Note):
    llm_config = {"config_list": config_list}
    coherence_evaluator= AssistantAgent(
        name="coherence_evaluator",
        system_message="""You are an ELITE MEDICAL DOCUMENTATION AUDITOR with 30+ years of experience evaluating SOAP notes using quantitative metrics and rigorous standards. Your evaluation methodology is extremely precise and unforgiving of errors.

EVALUATION RUBRIC:
""" + rubric + """

REFERENCE EXAMPLE (10/10 quality - virtually unattainable perfection):
Conversation: """ + demo_conversation + """
Exemplary SOAP Note: """ + demo_SOAP_Note + """

QUANTITATIVE SCORING METHODOLOGY (MANDATORY):
1. Begin with a maximum potential score of 10 points
2. Calculate and apply these MANDATORY deductions:
   - Each piece of conversation information missing from note: -0.5 points
   - Each piece of information in note not supported by conversation: -1 point
   - Each inconsistency between SOAP sections: -1 point
   - Each instance of vague/generic documentation: -0.5 points
   - Each improper use of medical terminology: -0.5 points
   - Each grammatical or formatting error: -0.25 points

3. Apply these MANDATORY scoring caps:
   - If ANY major clinical inconsistency exists: Maximum score capped at 4/10
   - If ANY SOAP section is missing or severely inadequate: Maximum score capped at 5/10
   - If ANY critical information from conversation is missing: Maximum score capped at 6/10
   - If total deductions exceed 5 points: Maximum score equals (10 - total deductions)

QUALITY METRICS TO CALCULATE:
1. Comprehensiveness: Percentage of relevant conversation details captured (below 80% = automatic cap at 6/10)
2. Accuracy: Number of unsupported statements or contradictions (ANY = automatic -1 point EACH)
3. Coherence: Number of logical disconnects between sections (ANY = automatic -1 point EACH)
4. Specificity: Percentage of documentation using specific rather than generic statements (below 70% = cap at 7/10)

SECTION-SPECIFIC SCORING (S.O.A.P):
- Each section starts with 10 points and receives deductions separately
- Final score cannot exceed the lowest section score +2
- Any section scoring below 5 caps the overall score at 6/10

FINAL SCORE CALCULATION (SHOW YOUR WORK):
SOAP Note Score = MIN(10, 10 - total_deductions, lowest_section_score + 2, all_applicable_caps)
""",
        llm_config=llm_config,
    )
    return coherence_evaluator

def score_generation(soap_note,conversation,rubric,demo_conversation,demo_soap_note):
    coherence_evaluator=evaluator_agent(rubric,demo_conversation,demo_soap_note)
    message = {"role": "user",
            "content": """STRICT QUANTITATIVE EVALUATION REQUIRED: Perform a detailed metric-based assessment of this SOAP note.

Conversation: """ + conversation + """
SOAP Note to evaluate: """ + soap_note + """

MANDATORY ASSESSMENT PROTOCOL:
1. EXTRACTION PHASE: Create a list of all key information points from the conversation transcript
2. VERIFICATION PHASE: Check each point against the SOAP note and mark as present/missing/contradicted
3. METRIC CALCULATION:
   - Count EXACTLY how many points from conversation are missing from the note
   - Count EXACTLY how many statements in the note lack support from conversation
   - Count EXACTLY how many inconsistencies exist between SOAP sections
   - Count EXACTLY how many instances of vague/generic documentation occur
   - Count EXACTLY how many improper terms or formatting issues exist
4. SECTION SCORING:
   - Score each SOAP section (S,O,A,P) individually from 0-10
   - Document specific deductions applied to each section
5. TOTAL DEDUCTIONS: Sum all applicable penalties using the quantitative scoring methodology
6. CAPS APPLICATION: Apply all mandatory scoring caps
7. FINAL CALCULATION: Show your mathematical calculation of the final score

Your evaluation must include all counts, calculations and justifications before the final score.

After all deductions and caps are applied, provide your final rating as a single number from 0-10.
Final Score Calculation:
[SHOW DETAILED CALCULATION]
Rating: """}
    evaluation=coherence_evaluator.generate_reply([message])
    return evaluation


def details_evaluator(breakdown_examples):
    llm_config = {"config_list": config_list,"temperature":0}
    evaluator= AssistantAgent(
        name="details_evaluator",
        system_message=f"""You are an ELITE MEDICAL DOCUMENTATION AUDITOR with 30+ years of experience evaluating 
        SOAP notes using quantitative metrics and rigorous standards. Your evaluation methodology is extremely precise and 
        unforgiving of errors.
SCORE THE SOAP NOTE OUT OF 10 BASED ON HOW MUCH OF THE BREAKDOWN INSTANCES FROM THE CONVERSATION SHOWN BELOW:-
      BREAKDOWN INSTANCES:-
      {breakdown_examples}
ARE PRESENT IN THE SOAP NOTE.
""",
        llm_config=llm_config,
    )
    return evaluator

def score_generation(soap_note,conversation,rubric,demo_conversation,demo_soap_note):
    coherence_evaluator=evaluator_agent(rubric,demo_conversation,demo_soap_note)
    message = {"role": "user",
            "content": """STRICT QUANTITATIVE EVALUATION REQUIRED: Perform a detailed metric-based assessment of this SOAP note.

Conversation: """ + conversation + """
SOAP Note to evaluate: """ + soap_note + """

MANDATORY ASSESSMENT PROTOCOL:
1. EXTRACTION PHASE: Create a list of all key information points from the conversation transcript
2. VERIFICATION PHASE: Check each point against the SOAP note and mark as present/missing/contradicted
3. METRIC CALCULATION:
   - Count EXACTLY how many points from conversation are missing from the note
   - Count EXACTLY how many statements in the note lack support from conversation
   - Count EXACTLY how many inconsistencies exist between SOAP sections
   - Count EXACTLY how many instances of vague/generic documentation occur
   - Count EXACTLY how many improper terms or formatting issues exist
4. SECTION SCORING:
   - Score each SOAP section (S,O,A,P) individually from 0-10
   - Document specific deductions applied to each section
5. TOTAL DEDUCTIONS: Sum all applicable penalties using the quantitative scoring methodology
6. CAPS APPLICATION: Apply all mandatory scoring caps
7. FINAL CALCULATION: Show your mathematical calculation of the final score

Your evaluation must include all counts, calculations and justifications before the final score.

After all deductions and caps are applied, provide your final rating as a single number from 0-10.
Final Score Calculation:
[SHOW DETAILED CALCULATION]
Rating: """}
    evaluation=coherence_evaluator.generate_reply([message])
    return evaluation

def detail_score_generation(soap_note,conversation,breakdown_examples):
    details__evaluator=details_evaluator(breakdown_examples)
    message = {"role": "user",
            "content": """STRICT QUANTITATIVE EVALUATION REQUIRED: Perform a detailed metric-based assessment of this SOAP note.

Conversation: """ + conversation + """
SOAP Note to evaluate: """ + soap_note + """
Breakdown instances in conversation: """+ breakdown_examples + """

Check if the breakdown instances are mentioned in the SOAP Note and evaluate the SOAP Note out of 10 
according to the number of instances mentioned in it
Rating: """}
    evaluation=details__evaluator.generate_reply([message])
    return evaluation
