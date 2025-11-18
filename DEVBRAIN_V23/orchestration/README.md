## LangGraph Orchestration

`LangGraphCoordinator` implements the Tier 0 orchestrator described in the Phase 9 Masterplan.
It stitches together planning, criticism, execution, and synthesis nodes using `langgraph`'s `StateGraph`, enabling deterministic control flow backed by a ReAcTree planner and Agentic Memory.
Use this coordinator to execute complex intents with reproducible state transitions, automatic criticism handling, and persistence of synthesized results back into A-MEM.