from pyngrok import ngrok

# Open a tunnel to the Streamlit port
public_url = ngrok.connect(8501)
print(f"Public URL: {public_url}")
