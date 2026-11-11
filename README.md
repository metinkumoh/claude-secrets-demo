# Gemini Secrets Demo — ATF Challenge Week 4.2 Exercise 2

A Streamlit app that calls Google Gemini using a server-side secret, with manual password-field fallback. This is a **Gemini alternative** to the Anthropic-specific exercise, selected to avoid requiring Anthropic paid API credits.

## Deploy (Streamlit Community Cloud)

1. Create a GitHub repository and upload `app.py`, `requirements.txt`, `.gitignore`, and this README. Do not upload any real secret keys.
2. Open https://share.streamlit.io and create an app from that repository; main file `app.py`.
3. Open **Manage app → ⋮ → Settings → Secrets** and enter `GEMINI_API_KEY = "your_real_key"` in the private Streamlit secrets editor. Save.
4. Open the app, leave the manual field unused, ask a question, and confirm a response.
5. To test the fallback, temporarily remove the server secret, save, refresh the app, enter **your own key** in the password field, and ask a question. Restore the server secret when finished.

## Test locally

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Optionally create `.streamlit/secrets.toml` locally by copying `.streamlit/secrets.toml.example` and replacing its placeholder. Never commit the real `secrets.toml`.

## Notes

- Uses `google-genai` and the `gemini-3.6-flash` model. Actual access depends on current model availability, account eligibility and API quotas. Free-tier requests are subject to limits; check https://ai.google.dev/gemini-api/docs/pricing.
- An app with a server-side key exposed publicly lets visitors spend your API allowance. Restrict access or add authentication and rate limits before widespread sharing.
- Never post, log, or upload real API keys. If a key was exposed, revoke it and generate a new one.
- The app intentionally displays a generic error rather than potentially sensitive provider exception text.
