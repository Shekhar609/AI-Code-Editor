# 🧑‍💻 AI-Powered Code Editor & Tester

A Streamlit app that lets you write, test, and get AI feedback on Python code using the Gemini API.

## Features
- Write Python code in a code editor
- Provide custom input (stdin)
- Run code and see output/errors
- Get AI-powered feedback on errors and code improvements

## Setup

1. **Clone the repository or copy the files.**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your Gemini API key:**
   - Add to `.streamlit/secrets.toml`:
     ```toml
     GEMINI_API_KEY = "your-gemini-api-key"
     ```
   - Or set as an environment variable:
     ```bash
     export GEMINI_API_KEY=your-gemini-api-key
     ```
4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Usage
- Enter your Python code in the editor.
- Provide any custom input (stdin) if needed.
- Click **Run Code** to execute and get output.
- See AI feedback for errors and suggestions.

---
Built with ❤️ using Streamlit & Gemini AI 