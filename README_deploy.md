# Deploy Guide (Live Demo)

## Option A — Streamlit Community Cloud (Free, fastest)
1. Push this folder to a **public GitHub repo**.
2. Go to https://share.streamlit.io → **New app**.
3. Select your repo/branch and set **App file** = `app/streamlit_app.py`.
4. Click **Deploy**. In ~1–2 minutes your app will be live.

## Option B — Hugging Face Spaces (Free)
1. Create new **Space** → Type: **Streamlit**.
2. Connect your GitHub or **Upload files**.
3. In Space settings, set **App file** to `app/streamlit_app.py`.
4. Add `app/requirements.txt` under **Python dependencies** (or include a root `requirements.txt` that points to it).

## Option C — Render (Free web service)
- One-click via `render.yaml`:
  - Create a new Web Service, point to your repo root.
  - Render auto-detects `render.yaml` and uses:
    - Build: `pip install -r app/requirements.txt`
    - Start: `streamlit run app/streamlit_app.py --server.port $PORT --server.address 0.0.0.0`

## Option D — Docker anywhere
```bash
docker build -t toi-insights .
docker run -p 8501:8501 toi-insights
```

## Option E — Local + Cloudflare Tunnel (instant private link)
```bash
# 1) Run the app locally
cd app
python -m pip install -r requirements.txt
streamlit run streamlit_app.py

# 2) Expose securely (replace 8501 if you changed the port)
cloudflared tunnel --url http://localhost:8501
```
This prints a public HTTPS URL you can share.

### Notes
- The app reads data from `data/` CSVs in the repo root. If you change dataset paths, update the Streamlit code accordingly.
- No secrets are required for this demo.
