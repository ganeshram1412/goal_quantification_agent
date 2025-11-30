"""
goal_quantification_agent.py
============================

Goal Quantification Agent (Step 2 of the orchestrated financial planning workflow).

This module defines the `goal_quantification_agent_tool`, an ADK `Agent`
responsible for taking a SMART goal already stored in the Financial State Object
(FSO), calling a deterministic Python tool to compute its **inflation-adjusted
Future Value (FV)**, and writing the result back into the FSO.

High-level responsibilities:
----------------------------
1. Read the input FSO JSON.
2. Extract:
     - `amount`      (present value / PV)
     - `time_frame`  (goal horizon in years / n)
   from `FSO["smart_goal_data"]`.
3. Call the Python tool:
     `goal_future_value_calculator(present_value, timeline_years, inflation_rate=0.06)`
4. Store the returned dictionary into:
     `FSO["quantification_data"]`
5. Output ONLY the **updated FSO JSON** (no narrative, no explanation).

This agent does not:
--------------------
- Interact with the user directly.
- Perform its own math in the prompt.
- Emit any natural language; the orchestrator or summarizer agent will
  handle user-facing explanations.

It is typically invoked immediately after the SMART Goal Agent.
"""

from google.adk.agents.llm_agent import Agent
from .tools import goal_future_value_calculator


# Token-optimized, tool-centric instruction for the agent.
optimized_instruction = """
You are the **Goal Quantifier**. Your ONLY task is to read the FSO, extract the
SMART goal fields, call the tool to compute the inflation-adjusted Future Value (FV),
and return the UPDATED FSO JSON.

===========================
MANDATE
===========================

1. FSO Extraction
   - Read the input Financial State Object (FSO).
   - From FSO["smart_goal_data"], extract:
       - amount       → present_value (PV)
       - time_frame   → timeline_years (n)
   - Do not ask the user anything. You only read and transform FSO.

2. TOOL CALL (Optional)
   - Debt reduction goal don't call the goal_future_value_calculator. Current value and Future value will be same create tool's JSON output accordingly.
   - You MUST NOT compute FV yourself.
   - You MUST call the tool:
       goal_future_value_calculator(
         present_value = PV,
         timeline_years = n,
         inflation_rate = 0.06
       )

3. FSO Update
   - Take the tool's JSON output.
   - Write it into:
       FSO["quantification_data"] = <tool_result>
   - Do NOT remove or alter any other existing keys in the FSO.

4. OUTPUT RULES
   - Your ONLY response is the UPDATED FSO as a JSON object.
   - No explanations, no greetings, no extra text.
   - Do NOT output markdown, bullets, or code fences.
   - Do NOT output anything other than the final FSO JSON.

Final response = updated FSO containing the key "quantification_data".
"""

# ADK Agent definition for use by the orchestrator/root agent.
goal_quantification_agent_tool = Agent(
    model="gemini-2.5-flash",
    name="goal_quantification_agent",
    description=(
        "Reads SMART goal data from the FSO, calls a deterministic tool to "
        "compute the inflation-adjusted future value using a fixed 6% rate, "
        "and writes the result back into the FSO under 'quantification_data'."
    ),
    instruction=optimized_instruction,
    tools=[goal_future_value_calculator],
    output_key="financial_state_object",
)