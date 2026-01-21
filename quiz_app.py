import streamlit as st
import time
from pathlib import Path

# Configuration
QUIZ_TITLE = "AthenaHealth & AI Quiz"
QUIZ_DURATION = 600  # 10 minutes

# Initialize session state
def init_session():
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'current_section' not in st.session_state:
        st.session_state.current_section = None
    if 'scores' not in st.session_state:
        st.session_state.scores = {'mcq': 0, 'pictorial': 0, 'crossword': 0}
    if 'q_index' not in st.session_state:
        st.session_state.q_index = 0
    if 'start_time' not in st.session_state:
        st.session_state.start_time = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'name' not in st.session_state:
        st.session_state.name = ""
    if 'email' not in st.session_state:
        st.session_state.email = ""

# Page config
st.set_page_config(page_title=QUIZ_TITLE, page_icon="📚", layout="wide")
init_session()

# MCQ Questions
mcq_questions = [
    {"question": "How does athenahealth describe its flagship product, athenaOne?", 
     "options": ["A standalone billing tool", "An integrated, AI-native healthcare solution", "A social media app for surgeons", "A simple calendar app"], 
     "answer": "An integrated, AI-native healthcare solution"},
    {"question": "What is the unique pricing model for athenaOne?", 
     "options": ["A massive upfront fee", "They accept payment in gold bars", "A percentage of your collections", "A flat monthly subscription"], 
     "answer": "A percentage of your collections"},
    {"question": "What is the EHR's 'AI-native' superpower?", 
     "options": ["It writes poetry for patients", "It plays chess with the doctor", "It streamlines tasks and automates data exchange", "It diagnoses patients automatically"], 
     "answer": "It streamlines tasks and automates data exchange"},
    {"question": "How does athenaOne handle rejected insurance claims?", 
     "options": ["It identifies errors before submission", "It ignores them and hopes for the best", "It uses a magic 8-ball", "It automatically sues the payer"], 
     "answer": "It identifies errors before submission"},
    {"question": "What impressive statistic does athenahealth boast regarding their 'clean claim submission rate'?", 
     "options": ["50%", "75%", "98.4%", "100%"], 
     "answer": "98.4%"},
    {"question": "What does athenaOne say about long-term contracts?", 
     "options": ["You must sign for 10 years", "No long-term contracts; leave anytime", "Contracts renew every Tuesday", "You have to sign in invisible ink"], 
     "answer": "No long-term contracts; leave anytime"},
    {"question": "How does the 'Patient Engagement' suite help patients?", 
     "options": ["It empowers them with self-service tools", "It forces them to learn medical coding", "It gives them free candy", "It plays loud music"], 
     "answer": "It empowers them with self-service tools"},
    {"question": "In MIPS quality scores, how do athenaOne clinicians compare to industry average?", 
     "options": ["They score way lower", "99.9% vs the 95.96% average", "They are exactly average", "The score is a secret"], 
     "answer": "99.9% vs the 95.96% average"},
    {"question": "Who is your best friend when you first start using athenaOne?", 
     "options": ["A Customer Success Manager", "A random chatbot", "No one, you are on your own", "The office cat"], 
     "answer": "A Customer Success Manager"},
    {"question": "What happens to your data if you decide to leave athenaOne?", 
     "options": ["They delete it immediately", "They keep it hostage", "You can take all your data with you", "They print it on a giant scroll"], 
     "answer": "You can take all your data with you"}
]

