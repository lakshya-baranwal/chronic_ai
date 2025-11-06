from agent.state import AgentState

def route_analysis(state: AgentState):
    """
    This conditional edge decides which path to take after analysis.
    """
    decision = state['analysis_decision'].strip('[]')
    print(f"--- Router: Decision is '{decision}' ---")
    
    if decision in ["Critical", "Repeated_High"]:
        return "escalate_to_doctor"
    else:
        return "notify_patient_only"