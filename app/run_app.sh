#!/usr/bin/env bash
cd "$(dirname "$0")"
python3 -m pip install -r requirements.txt
streamlit run streamlit_app.py
