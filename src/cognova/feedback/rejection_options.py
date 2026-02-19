"""Structured rejection options for the feedback system.

Manages the predefined rejection option master list.
Provides code-based filtering (runs rules/engine.py on rejected test)
and LLM fallback for unmatched or "Other" free-text classification.

Related: feedback/storage.py, feedback/patterns.py, rules/engine.py
"""

__all__ = ["RejectionOptions", "get_filtered_options", "classify_other"]
