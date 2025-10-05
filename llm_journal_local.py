"""
Journal Analyzer - Streamlit App

Author: Aditya Wresniyandaka
Date: 2025-10-05
Purpose: Analyze personal journal entries using a local Qwen3:30B model 
         running in an Ollama Podman container inside WSL/Linux, and provide
         actionable insights.

License: MIT License
"""

import streamlit as st
import requests

# -------------------------
# Ollama connection helper
# -------------------------
def query_ollama(model: str, prompt: str) -> str:
    """
    Send prompt to Ollama running locally (Podman/WSL).
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        return f"❌ Error: {e}"

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Journal Analyzer", page_icon="📔")

st.title("📔 Journal Analyzer with Ollama (local)")

st.write(
    "Paste your journal entry below (single day or multi-day). "
    "The LLM will analyze mood, highlights, stressors, and give advice."
)

# Text area for input
journal_text = st.text_area(
    "Your Journal Entry:",
    height=300,
    placeholder="Paste your journal text here..."
)

# Model selection
model_name = st.text_input("Model name", value="qwen3:30b", help="Enter the Ollama model name you want to use.")

# Analysis button
if st.button("Analyze Journal ✨"):
    if not journal_text.strip():
        st.warning("Please paste a journal entry first.")
    else:
        with st.spinner("Analyzing with Ollama..."):
            # 4 prompts in one pass
            prompts = [
                ("Weekly Mood Tracker", 
                 "Analyze this journal text and summarize the overall mood and emotional patterns."),
                ("Work/Study vs. Fun Balance", 
                 "Analyze this journal text. Identify how much time was spent on work/study vs. leisure. Suggest improvements."),
                ("Highlights & Stressors", 
                 "From this journal text, list 3 highlights (positive moments) and 3 stressors (negative moments)."),
                ("Actionable Advice", 
                 "Based on the journal text, suggest 3 concrete habits or strategies for better productivity and well-being.")
            ]

            for title, p in prompts:
                st.subheader(title)
                result = query_ollama(model_name, f"{p}\n\nJournal:\n{journal_text}")
                st.write(result)
