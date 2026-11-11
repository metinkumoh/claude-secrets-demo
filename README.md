# Week 4.2 — Exercise 2: Anthropic API with Secrets

A Streamlit app that calls Claude using the official Anthropic Python SDK, with both server-side and manually supplied API keys.

## Quick start

Requires Python 3.10+ and a valid Anthropic API key (may incur charges).

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Method A — Cloud-managed secret (recommended)

Deploy the repo on [Streamlit Community Cloud](https://share.streamlit.io/). Open your app's **Settings → Secrets** panel and add this TOML:

```toml
ANTHROPIC_API_KEY = "YOUR_REAL_API_KEY"
```

Save and restart/rerun the app if needed. It should display **API key configured via Streamlit secret.** The key is not exposed in app code.

For local testing, create `.streamlit/secrets.toml` with the same contents. It is excluded by `.gitignore`.

You can also set `ANTHROPIC_API_KEY` in your local process environment. The app checks `st.secrets` first, then environment variables.

## Method B — Manual fallback

To test the fallback, run a local copy **without** `.streamlit/secrets.toml` and **without** the `ANTHROPIC_API_KEY` environment variable. The app displays a password-type field. Enter your own key; press **Ask Claude**. No key is saved by this app to a file, and it is not deliberately logged. For safety, use this option only in a deployment you control and trust. Do not share credentials with strangers or put them in screenshots.

## Automated tests

```powershell
python -m unittest discover -s tests -v
```

Six unit tests verify credential source selection and fallback with dummy values. These tests **do not** call the live Anthropic API. To complete a live end-to-end test, provide a valid key and submit a question.

## Configuring the model

The app defaults to `claude-haiku-5-5`. To change it, set an `ANTHROPIC_MODEL` environment variable to a model available to your Anthropic account. This environment setting is optional and is not a secret.

## Security notes

- Never commit keys or `.streamlit/secrets.toml` to Git.
- Don't print secrets, put them in logs, or include them in chat messages.
- Avoid storing visitors' supplied keys. This app does not persist them to disk but Streamlit holds input-widget values in the active session.
- Public use of your server-side API key can incur charges; add access control, rate limits, and spending caps before publicly promoting the app.

## Deployment

Upload `app.py`, `auth.py`, `requirements.txt`, `.gitignore`, and `README.md` to a GitHub repository and deploy on Streamlit Community Cloud by selecting `app.py` as the main file. Configure the secret through the Streamlit Cloud UI, not through GitHub. For this exercise, no Dockerfile or Hugging Face YAML is required.

Reference: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management
