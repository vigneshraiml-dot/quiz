import streamlit as st
import time

# --- CONFIGURATION ---
QUIZ_TITLE = "AthenaHealth & AI Round 1"
QUIZ_DURATION = 120  # Seconds

# --- QUIZ DATA ---
questions = [
    {"question": "How does athenahealth describe its flagship product, athenaOne?", "options": ["A standalone billing tool", "An integrated, AI-native healthcare solution", "A social media app", "A simple calendar"], "answer": "An integrated, AI-native healthcare solution"},
    {"question": "What is the unique pricing model for athenaOne?", "options": ["Monthly subscription", "A percentage of collections", "Payment in gold", "Hourly rate"], "answer": "A percentage of collections"},
    {"question": "What is the EHR's 'AI-native' superpower?", "options": ["Writes poetry", "Diagnoses automatically", "Streamlines tasks & automates data exchange", "Plays chess"], "answer": "Streamlines tasks & automates data exchange"},
    {"question": "How does athenaOne handle rejected insurance claims?", "options": ["Identifies errors before submission", "Ignores them", "Sues the payer", "Returns them to patient"], "answer": "Identifies errors before submission"},
    {"question": "What is the 'clean claim submission rate' statistic?", "options": ["50%", "75%", "98.4%", "100%"], "answer": "98.4%"},
    {"question": "What does athenaOne say about long-term contracts?", "options": ["10-year lock-in", "Renew every Tuesday", "No long-term contracts (Leave anytime)", "Lifetime binding"], "answer": "No long-term contracts (Leave anytime)"},
    {"question": "🐍 Puzzle Clue: The favorite coding language of AI developers. (6 letters)", "options": ["COBRA", "PYTHON", "VIPER", "JAVA"], "answer": "PYTHON"},
    {"question": "✨ Puzzle Clue: The text you type to get the AI to do something.", "options": ["CODE", "SCRIPT", "PROMPT", "COMMAND"], "answer": "PROMPT"},
    {"question": "🥗 Puzzle Clue: What AI eats for breakfast (terabytes of it).", "options": ["CHIPS", "DATA", "WIFI", "ELECTRICITY"], "answer": "DATA"},
    {"question": "⚖️ Puzzle Clue: When an AI plays favorites because of bad training.", "options": ["BIAS", "ERROR", "GLITCH", "HALO"], "answer": "BIAS"}
]

# --- UI SETUP ---
st.set_page_config(page_title="Quiz Round 1", page_icon="🧩", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    div[data-testid="stMetricValue"] { font-size: 24px; color: #FF4B4B; }
    .stRadio label { font-size: 18px; padding: 12px; background: #f0f2f6; border-radius: 8px; margin: 4px 0; display:block; cursor:pointer;}
    .stRadio label:hover { background: #e0e2e6; }
    .stButton > button { width: 100%; border-radius: 8px; height: 50px; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'step' not in st.session_state: st.session_state.step = 'login'
if 'score' not in st.session_state: st.session_state.score = 0
if 'q_index' not in st.session_state: st.session_state.q_index = 0
if 'start_time' not in st.session_state: st.session_state.start_time = 0
if 'email' not in st.session_state: st.session_state.email = ""

# --- 1. LOGIN SCREEN ---
if st.session_state.step == 'login':
    st.title(f"🚀 {QUIZ_TITLE}")
    st.info("Enter your email to begin the challenge.")
    with st.form("login"):
        email = st.text_input("Email Address")
        if st.form_submit_button("Start Quiz"):
            if email:
                st.session_state.email = email
                st.session_state.start_time = time.time()
                st.session_state.step = 'quiz'
                st.rerun()
            else:
                st.warning("Email is required!")

# --- 2. QUIZ SCREEN ---
elif st.session_state.step == 'quiz':
    # Timer Logic
    elapsed = time.time() - st.session_state.start_time
    remaining = QUIZ_DURATION - elapsed
    if remaining <= 0:
        st.session_state.step = 'finish'
        st.rerun()

    # Header
    col1, col2 = st.columns([4, 1])
    col1.progress((st.session_state.q_index + 1) / len(questions), text=f"Question {st.session_state.q_index + 1} of {len(questions)}")
    col2.metric("⏱️ Time", f"{int(remaining)}s")

    # Question
    q = questions[st.session_state.q_index]
    st.subheader(q['question'])
    
    # Options
    choice = st.radio("Options", q['options'], index=None, key=f"q{st.session_state.q_index}", label_visibility="collapsed")

    # Navigation
    if st.button("Next Question ➜", type="primary"):
        if choice:
            if choice == q['answer']:
                st.session_state.score += 1
            
            if st.session_state.q_index + 1 < len(questions):
                st.session_state.q_index += 1
                st.rerun()
            else:
                st.session_state.step = 'finish'
                st.rerun()
        else:
            st.warning("Please select an answer!")

# --- 3. FINISH SCREEN ---
elif st.session_state.step == 'finish':
    st.balloons()
    st.title("🏆 Quiz Complete!")
    
    final_score = int((st.session_state.score / len(questions)) * 100)
    
    st.markdown(f"""
        <div style="text-align:center; padding:30px; background:#f0f8ff; border-radius:15px; border: 2px solid #ddd;">
            <h2>Score: {st.session_state.score} / {len(questions)}</h2>
            <h1 style="font-size:60px; color:#4CAF50;">{final_score}%</h1>
            <p>Well done, {st.session_state.email}!</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Restart Quiz"):
        st.session_state.clear()
        st.rerun()
