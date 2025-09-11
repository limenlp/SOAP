import re
import statistics


def get_avg_section_scores(loss_list,conversation_list):
    subjective_list=[]
    objective_list=[]
    assessment_list=[]
    plan_list=[]
    for i in range(0,len(conversation_list)):
        text=loss_list[i].value
        subjective_match = re.search(r"\*?\*?\s*Subjective\s*\(S\):\s*\*?\*?\s*(\d+)/\d+", text)
        subjective_score = subjective_match.group(1)
        subjective_list.append(float(subjective_score))
        objective_match = re.search(r'\*?\*?\s*Objective\s*\(O\):\s*\*?\*?\s*(\d+)/\d+', text)
        objective_score = objective_match.group(1)
        objective_list.append(float(objective_score))
        assessment_match = re.search(r'\*?\*?\s*Assessment\s*\(A\):\s*\*?\*?\s*(\d+)/\d+', text)
        assessment_score = assessment_match.group(1)
        assessment_list.append(float(assessment_score))
        plan_match = re.search(r'\*?\*?\s*Plan\s*\(P\):\s*\*?\*?\s*(\d+)/\d+', text)
        plan_score = plan_match.group(1)
        plan_list.append(float(plan_score))
    return statistics.mean(subjective_list),statistics.mean(objective_list),statistics.mean(assessment_list),statistics.mean(plan_list)