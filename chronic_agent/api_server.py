from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn
import datetime
import os
import glob

# Import your agent app and data loader
from agent.graph import app as agent_app
from agent.utils import load_patient_data
from agent.state import AgentState 

# This is the Mount Path from your render.yaml
PERSISTENT_STORAGE_PATH = "/var/data"

# Initialize FastAPI
app = FastAPI(
    title="Chronic AI Health Agent",
    description="An API for running the agentic health monitor."
)

# Load environment variables (like GOOGLE_API_KEY)
load_dotenv()

# Define the input data model for the API request
class PatientRequest(BaseModel):
    patient_id: str

#POST
@app.post("/run_agent", response_model=AgentState)
async def run_agent(request: PatientRequest):
    """
    Run the health agent for a specific patient.
    """
    
    # 1. Load the patient data
    patient_profile, full_data_stream = load_patient_data(request.patient_id)
    
    if not patient_profile or not full_data_stream:
        raise HTTPException(
            status_code=404, 
            detail=f"Patient data not found for ID: {request.patient_id}"
        )

    # 2. Define the agent inputs
    inputs = {
        "patient_profile": patient_profile,
        "full_data_stream": full_data_stream
    }

    print(f"--- API: Running agent for {request.patient_id} ---")
    
    # 3. Run the agent and get the final state
    try:
        final_state = agent_app.invoke(inputs)
    except Exception as e:
        print(f"Agent run failed: {e}")
        raise HTTPException(status_code=500, detail=f"Agent error: {e}")

    print("--- API: Agent run complete ---")
    
    # 4. Return the final state as JSON
    return final_state

# GET
@app.get("/reports/latest_alert/{patient_id}")
async def get_latest_alert_report(patient_id: str):
    """
    Finds the most recent 'doctor_file_report' from the
    persistent disk and returns it.
    """
    
    # 1. Load the patient's profile to get their name
    patient_profile, _ = load_patient_data(patient_id)
    
    if not patient_profile:
        raise HTTPException(
            status_code=404, 
            detail=f"Patient profile not found for ID: {patient_id}"
        )
    
    # 2. Get the patient's first name
    try:
        patient_name = patient_profile.get('name', 'unknown').split(' ')[0]
    except Exception:
        patient_name = "unknown"

    # 3. Find all alert reports on the persistent disk
    report_dir = os.path.join(PERSISTENT_STORAGE_PATH, "doctor_reports")
    search_pattern = os.path.join(report_dir, f"ALERT_{patient_name}_*.txt")
    
    report_files = glob.glob(search_pattern)
    
    if not report_files:
        raise HTTPException(
            status_code=404, 
            detail=f"No alert reports found for patient: {patient_name}"
        )
    
    # 4. Sort the files by modification time and get the newest one
    latest_report = max(report_files, key=os.path.getmtime)
    
    print(f"--- API: Fetching latest report: {latest_report} ---")

    # 5. Return the file
    return FileResponse(
        path=latest_report,
        media_type='text/plain',
        filename=os.path.basename(latest_report)
    )

# This block MUST be at the end of the file
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)