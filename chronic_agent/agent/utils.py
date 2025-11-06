import os
import json

# Get the project root directory (which is one level up from 'agent/')
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def load_patient_data(patient_id):
    """
    Loads both the profile and data stream for a given patient ID.
    """
    print(f"--- Loading data for patient: {patient_id} ---")
    
    # 1. Load Profile
    profile_path = os.path.join(project_root, 'patients', 'profiles', f"{patient_id}.json")
    try:
        with open(profile_path, 'r') as f:
            patient_profile = json.load(f)
        print(f"Successfully loaded profile from: {profile_path}")
    except FileNotFoundError:
        return None, None
    
    # 2. Load Data Stream
    data_path = os.path.join(project_root, 'patients', 'data', f"{patient_id}.json")
    try:
        with open(data_path, 'r') as f:
            full_data_stream = json.load(f)
        print(f"Successfully loaded data stream from: {data_path}")
    except FileNotFoundError:
        return None, None
        
    return patient_profile, full_data_stream