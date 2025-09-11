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
        system_message=f'''You are an expert clinician analyzing patient-AI interactions. Your task is to extract structured instances of communication between the patient and the AI, focusing on the following **target components**:  
1. **VAT Tools**: Identify references to AI systems (e.g., "Hey Gemini, explain biotechnology") or tools (e.g., "Alexa, set a timer").  
2. **Specific Topics**: Highlight niche subjects (e.g., "Texas Flooding," "mental health," or "biotechnology").  
3. **Structured Models/Visual Supports**: Note instances where the AI uses frameworks (e.g., flowcharts, decision trees) or visual aids (e.g., diagrams, timelines) to structure responses.  
4. **Prompt Revision**: Flag cases where the patient adjusts their query (e.g., "Can you clarify that?") or the AI rephrases for clarity.  

**Guidelines**:  
- **Analyze the entire conversation** to detect patterns spanning multiple exchanges (e.g., a flowchart explanation may span 3-5 lines).  
- **Explicitly map each example to the target components** (e.g., "This instance matches VAT Tools because the patient invoked Gemini").  
- **Quantify divergence** (e.g., "The examples miss 4/5 key elements: VAT tools, structured models, prompt revisions, and specific topics").  
- **Adjust examples to align with the objective** (e.g., "Include a case where the AI uses a flowchart to explain biotechnology").  

**Why this matters**:  
By explicitly linking components to patterns, the LLM can debug mismatches. For instance, if the AI fails to mention a VAT tool like 
Gemini, the system prompt should guide the LLM to recognize this as a gap and suggest adjustments 
(e.g., "Add a scenario where the patient asks Gemini to visualize a biotech process"). 
This ensures the output is actionable, precise, and aligned with the objective of structured, context-aware analysis.''',
        llm_config=llm_config
    )

def multi_class_classification(conversation,example):
    classifier_agent=multi_class_classifier(example)
    message = {"role": "user",
            "content":f"""CONVERSATION: {conversation}
EXAMPLES: {example}
Instructions:
Analyze all patient-Alexa interactions. Evaluate entire communication patterns, not single lines. Identify both successful interactions and breakdowns using the provided categories.
Output:
Successful #[X]: [Evidence] - [Context]
Breakdown #[X]: [Category] - [Evidence] - [Context]

"""}

    classification_result=classifier_agent.generate_reply([message])
    return classification_result