# Pictorial Questions
pictorial_questions = [
    {"question": "What AI concept does this image represent?", 
     "image": "assets/robot_lightbulb.png",
     "options": ["A new lightbulb design", "Artificial Intelligence (AI)", "A robot electrician", "A metal toy"], 
     "answer": "Artificial Intelligence (AI)", "hint": "The robot with an idea!"},
    {"question": "What technology is shown here?", 
     "image": "assets/cloud_server.png",
     "options": ["A rainy day for computers", "Data Mining", "Cloud Computing", "A broken server"], 
     "answer": "Cloud Computing", "hint": "Data in the cloud!"},
    {"question": "What does this vehicle represent?", 
     "image": "assets/self_driving_car.png",
     "options": ["A ghost driver", "A parked car", "Self-driving car (Autonomous Vehicle)", "A very dangerous driver"], 
     "answer": "Self-driving car (Autonomous Vehicle)", "hint": "AI at the wheel!"},
    {"question": "What type of reality is this?", 
     "image": "assets/vr_headset.png",
     "options": ["Augmented Reality", "Virtual Reality (VR)", "A new kind of sunglasses", "Someone having a vivid dream"], 
     "answer": "Virtual Reality (VR)", "hint": "Immersive experience!"},
    {"question": "What AI component is this?", 
     "image": "assets/neural_network.png",
     "options": ["A super-smart CPU", "A Neural Network", "A computer virus", "A cyborg brain"], 
     "answer": "A Neural Network", "hint": "Brain-inspired computing!"},
    {"question": "What type of AI model is represented?", 
     "image": "assets/llm_book.png",
     "options": ["A digital library", "A Large Language Model (LLM)", "An e-book reader", "An audiobook"], 
     "answer": "A Large Language Model (LLM)", "hint": "Like ChatGPT!"},
    {"question": "What technology is being used?", 
     "image": "assets/facial_recognition.png",
     "options": ["A new Snapchat filter", "Eye-tracking software", "Facial Recognition", "A virtual makeup app"], 
     "answer": "Facial Recognition", "hint": "Face scanning!"},
    {"question": "What feature is helping the user type?", 
     "image": "assets/predictive_text.png",
     "options": ["Autocorrecting a mistake", "Using Predictive Text", "Translating a language", "Sending an emoji"], 
     "answer": "Using Predictive Text", "hint": "Text suggestions!"},
    {"question": "What flying device uses AI?", 
     "image": "assets/drone.png",
     "options": ["A remote-controlled helicopter", "A Drone (UAV)", "A small airplane", "A flying camera"], 
     "answer": "A Drone (UAV)", "hint": "Unmanned flight!"},
    {"question": "What smart home device is this?", 
     "image": "assets/smart_assistant.png",
     "options": ["A Bluetooth speaker", "A WiFi router", "A Smart Home Assistant", "An alarm clock"], 
     "answer": "A Smart Home Assistant", "hint": "Voice activated!"}
]

# Crossword Questions
crossword_questions = [
    {"question": "ACROSS 1: Computer program for chatting (7 Letters)", 
     "options": ["CHATBOT", "PROGRAM", "ANDROID", "WEBSITE"], "answer": "CHATBOT"},
    {"question": "ACROSS 2: When AI makes up facts (11 Letters)", 
     "options": ["HALLUCINATE", "IMAGINATION", "FABRICATION", "CALCULATION"], "answer": "HALLUCINATE"},
    {"question": "ACROSS 3: Snake-named programming language (6 Letters)", 
     "options": ["PYTHON", "COBRAS", "PASCAL", "GOLANG"], "answer": "PYTHON"},
    {"question": "ACROSS 4: Text input to AI (6 Letters)", 
     "options": ["PROMPT", "INPUTS", "ORDERS", "SIGNAL"], "answer": "PROMPT"},
    {"question": "ACROSS 5: AI _____ (5 Letters)", 
     "options": ["MODEL", "BRAIN", "AGENT", "SMART"], "answer": "MODEL"},
    {"question": "DOWN 6: AI's food (4 Letters)", 
     "options": ["DATA", "CODE", "WIFI", "BITS"], "answer": "DATA"},
    {"question": "DOWN 7: Physical AI body (5 Letters)", 
     "options": ["ROBOT", "DROID", "CYBORG", "CLONE"], "answer": "ROBOT"},
    {"question": "DOWN 8: AI unfairness (4 Letters)", 
     "options": ["BIAS", "HATE", "LOVE", "FEAR"], "answer": "BIAS"},
    {"question": "DOWN 9: Computer ______ (6 Letters)", 
     "options": ["VISION", "SENSOR", "CAMERA", "SCREEN"], "answer": "VISION"},
    {"question": "DOWN 10: ____ Learning (4 Letters)", 
     "options": ["DEEP", "WIDE", "HUGE", "LONG"], "answer": "DEEP"}
]

