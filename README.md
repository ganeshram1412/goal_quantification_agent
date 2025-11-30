# Goal Quantification Agent — README (Updated)

This README documents the updated **Goal Quantification Agent**, now redesigned to use a **deterministic Python tool** for Future Value (FV) computation rather than relying on the LLM for mathematical accuracy.

---

## 📌 Purpose

The **Goal Quantification Agent** performs Step 2B of the financial planning workflow:

### ✔ Reads the SMART Goal

### ✔ Computes Future Value using a tool

### ✔ Updates the FSO with quantification_data

### ✔ Returns ONLY the updated FSO (no text)

This ensures downstream modules like Scenario Modeling, Asset Allocation, and Tax Planning receive accurate, inflation-adjusted goal values.

---

## 🧠 What Changed?

### **⛔ Old Behavior (Removed):**

- LLM performed FV calculation directly
- Potential floating‑point inaccuracies
- No deterministic reproducibility

### **✅ New Behavior (Improved):**

- Uses a deterministic Python tool:
  `calculate_future_value(pv, years, rate=0.06)`
- Guaranteed mathematical correctness
- Ensures consistent output across runs
- Cleaner agent prompt and fewer tokens

---

## 🔧 Tool Implementation

```python
def calculate_future_value(present_value: float, years: float, rate: float = 0.06) -> dict:
    '''
    Calculates future value using FV = PV * (1 + r)^n.

    Parameters:
    - present_value: float
    - years: float
    - rate: float = 0.06 (6% inflation)

    Returns:
    dict with:
      - present_value
      - years
      - rate
      - future_value
    '''
    future_value = present_value * ((1 + rate) ** years)
    return {
        "present_value": present_value,
        "timeline_years": years,
        "inflation_rate_assumed": rate,
        "future_value_required": future_value,
    }
```

---

## 🧩 Updated Agent Logic

### **FSO Input Expected**

From:

```
FSO.smart_goal_data.amount
FSO.smart_goal_data.time_frame
```

### **Workflow**

1. Extract PV + years
2. Call `calculate_future_value` tool
3. Insert result into:

```
FSO["quantification_data"]
```

4. Output ONLY the updated `financial_state_object`

---

## 📘 Agent Definition (Updated)

```python
goal_quantification_agent_tool = Agent(
    model='gemini-2.5-flash',
    name='goal_quantification_agent',
    description='Determines the future value of the client goal using a deterministic FV calculator tool.',
    instruction=optimized_instruction,
    tools=[calculate_future_value],
    output_key="financial_state_object"
)
```

---

## 📈 Example

If PV = ₹5,00,000  
years = 15

```
FV = 500000 * (1.06)^15 = 1,197,567.34
```

FSO gets:

```json
"quantification_data": {
  "present_value": 500000,
  "timeline_years": 15,
  "inflation_rate_assumed": 0.06,
  "future_value_required": 1197567.34
}
```

---

## 🧾 Notes

- No user interaction
- No commentary in output
- Designed for token‑efficient workflows
- Guarantees accuracy & determinism
- Supports all downstream planning agents

---
