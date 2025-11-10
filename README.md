# 🩺 Chronic AI

## Overview
Our project **"Chronic AI"** is an autonomous agent designed to assist doctors in managing patients with chronic diseases such as diabetes and hypertension, which require consistent tracking of blood pressure, daily activity, and medication adherence.

---

## The Problem
Doctors often struggle with manually tracking long-term data for multiple patients and detecting meaningful trends in their health data.

---

## Our Solution
**"Chronic AI"** acts as a 24/7 digital assistant that continuously analyzes multi-day patient data streams, including:
- Daily vitals (Blood Pressure, Blood Sugar)
- Activity and sleep patterns
- Medication adherence

The core of our system is a stateful GenAI agent built with **FastAPI**, **LangGraph**, and a **Generative AI model**.  
Instead of flagging a single abnormal reading, it identifies long-term patterns and causal correlations in the data.

---

## Example Insights
For example, the agent detects:
- **Negative Trends:** Blood pressure rising steadily for 3+ days  
- **Causal Correlations:** High blood sugar correlating with missed medication  
- **Deviations from Targets:** Activity levels dropping below doctor-set goals

---

## Automated Actions
Based on these insights, the agent automatically:
- Classifies the patient’s condition as **Normal**, **Slight Deviation**, or **Critical**
- Sends personalized, encouraging messages to the patient
- Escalates to the doctor only when a serious trend is confirmed

---

## Reporting
When a critical pattern is detected, Chronic AI generates:
1. **Immediate Alert Reports** for doctors  
2. **Weekly Summary Reports** for long-term patient monitoring

---
Note: This agent was built during the **GenAI Hackathon Multisite Finals** held at **LPCPS, Lucknow**, and organized by **AI Community Lucknow**.

