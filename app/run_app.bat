@echo off
cd /d %~dp0
python -m pip install -r requirements.txt
streamlit run streamlit_app.py
