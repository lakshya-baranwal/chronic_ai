from typing import TypedDict, Optional, Dict, Any, List

class AgentState(TypedDict, total=False):
    """
    This TypedDict defines the state that is passed between all nodes in the graph.
    It is the "memory" of the agent.
    """

    patient_profile: Dict[str, Any]
    full_data_stream: List[Dict[str, Any]] # This is the full multi-day data list
    
    # analysis to be filled by analysis node
    todays_data: Dict[str, Any]       # The last item from the list, for convenience
    analysis_decision: str            # The classification: "Normal", "Slight_Deviation", "Repeated_High", "Critical"
    analysis_reasoning: str           # The LLM's justification
    
    # tools output to be filled by generation node
    available_slots: Optional[list[str]] # From calendar tool
    
    # output to be filled by generation nodes 
    message_to_patient: str            # Final message for the patient
    message_to_doctor: Optional[str]   # Final alert for the doctor (if any)
    summary_report: Optional[str]      # Detailed report for the doctor (if any)

    doctor_file_report: Optional[str]