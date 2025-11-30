"""
tools.py
========

Deterministic financial calculation utilities for the Goal Quantification Agent.

This module exposes pure-Python helper functions that perform **non-LLM**
numeric calculations required by the orchestration pipeline.

Current scope:
--------------
- `goal_future_value_calculator`: Computes the **inflation-adjusted future value (FV)**
  of a goal using the standard compound-interest formula:

      FV = PV * (1 + i) ** n

  where:
      PV = present value (current goal amount),
      i  = annual inflation rate (default: 6%),
      n  = number of years until the goal.

The returned structure is designed to be dropped directly into the
Financial State Object (FSO) under the key `"quantification_data"`.
"""

from typing import Dict


def goal_future_value_calculator(
    present_value: float,
    timeline_years: float,
    inflation_rate: float = 0.06,
) -> Dict[str, float]:
    """
    Compute the inflation-adjusted future value (FV) of a financial goal.

    This function is intended to be used as an ADK tool by the
    Goal Quantification Agent. It performs deterministic math only
    (no LLM calls, no side effects).

    Formula:
        FV = PV * (1 + i) ** n

    Args:
        present_value (float):
            The current goal amount (PV) in currency units
            (e.g., today's required corpus for a goal).
        timeline_years (float):
            The time horizon in years (n) until the goal.
        inflation_rate (float, optional):
            Annual inflation rate (i) expressed as a decimal.
            Defaults to 0.06 (i.e., 6% per year).

    Returns:
        Dict[str, float]:
            A dictionary formatted to be stored under
            `FSO["quantification_data"]`, with keys:

                - "present_value":
                    The input PV.
                - "inflation_rate_assumed":
                    The inflation rate used for the calculation.
                - "timeline_years":
                    The time horizon in years.
                - "future_value_required":
                    The computed inflation-adjusted future value (FV).

    Notes:
        - The function assumes non-negative values for `present_value`
          and `timeline_years`. It does not enforce validation; that
          should be handled upstream (e.g., in the SMART Goal agent).
        - The result is deterministic and does not depend on any
          external state.
    """
    # Basic safety: coerce negative or weird values as-is; upstream
    # agents are responsible for validation / guarding against bad input.
    fv = present_value * (1 + inflation_rate) ** timeline_years

    return {
        "present_value": float(present_value),
        "inflation_rate_assumed": float(inflation_rate),
        "timeline_years": float(timeline_years),
        "future_value_required": float(fv),
    }