import json
from agent.state import AgentState
from agent.llm import get_llm
from agent.prompts import ANALYZE_DATA_TREND_PROMPT
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.json import JsonOutputParser

def analyze_data(state: AgentState):
    """
    Node 1: Analyzes the full patient data stream.
    """
    print("--- Node: analyze_data ---")
    
    llm = get_llm()
    prompt_template = ChatPromptTemplate.from_template(ANALYZE_DATA_TREND_PROMPT)
    parser = JsonOutputParser()
    chain = prompt_template | llm | parser

    full_history = state['full_data_stream']
    todays_data = full_history[-1] # Today is the last item
    
    full_data_stream_json = json.dumps(full_history, indent=2)
    
    response = chain.invoke({
        "patient_profile": state['patient_profile'],
        "full_data_stream_json": full_data_stream_json
    })
    
    return {
        "todays_data": todays_data, 
        "analysis_decision": response['decision'],
        "analysis_reasoning": response['reasoning']
    }