import streamlit as st
import config
from engine import stream_prospectus

st.set_page_config(page_title="AI Prospectus Generator", page_icon="🏢")
st.title("🏢 Intelligent Company Prospectus Generator")

# User Inputs
company_name = st.text_input("Company Name", value="")
target_url = st.text_input("Target Website URL", value="")

col1, col2 = st.columns(2)
with col1:
    provider = st.selectbox("LLM Provider", ["OpenAI", "Gemini", "Ollama"])
with col2:
    tone = st.selectbox("Tone", ["Professional", "Snarky/Humorous"])

# Automatically lock the model based on the selected provider
if provider == "OpenAI":
    selected_model = config.DEFAULT_OPENAI_MODEL
elif provider == "Gemini":
    selected_model = config.DEFAULT_GEMINI_MODEL
else:
    selected_model = config.DEFAULT_OLLAMA_MODEL

# Display locked model name in a disabled field so the user can see it but cannot edit it
st.text_input("Model Name", value=selected_model, disabled=True)

if st.button("Generate Prospectus"):
    if not target_url or not company_name:
        st.error("Please enter both a company name and URL.")
    else:
        st.info(f"Analyzing {target_url} using {provider} ({selected_model})...")
        report_placeholder = st.empty()
        full_response = ""
        
        # Stream output in real-time
        for chunk in stream_prospectus(
            company_name=company_name, 
            url=target_url, 
            tone=tone, 
            provider=provider, 
            model=selected_model
        ):
            full_response += chunk
            report_placeholder.markdown(full_response)