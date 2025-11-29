# Goal Quantification Agent — README

## 📌 Overview

The **Goal Quantification Agent** is Step 2 in the financial planning pipeline.  
It reads the client's SMART Goal from the FSO (Financial State Object), applies a fixed **6% inflation rate**, and computes the **Future Value (FV)** using:

```
FV = PV * (1 + i)^n
```

Where:

- `PV` = Present goal amount
- `i` = 0.06 (6% inflation assumption)
- `n` = Time frame in years

The agent updates the FSO by adding a new block: `quantification_data`.

---

## 🎯 Responsibilities

### Extracts From FSO

Reads from:

```
FSO["smart_goal_data"]["amount"]
FSO["smart_goal_data"]["time_frame"]
```

### Performs FV Calculation

Deterministic computation via LLM:

- Applies 6% inflation
- Computes the future expected cost of the goal
- Creates a structured summary

### Updates FSO

Adds:

```
"quantification_data": {
    "present_value": PV,
    "inflation_rate_assumed": 0.06,
    "timeline_years": n,
    "future_value_required": FV
}
```

### Output Requirements

- Must return **only** the updated `financial_state_object`
- No explanations, greetings, or extra text
- No tools used — pure LLM computation

---

## 🧠 Example

If:

- PV = ₹10,00,000
- n = 10 years

Then FV:

```
FV = 1000000 * (1.06)^10 ≈ 17,90,847.42
```

FSO receives:

```
"quantification_data": {
  "present_value": 1000000,
  "inflation_rate_assumed": 0.06,
  "timeline_years": 10,
  "future_value_required": 1790847.42
}
```

---

## 🧩 Agent Definition

```python
goal_quantification_agent_tool = Agent(
    model='gemini-2.5-flash',
    name='goal_quantification_agent',
    description='Calculates the Future Value (FV) of the client's goal using a 6% inflation assumption.',
    instruction=optimized_instruction,
    tools=[],
    output_key="financial_state_object"
)
```

---

## 📂 File Purpose

Use this agent immediately after SMART Goal creation to pass inflation-adjusted values to all downstream agents like:

- Budget Optimizer
- Asset Allocation Agent
- Scenario Modeling Agent

---

## ✨ Notes

- Completely deterministic
- No user interaction
- Designed for ADK multi-agent orchestration
- Supports clean, pipeline-friendly FSO updates