# Crossword SVG
CROSSWORD_SVG = """<svg width="600" height="450" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#f9f9f9"/>
  <g transform="translate(20, 180)"> <rect x="0" y="0" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
    <text x="5" y="15" font-family="Arial" font-size="12">3</text>
    <rect x="40" y="0" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
    <rect x="80" y="0" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
    <rect x="120" y="0" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
    <rect x="160" y="0" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
    <rect x="200" y="0" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  </g>
  <rect x="20" y="60" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <text x="25" y="75" font-family="Arial" font-size="12">4</text>
  <rect x="60" y="60" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="100" y="60" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="140" y="60" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="180" y="60" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="220" y="60" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="100" y="20" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <text x="105" y="35" font-family="Arial" font-size="12">5</text>
  <rect x="100" y="100" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="100" y="140" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="60" y="100" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <text x="65" y="115" font-family="Arial" font-size="12">1</text>
  <rect x="60" y="140" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="60" y="220" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="60" y="260" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="60" y="300" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="60" y="340" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="260" y="140" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <text x="265" y="155" font-family="Arial" font-size="12">9</text>
  <rect x="260" y="220" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="260" y="260" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="260" y="300" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="260" y="340" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="140" y="220" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <text x="145" y="235" font-family="Arial" font-size="12">8</text>
  <rect x="180" y="220" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="220" y="220" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="220" y="300" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <text x="225" y="315" font-family="Arial" font-size="12">7</text>
  <rect x="300" y="300" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="340" y="300" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="380" y="300" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="340" y="140" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <text x="345" y="155" font-family="Arial" font-size="12">6/10</text>
  <rect x="340" y="220" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="340" y="260" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="380" y="140" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="420" y="140" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
  <rect x="460" y="140" width="40" height="40" stroke="black" fill="white" stroke-width="2"/>
</svg>"""

# Helper function
def get_questions(section):
    if section == 'mcq':
        return mcq_questions
    elif section == 'pictorial':
        return pictorial_questions
    return crossword_questions

# Home Page
if st.session_state.page == 'home':
    st.title("📚 " + QUIZ_TITLE)
    st.divider()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Welcome to the Quiz!")
        st.write("Test your knowledge across three exciting sections:")
        
        st.info("""
        **📝 Section 1: AthenaHealth MCQ**  
        10 questions about athenaOne healthcare platform
        
        **🎨 Section 2: Pictorial Charades**  
        10 visual puzzles about AI concepts
        
        **🧩 Section 3: AI Crossword**  
        10 crossword clues about AI terminology
        """)
        
        st.divider()
        st.subheader("Enter Your Details")
        
        name = st.text_input("Name")
        email = st.text_input("Email")
        
        if st.button("Start Quiz", type="primary", use_container_width=True):
            if name and email:
                st.session_state.name = name
                st.session_state.email = email
                st.session_state.start_time = time.time()
                st.session_state.page = 'section_select'
                st.rerun()
            else:
                st.error("Please enter both name and email")
    
    with col2:
        st.subheader("Quiz Rules")
        st.warning("""
        ⏱️ **Time Limit:** 10 minutes total
        
        📊 **Total Questions:** 30
        
        ✅ **Scoring:** 1 point per correct answer
        
        🔄 **Navigation:** Move between sections
        """)

# Section Selection Page
elif st.session_state.page == 'section_select':
    st.title("📋 Select a Section")
    st.divider()
    
    # Timer
    if st.session_state.start_time:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, QUIZ_DURATION - elapsed)
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        if remaining <= 0:
            st.session_state.page = 'results'
            st.rerun()
        
        st.sidebar.metric("⏱️ Time", f"{minutes:02d}:{seconds:02d}")
        st.sidebar.metric("📊 Total Score", f"{sum(st.session_state.scores.values())}/30")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📝 MCQ")
        st.write("AthenaHealth questions")
        st.metric("Score", f"{st.session_state.scores['mcq']}/10")
        if st.button("Start MCQ", use_container_width=True):
            st.session_state.current_section = 'mcq'
            st.session_state.q_index = 0
            st.session_state.page = 'quiz'
            st.rerun()
    
    with col2:
        st.subheader("🎨 Pictorial")
        st.write("AI concept puzzles")
        st.metric("Score", f"{st.session_state.scores['pictorial']}/10")
        if st.button("Start Pictorial", use_container_width=True):
            st.session_state.current_section = 'pictorial'
            st.session_state.q_index = 0
            st.session_state.page = 'quiz'
            st.rerun()
    
    with col3:
        st.subheader("🧩 Crossword")
        st.write("AI terminology")
        st.metric("Score", f"{st.session_state.scores['crossword']}/10")
        if st.button("Start Crossword", use_container_width=True):
            st.session_state.current_section = 'crossword'
            st.session_state.q_index = 0
            st.session_state.page = 'quiz'
            st.rerun()
    
    st.divider()
    if st.button("📊 View Results", type="primary", use_container_width=True):
        st.session_state.page = 'results'
        st.rerun()

