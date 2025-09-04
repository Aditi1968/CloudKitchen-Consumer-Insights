# Frontend (Streamlit) – Live Demo

## Quick Start
1. Install Python 3.10+
2. Open a terminal in `app/` and run:
   - Windows: `run_app.bat`
   - macOS/Linux: `bash run_app.sh`

This will install deps and launch the app at `http://localhost:8501/`.

## What’s inside
- Interactive charts (Plotly)
- Filters (age, order time, cuisine, keyword)
- Story Ideas (rule-based generator)
- Founder CRM view + export
- Meetings calendar view
- Pitch email generator

## Refresh the dataset
From project root:
```bash
python src/generate_data.py
```
Then refresh the browser.
