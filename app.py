import os
import streamlit as st
from google import genai

MODEL = "gemini-3.6-flash"


def configured_key():
    """Retrieve server key, without displaying or logging it."""
    try:
        key = st.secrets.get("GEMINI_API_KEY")
        if key:
            return str(key).strip()
    except (FileNotFoundError, KeyError):
        pass
    return os.environ.get("GEMINI_API_KEY", "").strip()


st.set_page_config(page_title="Gemini Secrets Demo", page_icon="🔐")
st.title("🔐 Gemini Secrets Demo")
st.caption("ATF Challenge · Week 4.2 · Exercise 2")
server_key = configured_key()
if server_key:
    st.success("Server-side Gemini API key configured.")
    user_key = ""
else:
    st.warning("No server-side API key configured.")
    st.info("Only enter your own key in a deployment you control. Never share or log API keys.")
    user_key = st.text_input("Gemini API key", type="password", placeholder="Paste your own key", autocomplete="off")

prompt = st.text_area("Ask Gemini a question", value="Explain what an API key is in one sentence.")
if st.button("Ask Gemini", type="primary"):
    key = server_key or user_key.strip()
    if not key:
        st.error("Add a Gemini API key in Streamlit Secrets or enter your own key above.")
    elif not prompt.strip():
        st.error("Please enter a question.")
    else:
        with st.spinner("Contacting Gemini..."):
            try:
                client = genai.Client(api_key=key)
                response = client.models.generate_content(model=MODEL, contents=prompt.strip())
                if response.text:
                    st.subheader("Gemini's answer")
                    st.write(response.text)
                else:
                    st.warning("No text answer was returned. Please try a different question.")
            except Exception as exc:
                # Don't print raw errors: some third-party exceptions may contain credentials.
                st.error("The API request failed. Check your API key, free-tier model access, quotas, and app logs (without revealing secrets).")
