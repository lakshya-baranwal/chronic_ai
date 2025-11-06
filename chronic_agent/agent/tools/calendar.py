def check_doctor_schedule(doctor_id: str) -> list[str]:
    """
    A mock tool to check a doctor's schedule.
    """
    print(f"--- Tool Used: check_doctor_schedule (Doctor ID: {doctor_id}) ---")
    # Mock data
    return [
        "Tomorrow, Nov 7 at 4:00 PM",
        "Friday, Nov 8 at 10:00 AM",
    ]