# Quiz Page
elif st.session_state.page == 'quiz':
    questions = get_questions(st.session_state.current_section)
    
    # Timer
    if st.session_state.start_time:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, QUIZ_DURATION - elapsed)
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        if remaining <= 0:
            st.session_state.page = 'results'
            st.rerun()
        
        st.sidebar.metric("⏱️ Time", f"{minutes:02d}:{seconds:02d}")
        st.sidebar.metric("📊 Score", f"{sum(st.session_state.scores.values())}/30")
    
    # Section title
    titles = {'mcq': '📝 MCQ Section', 'pictorial': '🎨 Pictorial Section', 'crossword': '🧩 Crossword Section'}
    st.title(titles[st.session_state.current_section])
    
    # Progress
    progress = (st.session_state.q_index + 1) / len(questions)
    st.progress(progress)
    st.caption(f"Question {st.session_state.q_index + 1} of {len(questions)}")
    st.divider()
    
    q = questions[st.session_state.q_index]
    
    # Display based on section
    if st.session_state.current_section == 'crossword':
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Crossword Puzzle")
            st.markdown(CROSSWORD_SVG, unsafe_allow_html=True)
        with col2:
            st.subheader("Question")
            st.write(q['question'])
            choice = st.radio("Select answer:", q['options'])
    
    elif st.session_state.current_section == 'pictorial':
        col1, col2 = st.columns([1, 1])
        with col1:
            # Check if image exists
            img_path = Path(q['image'])
            if img_path.exists():
                st.image(str(img_path))
            else:
                st.info(f"🖼️ Image: {q['image']}")
                st.caption("(Image placeholder)")
            
            if 'hint' in q:
                with st.expander("💡 Hint"):
                    st.write(q['hint'])
        
        with col2:
            st.subheader("Question")
            st.write(q['question'])
            choice = st.radio("Select answer:", q['options'])
    
    else:  # MCQ
        st.subheader("Question")
        st.write(q['question'])
        choice = st.radio("Select answer:", q['options'])
    
    st.divider()
    
    # Navigation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.session_state.q_index > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.q_index -= 1
                st.rerun()
    
    with col2:
        if st.button("🏠 Menu", use_container_width=True):
            st.session_state.page = 'section_select'
            st.rerun()
    
    with col3:
        is_last = st.session_state.q_index >= len(questions) - 1
        
        if st.button("Next ➡️" if not is_last else "Complete ✅", type="primary", use_container_width=True):
            if choice:
                key = f"{st.session_state.current_section}_{st.session_state.q_index}"
                if key not in st.session_state.answers:
                    if choice == q['answer']:
                        st.session_state.scores[st.session_state.current_section] += 1
                    st.session_state.answers[key] = choice
                
                if is_last:
                    st.session_state.page = 'section_select'
                else:
                    st.session_state.q_index += 1
                st.rerun()
            else:
                st.error("Please select an answer")

# Results Page
elif st.session_state.page == 'results':
    st.title("📊 Quiz Results")
    st.divider()
    
    total = sum(st.session_state.scores.values())
    percentage = (total / 30) * 100
    
    st.subheader(f"Hello, {st.session_state.name}!")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.metric("Total Score", f"{total}/30")
        st.metric("Percentage", f"{percentage:.1f}%")
        
        if percentage >= 80:
            st.success("🏆 Excellent!")
        elif percentage >= 60:
            st.info("⭐ Good Job!")
        else:
            st.warning("📚 Keep Learning!")
    
    st.divider()
    st.subheader("Section Breakdown")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**📝 MCQ**")
        score = st.session_state.scores['mcq']
        st.metric("Score", f"{score}/10")
        st.progress(score / 10)
    
    with col2:
        st.write("**🎨 Pictorial**")
        score = st.session_state.scores['pictorial']
        st.metric("Score", f"{score}/10")
        st.progress(score / 10)
    
    with col3:
        st.write("**🧩 Crossword**")
        score = st.session_state.scores['crossword']
        st.metric("Score", f"{score}/10")
        st.progress(score / 10)
    
    st.divider()
    if st.button("🔄 New Quiz", type="primary", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
