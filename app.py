import streamlit as st
import subprocess
import tempfile
import sys
import os
import google.generativeai as genai

# --- Gemini API Setup ---
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def list_gemini_models():
    try:
        return [m.name for m in genai.list_models()]
    except Exception as e:
        return [f"Error listing models: {e}"]

def get_gemini_feedback(code, error=None):
    if not GEMINI_API_KEY:
        return "[Gemini API key not set. Please set GEMINI_API_KEY in Streamlit secrets or environment variable.]"
    prompt = f"""
You are an expert Python tutor. Analyze the following code and provide feedback.

Code:
{code}
"""
    if error:
        prompt += f"\n\nError:\n{error}\n\n1. Explain what went wrong.\n2. Suggest how to fix it.\n3. Suggest improvements for code style, structure, or efficiency."
    else:
        prompt += "\n\n1. Suggest improvements for code style, structure, or efficiency."
    try:
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[Gemini API error: {e}]"

def run_python_code(code, custom_input):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
        tmp.write(code)
        tmp_path = tmp.name
    try:
        result = subprocess.run(
            [sys.executable, tmp_path],
            input=custom_input,
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout
        error = result.stderr
    except subprocess.TimeoutExpired:
        output = ""
        error = "[Error] Code execution timed out."
    except Exception as e:
        output = ""
        error = f"[Error] {e}"
    finally:
        os.remove(tmp_path)
    return output, error

# --- Streamlit UI ---
st.set_page_config(page_title="AI-Powered Code Editor", layout="centered")
st.title("🧑‍💻 AI-Powered Code Editor & Tester")
st.markdown("""
Write your Python code below, provide custom input, and get instant feedback with Gemini AI!
""")

code = st.text_area("Python Code", height=200, value="n = int(input())\nprint(n * 10)")
custom_input = st.text_area("Custom Input (stdin)", height=80, value="5")
run_clicked = st.button("Run Code")

if run_clicked:
    with st.spinner("Running code..."):
        output, error = run_python_code(code, custom_input)
    st.subheader("Output")
    st.code(output if output else "[No output]", language="text")
    if error:
        st.subheader("Error")
        st.code(error, language="text")
    with st.spinner("Getting AI feedback..."):
        feedback = get_gemini_feedback(code, error if error else None)
    st.subheader("Gemini AI Feedback")
    st.write(feedback)

if st.button("Show Available Gemini Models"):
    st.subheader("Available Gemini Models")
    models = list_gemini_models()
    st.write(models)

st.markdown("---")
st.caption("Built with Streamlit & Gemini AI | © 2024") 