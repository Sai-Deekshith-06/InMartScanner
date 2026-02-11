# python -m venv venv
# source venv/Scripts/activate
# pip install -r requirements.txt
# streamlit run app1.py
#!/bin/bash

export RAPID_API_KEY="32d4e13869mshe58c8ba195ec19bp1992bcjsn25302358262e"
docker compose build --no-cache
docker compose up