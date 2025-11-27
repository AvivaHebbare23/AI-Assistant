import streamlit as st
from google import genai
from google.genai import types
import io

client = genai.Client(api_key="AIzaSyCSeiUzLPBXVSfP-c6J-IA_rXuoP3pV2WI")

def generate_response(prompt: str, temperature: float = 0.3) -> str:
    """Generate response using Gemini API."""
    try:
        system_prompt = """You're a math mastermind. 
        Solve math problems step-by-step, explain reasoning, use proper notation, and highlight the final answers. """
        full_prompt = f"{system_prompt}\n\nProblem: {prompt}"
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=full_prompt)])]
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=contents, 
            config=types.GenerateContentConfig(temperature=temperature),
            )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


st.set_page_config(page_title="AI Math Assistant", layout="centered")
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 36px;
        color: blue;
        font-weight: bold;
    }
    .history-box {
        background: linear-gradient(135deg, pink 0%, purple 100%);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 20 px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .question {
        font-weight: bold;
        color: blue;
        margin-bottom: 5px;
    }
    .answer {
        background: white;
        padding: 10px;
        border-left: 4px solid orange;
        border-radius: 8px;
        color: red;
    }

    </style>
""", unsafe_allow_html=True)
    
st.markdown('<div class="main-title">Math Assistant<\div>', unsafe_allow_html=True)
st.write("Solve math problems from basic arithmetic to advanced calculus with clear, step-by-step solutions.")

with st.expander("📚 Example Problems"):
    st.markdown("""
- **Algebra:** Solve 2x² + 5x - 3 = 0
- **Calculus:** Derivative of sin(x²) + ln(x)
- **Geometry:** Area of a triangle with vertices (0,0), (3,4), (6,0)
- **Statistics:** Probability of rolling a 7 with two dice
- **Word Problems:** A train goes 300 miles in 4 hours. Speed?
""")
    
if "history" not in st.session_state: st.session_state.history = []

col1, col2 = st.columns([1,2])
if col1.button("🧹 Clear History"): st.session_state.history.clear()
if col2.button("📥 Export Solutions") and st.session_state.history:
    export_text = "\n\n".join([f"Q: {h['q']}\nA: {h['a']}" for h in st.session_state.history])
    bio = io.BytesIO(export_text.encode("utf-8"))
    st.download_button("Download", bio, "math_solutions.txt")

with st.form("math form"):
    user_input = st.text_area("Enter your math problem: ", height=80)
    difficulty = st.selectbox("Level", ["Basic", "Intermediate", "Advanced"], index=1)
    submitted = st.form_submit_button("Solve")
    if submitted and user_input.strip():
        with st.spinner("Solving your problem..."):
            ans = generate_response(f"[{difficulty}] {user_input.strip()}")
        st.session_state.history.insert(0, {"q": user_input.strip(), "a": ans, "d": difficulty})

if st.session_state.history:
    st.markdown("### 📋 Solution History")
    for i, h in enumerate(st.session_state.history, 1):
        st.markdown(f"""
        <div class="history-box">
            <div class="question">Problem {i} ({h['d']}): {h['q']}</div>
            <div class="answer">{h['a']}</div>
        </div>
        """, unsafe_allow_html=True)