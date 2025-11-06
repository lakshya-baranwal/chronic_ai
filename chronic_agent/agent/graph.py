from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.router import route_analysis

# Import all nodes
from agent.nodes.analysis import analyze_data
from agent.nodes.generation import generate_patient_message, generate_doctor_alert
from agent.nodes.actions import dispatch_notifications, save_report_to_file

def create_agent_graph():
    """
    Creates and returns the compiled LangGraph agent.
    """
    workflow = StateGraph(AgentState)

    # 1. Add nodes
    workflow.add_node("analyze_data", analyze_data)
    workflow.add_node("generate_doctor_alert", generate_doctor_alert)
    workflow.add_node("save_report_to_file", save_report_to_file)
    workflow.add_node("generate_patient_message", generate_patient_message)
    workflow.add_node("dispatch_notifications", dispatch_notifications)

    # 2. Set entry point
    workflow.set_entry_point("analyze_data")

    # 3. Add conditional router
    workflow.add_conditional_edges(
        "analyze_data",
        route_analysis,
        {
            "escalate_to_doctor": "generate_doctor_alert",
            "notify_patient_only": "generate_patient_message"
        }
    )

    # 4. Add normal edges
    workflow.add_edge("generate_doctor_alert", "save_report_to_file")
    workflow.add_edge("save_report_to_file", "generate_patient_message")
    workflow.add_edge("generate_patient_message", "dispatch_notifications")
    workflow.add_edge("dispatch_notifications", END)

    # 5. Compile
    app = workflow.compile()
    return app

# Expose the compiled app
app = create_agent_graph()