import os
from agent.state import AgentState
from datetime import datetime

# This is the Mount Path from your render.yaml
PERSISTENT_STORAGE_PATH = "/var/data"

def save_report_to_file(state: AgentState):
    """
    Node (Conditional): Saves the immediate alert report to the persistent disk.
    Includes a full timestamp to prevent overwrites.
    """
    print("--- Node: save_report_to_file (ALERT) ---")
    
    report_content = state.get("doctor_file_report")
    if not report_content:
        print("No alert report content to save.")
        return {}

    # Write to the persistent disk
    output_dir = os.path.join(PERSISTENT_STORAGE_PATH, "doctor_reports")
    os.makedirs(output_dir, exist_ok=True)
    
    # Get patient name for the file
    patient_name = state['patient_profile'].get('name', 'patient').split(' ')[0]
    
    # We add a full timestamp so files are unique
    date_str = datetime.now().strftime("%Y-%m-%d_%H%M%S") # e.g., 2025-11-06_151200
    filename = f"ALERT_{patient_name}_{date_str}.txt"
    
    filepath = os.path.join(output_dir, filename)
    
    try:
        with open(filepath, "w") as f:
            f.write(report_content)
        print(f"Successfully saved alert report to: {filepath}")
    except Exception as e:
        print(f"Error saving alert report file: {e}")
        
    return {}


def dispatch_notifications(state: AgentState):
    """
    Node: "Sends" all generated messages to the console.
    """
    print("--- Node: dispatch_notifications ---")
    
    # 1. Send message to patient
    patient_message = state['message_to_patient']
    print("=" * 30)
    print(f"MESSAGE TO PATIENT ({state['patient_profile']['name']}):")
    print(patient_message)
    print("=" * 30)

    # 2. Send alert to doctor (if it exists)
    if state.get("message_to_doctor"):
        doctor_message = state['message_to_doctor']
        doctor_report = state['summary_report']
        
        print("\n" + "=" * 30)
        print(f"ALERT TO DOCTOR ({state['patient_profile']['doctor_id']}):")
        print(f"Push Notification: {doctor_message}")
        print("\n--- Dashboard Summary ---")
        print(doctor_report)
        print("\n(Immediate alert .txt report saved to persistent disk)")
        print("=" * 30)
        
    return {}

def save_weekly_summary(state: AgentState):
    """
    Node (Unconditional): Saves the weekly summary to the persistent disk.
    File name format: YYYY_MM_WW_patient_id.txt
    """
    print("--- Node: save_weekly_summary (WEEKLY) ---")
    
    report_content = state.get("weekly_summary_text")
    if not report_content:
        print("No weekly summary content to save.")
        return {}

    # Get data for file naming
    now = datetime.now()
    year = now.year
    month = now.month
    week = now.isocalendar().week 
    patient_id = state['patient_profile'].get('patient_id', 'unknown')
    
    # Build the file name and path
    filename = f"{year}_{month:02d}_{week:02d}_{patient_id}.txt"
    
    # Write to the persistent disk
    output_dir = os.path.join(PERSISTENT_STORAGE_PATH, "patients/reports")
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, filename)
    
    try:
        with open(filepath, "w") as f:
            f.write(report_content)
        print(f"Successfully saved weekly summary to: {filepath}")
    except Exception as e:
        print(f"Error saving weekly summary file: {e}")
        
    return {}