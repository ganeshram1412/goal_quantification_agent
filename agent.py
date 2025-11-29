"""
goal_quantification_agent.py
============================

This module defines the **Goal Quantification Agent**, responsible for Step 2 
in the multi-agent financial planning pipeline. Its function is to compute the 
inflation-adjusted **Future Value (FV)** of the client’s stated goal using a 
fixed 6% inflation assumption, and then update the Financial State Object (FSO) 
accordingly.

---------------------------------------------------------------------------
AGENT ROLE
---------------------------------------------------------------------------

The Goal Quantification Agent reads the client's goal details from the FSO, 
performs deterministic financial calculations, and outputs the updated FSO 
containing a new block called ``quantification_data``.

This ensures that downstream agents (budgeting, asset allocation, scenario 
modeling, etc.) work with realistic, inflation-adjusted goal values.

---------------------------------------------------------------------------
INPUT (from FSO)
---------------------------------------------------------------------------

The agent extracts the following fields from:
    FSO["smart_goal_data"]

- ``amount`` (Present Value — PV)
- ``time_frame`` (Number of years — n)

These fields must be populated by the SMART Goal Agent.

---------------------------------------------------------------------------
CALCULATION LOGIC
---------------------------------------------------------------------------

The agent uses the standard future value formula:

    FV = PV * (1 + i)^n

Where:
    PV = Present value (goal amount)
    i  = 0.06 (6% annual inflation rate; non-negotiable)
    n  = Goal timeline in years

The calculation must be performed by the LLM with no external tools.

---------------------------------------------------------------------------
OUTPUT (updated FSO)
---------------------------------------------------------------------------

The agent creates and inserts a new block:

    "quantification_data": {
        "present_value": <PV>,
        "inflation_rate_assumed": 0.06,
        "timeline_years": <n>,
        "future_value_required": <FV>
    }

No conversational text should be added.  
The final output MUST be the updated FSO JSON only.

---------------------------------------------------------------------------
CONSTRAINTS
---------------------------------------------------------------------------

- No direct user interaction.
- No greetings, explanations, or commentary in the final output.
- No tools are used; the LLM performs only extraction + mathematical reasoning.
- Output **must only** be the updated ``financial_state_object``.

---------------------------------------------------------------------------
USAGE
---------------------------------------------------------------------------

This agent is instantiated as:

    goal_quantification_agent_tool = Agent(
        model='gemini-2.5-flash',
        name='goal_quantification_agent',
        description='Calculates the Future Value (FV) of the client\'s goal using a 6% inflation assumption.',
        instruction=optimized_instruction,
        tools=[],
        output_key="financial_state_object"
    )

This agent is typically invoked immediately after SMART Goal creation as part 
of your orchestrated ADK workflow.
"""

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