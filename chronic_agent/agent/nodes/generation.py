import json
from agent.state import AgentState
from agent.llm import get_llm
from agent.prompts import PATIENT_MESSAGE_PROMPT, DOCTOR_ALERT_PROMPT
from agent.tools.calendar import check_doctor_schedule
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.json import JsonOutputParser

def generate_doctor_alert(state: AgentState):
    """
    Node 2 (Conditional): Generates report, alert, and text file content.
    """
    print("--- Node: generate_doctor_alert ---")
    
    slots = check_doctor_schedule(state['patient_profile']['doctor_id'])
    
    llm = get_llm()
    prompt_template = ChatPromptTemplate.from_template(DOCTOR_ALERT_PROMPT)
    parser = JsonOutputParser()
    chain = prompt_template | llm | parser

    response = chain.invoke({
        "patient_name": state['patient_profile']['name'],
        "analysis_decision": state['analysis_decision'],
        "analysis_reasoning": state['analysis_reasoning'],
        "patient_profile": state['patient_profile'],
        "full_data_stream_json": json.dumps(state['full_data_stream'], indent=2),
        "available_slots": slots
    })
    
    return {
        "available_slots": slots,
        "message_to_doctor": response['alert_message'],
        "summary_report": response['summary_report'],
        "doctor_file_report": response['full_report_text']
    }

def generate_patient_message(state: AgentState):
    """
    Node 3: Generates a clear, empathetic message for the patient.
    """
    print("--- Node: generate_patient_message ---")
    
    llm = get_llm()
    prompt_template = ChatPromptTemplate.from_template(PATIENT_MESSAGE_PROMPT)
    parser = JsonOutputParser()
    chain = prompt_template | llm | parser
    
    response = chain.invoke({
        "patient_name": state['patient_profile']['name'],
        "analysis_decision": state['analysis_decision'],
        "analysis_reasoning": state['analysis_reasoning']
    })
    
    return {"message_to_patient": response['message']}