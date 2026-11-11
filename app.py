"""Week 4.2 Exercise 2 — Anthropic API with secure secret fallback."""
import os
import streamlit as st
from anthropic import Anthropic, AuthenticationError, RateLimitError, APIConnectionError, APIStatusError
from auth import resolve_api_key

st.set_page_config(page_title="Claude Secrets Demo", page_icon="🔐")
st.title("🔐 Claude API — Secure Secrets Demo")
st.caption("Week 4.2 · Exercise 2")

# Reading Streamlit Cloud secrets can raise FileNotFoundError on a fresh local install.
try:
    cloud_key = st.secrets.get("ANTHROPIC_API_KEY")
except (FileNotFoundError, KeyError):
    cloud_key = None

configured_key, source = resolve_api_key(
    environment_key=os.getenv("ANTHROPIC_API_KEY"),
    streamlit_key=cloud_key,
)

manual_key = None
if configured_key:
    st.success(f"API key configured via {source}.")
    st.info("The app uses its server-side key. Visitors do not need to enter one.")
else:
    st.warning("No server-side API key was configured.")
    st.info("Only enter your own key into a deployment you control and trust. Public apps must not log or save visitors' keys.")
    manual_key = st.text_input(
        "Anthropic API key (optional)",
        type="password",
        placeholder="sk-ant-...",
        help="For this exercise only. The key is used to call Anthropic and is not saved to disk.",
    )

api_key, source = resolve_api_key(
    environment_key=os.getenv("ANTHROPIC_API_KEY"),
    streamlit_key=cloud_key,
    manual_key=manual_key,
)

model = os.getenv("ANTHROPIC_MODEL", "claude-haiku-5-5")
question = st.text_area("Ask Claude a question", value="Explain what an API key is in one sentence.", max_chars=2000)

if st.button("Ask Claude", type="primary"):
    if not api_key:
        st.error("Provide an API key to continue.")
    elif not question.strip():
        st.error("Enter a question.")
    else:
        try:
            with st.spinner("Contacting Anthropic..."):
                client = Anthropic(api_key=api_key, timeout=30.0, max_retries=0)
                response = client.messages.create(
                    model=model,
                    max_tokens=200,
                    messages=[{"role": "user", "content": question.strip()}],
                )
            answer = "\n".join(block.text for block in response.content if block.type == "text")
            st.subheader("Claude's reply")
            st.write(answer or "The model returned no text response.")
            st.caption(f"Credential source: {source}; model: {model}")
        except AuthenticationError:
            st.error("Authentication failed. Check whether the API key is valid.")
        except RateLimitError:
            st.error("The API request was rate-limited or your account has reached its available quota.")
        except APIConnectionError:
            st.error("Could not connect to Anthropic. Check your network and try again.")
        except APIStatusError as exc:
            st.error(f"Anthropic returned an API error (HTTP {exc.status_code}). Check your model access and account settings.")
        except Exception:
            st.error("The request could not be completed. Check your deployment logs for non-sensitive diagnostics.")

st.divider()
st.caption("API calls may incur Anthropic charges. Never publish or print API keys.")
