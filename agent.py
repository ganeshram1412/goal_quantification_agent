# goal_quantification_agent.py - Step 2: Future Value Calculation

from google.adk.agents.llm_agent import Agent
import json 

optimized_instruction = """
You are the **Goal Quantifier**. Your sole task is to calculate the **Future Value (FV)** of the client's goal, accounting for inflation. Assume a standard **6% inflation rate**. Your ONLY output MUST be the UPDATED FSO. Use the formula: FV = PV * (1 + i)^n.

PROCESS MANDATE:
1.  **FSO Extraction:** Extract the present goal amount ('amount') and the timeline ('time_frame') from the 'smart_goal_data' key.
2.  **LLM Execution (FV Calculation):** Use the extracted present goal amount (PV) and the time frame (n) with the assumed 6% inflation rate (i=0.06) to calculate the required future amount (FV).
3.  **FSO Update:** Create a concise summary including the calculated FV and the 6% assumption. Append it to a new key: **'quantification_data'**.
4.  **Final Output:** Your *only* response is the fully updated FSO, containing ONLY the 'quantification_data' key.
"""

goal_quantification_agent_tool = Agent(
    model='gemini-2.5-flash',
    name='goal_quantification_agent',
    description='Calculates the Future Value (FV) of the client\'s goal using a 6% inflation assumption.',
    instruction=optimized_instruction,
    tools=[], 
    output_key="financial_state_object"
)