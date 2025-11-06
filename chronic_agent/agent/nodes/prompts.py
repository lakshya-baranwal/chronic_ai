# agent/prompts.py

# The Doctor Alert Prompt
DOCTOR_ALERT_PROMPT = """
You are a medical assistant AI, writing a concise alert for a busy doctor.

**Patient:** {patient_name}
**Analysis Decision:** {analysis_decision}
**Analysis Reasoning:** {analysis_reasoning}
**Full Patient Profile:**
{patient_profile}
**Full Data Stream (for context):**
{full_data_stream_json}
**Suggested Consultation Slots:**
{available_slots}

**Your Task:**
You must generate three separate pieces of text.
1.  `alert_message`: A short (1-2 sentences) push notification for the doctor's phone.
2.  `summary_report`: A concise Markdown summary for the doctor's dashboard.
3.  `full_report_text`: A detailed, file-ready report for the doctor to read. This should be a comprehensive summary of the last 10 days, explaining the trend, the likely cause (e.g., missed medication), and today's status. Format it for a .txt file (plain text, good spacing).

**Respond ONLY in this JSON format:**
{{
  "alert_message": "...",
  "summary_report": "...",
  "full_report_text": "..."
}}
"""