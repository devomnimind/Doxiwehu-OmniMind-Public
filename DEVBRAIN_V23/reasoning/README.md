# ReAcTree Reasoning

This module implements the **ReAcTree** hierarchical reasoning agent described in Phase 9 Tier 0.
It provides tree-based task decomposition, local ReAct-style execution nodes, and control-flow navigation (sequence, fallback, parallel).
Use `ReAcTreeAgent` for complex goals that benefit from structured subgoals and reusing episodic history recorded in the agent tree.