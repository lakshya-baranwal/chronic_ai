import sys
import os
import json
from dotenv import load_dotenv

# Add the project root directory to the Python import path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)

# --- IMPORT FROM THE NEW LOCATION ---
from agent.utils import load_patient_data 
from agent.graph import app 

def run_agent_test():
    load_dotenv()
    
    print("===================================")
    patient_id = input("Please enter the Patient ID (e.g., patient_01): ")
    print("===================================")
    
    # Load patient data
    patient_profile, full_data_stream = load_patient_data(patient_id)
    
    if not patient_profile or not full_data_stream:
        print(f"--- Agent run failed: Could not load data for '{patient_id}'. ---")
        return

    # Define the inputs
    inputs = {
        "patient_profile": patient_profile,
        "full_data_stream": full_data_stream
    }
    
    print(f"RUNNING HEALTH AGENT FOR: {patient_profile.get('name', patient_id)}")
    print("===================================")

    # Run the agent
    for output in app.stream(inputs):
        node_name = list(output.keys())[0]
        print(f"\n--- Output from Node: {node_name} ---")
    
    print("\n===================================")
    print("AGENT RUN COMPLETE")
    print("===================================")

if __name__ == "__main__":
    run_agent_test()
    