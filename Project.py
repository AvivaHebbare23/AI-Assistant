import streamlit as st
from google import genai 
from google.genai import types

client = genai.Client(api_key="AIzaSyCSeiUzLPBXVSfP-c6J-IA_rXuoP3pV2WI")

def generate_response(prompt, temperature=0.3):
    """Generate a response from Gemini API."""
    try:
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
        config_params = types.GenerateContentConfig(temperature=temperature)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=contents, config=config_params)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
    
def setup_ui():
    st.title("AI Teaching Assistant")
    st.write("Welcome! You can ask anything and I'll generate an answer.")
    user_input = st.text_input("Enter your question here: ")
    if user_input:
        st.write(f"**Your Question is: ** {user_input}")
        response = generate_response(user_input)
        st.write(f"**AI's Answer: ** {response}")
    else:
        st.write("Please enter a question.")

setup_ui()