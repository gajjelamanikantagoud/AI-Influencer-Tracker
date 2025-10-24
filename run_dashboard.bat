@echo off
echo Starting AI Influencer Dashboard...

:: Activate the virtual environment
call venv\Scripts\activate

:: Run the streamlit app
streamlit run app/dashboard.py