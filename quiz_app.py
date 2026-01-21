import streamlit as st
import time
import base64
from pathlib import Path

# --- ⚙️ CONFIGURATION ---
QUIZ_TITLE = "AthenaHealth & AI Quiz"
QUIZ_DURATION = 600  # 10 minutes for all sections

# --- 📝 ALL QUIZ SECTIONS ---

# Section 1: athenahealth MCQs
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
     "answer": "You can take all your data with you"},
]

# Section 2: Pictorial Charades (AI Concepts)
pictorial_questions = [
    {"question": "🤖💡 What's the big idea here? (Robot with lightbulb)", 
     "options": ["A new lightbulb design", "Artificial Intelligence (AI)", "A robot electrician", "A metal toy"], 
     "answer": "Artificial Intelligence (AI)", "hint": "The robot with an idea (lightbulb) is the classic symbol!"},
    {"question": "☁️💾 Where is all that data going? (Cloud raining into server)", 
     "options": ["A rainy day for computers", "Data Mining", "Cloud Computing", "A broken server"], 
     "answer": "Cloud Computing", "hint": "The cloud raining data into a server!"},
    {"question": "🚗👻 Who's driving this thing? (Car with no driver)", 
     "options": ["A ghost driver", "A parked car", "Self-driving car (Autonomous Vehicle)", "A very dangerous driver"], 
     "answer": "Self-driving car (Autonomous Vehicle)", "hint": "No driver needed, the AI is at the wheel!"},
    {"question": "🥽🌐 What kind of reality is this? (Person with headset)", 
     "options": ["Augmented Reality", "Virtual Reality (VR)", "A new kind of sunglasses", "Someone having a vivid dream"], 
     "answer": "Virtual Reality (VR)", "hint": "The headset and reaching pose are dead giveaways!"},
    {"question": "🧠💻 What is this brainy-looking chip?", 
     "options": ["A super-smart CPU", "A Neural Network", "A computer virus", "A cyborg brain"], 
     "answer": "A Neural Network", "hint": "The brain structure on a chip!"},
    {"question": "📚🗣️ What kind of AI is this big book representing?", 
     "options": ["A digital library", "A Large Language Model (LLM)", "An e-book reader", "An audiobook"], 
     "answer": "A Large Language Model (LLM)", "hint": "Like ChatGPT, trained on huge amounts of text!"},
    {"question": "👤🔲 What technology is being used on this person's face?", 
     "options": ["A new Snapchat filter", "Eye-tracking software", "Facial Recognition", "A virtual makeup app"], 
     "answer": "Facial Recognition", "hint": "The digital grid scanning the face!"},
    {"question": "📱⌨️ What is the phone doing to help the user type?", 
     "options": ["Autocorrecting a mistake", "Using Predictive Text", "Translating a language", "Sending an emoji"], 
     "answer": "Using Predictive Text", "hint": "Suggested words above the keyboard!"},
    {"question": "🚁📷 What is this flying device that often uses AI for navigation?", 
     "options": ["A remote-controlled helicopter", "A Drone (UAV)", "A small airplane", "A flying camera"], 
     "answer": "A Drone (UAV)", "hint": "Unmanned Aerial Vehicles use AI for autonomous flight!"},
    {"question": "🔊🏠 What is this common household device that listens to your commands?", 
     "options": ["A Bluetooth speaker", "A WiFi router", "A Smart Home Assistant", "An alarm clock"], 
     "answer": "A Smart Home Assistant", "hint": "Hey Alexa, Hey Google, Hey Siri!"},
]

# Section 3: Crossword Clues
crossword_questions = [
    {"question": "ACROSS 1: 'I'm the friendly computer program you're chatting with. I don't have a body, but I love to chat!' (7 Letters)", 
     "options": ["CHATBOT", "PROGRAM", "ANDROID", "WEBSITE"], "answer": "CHATBOT", "category": "across"},
    {"question": "ACROSS 2: 'Oops! This is what happens when an AI makes up a fact but sounds super confident about it.' (11 Letters)", 
     "options": ["HALLUCINATE", "IMAGINATION", "FABRICATION", "CALCULATION"], "answer": "HALLUCINATE", "category": "across"},
    {"question": "ACROSS 3: 'The favorite coding language of AI developers. Shares its name with a large, slithery reptile.' (6 Letters)", 
     "options": ["PYTHON", "COBRAS", "PASCAL", "GOLANG"], "answer": "PYTHON", "category": "across"},
    {"question": "ACROSS 4: 'The text you type to get the AI to do something. The better this is, the better your answer!' (6 Letters)", 
     "options": ["PROMPT", "INPUTS", "ORDERS", "SIGNAL"], "answer": "PROMPT", "category": "across"},
    {"question": "ACROSS 5: 'I'm trained on data to make predictions. I am an AI _____.' (5 Letters)", 
     "options": ["MODEL", "BRAIN", "AGENT", "SMART"], "answer": "MODEL", "category": "across"},
    {"question": "DOWN 6: 'This is what AI eats for breakfast, lunch, and dinner. Without terabytes of this, AI learns nothing!' (4 Letters)", 
     "options": ["DATA", "CODE", "WIFI", "BITS"], "answer": "DATA", "category": "down"},
    {"question": "DOWN 7: 'Beep boop! I might build your car, vacuum your floor, or dance in a viral video. I have a physical body.' (5 Letters)", 
     "options": ["ROBOT", "DROID", "CYBORG", "CLONE"], "answer": "ROBOT", "category": "down"},
    {"question": "DOWN 8: 'If an AI only likes dogs because it was never shown a cat, it has this. When the computer plays favorites.' (4 Letters)", 
     "options": ["BIAS", "HATE", "LOVE", "FEAR"], "answer": "BIAS", "category": "down"},
    {"question": "DOWN 9: 'Computer ______ is how an autonomous car sees the stop sign and the squirrel on the road.' (6 Letters)", 
     "options": ["VISION", "SENSOR", "CAMERA", "SCREEN"], "answer": "VISION", "category": "down"},
    {"question": "DOWN 10: 'This word goes before Learning when you have many layers of neural networks. It's not shallow, it's...?' (4 Letters)", 
     "options": ["DEEP", "WIDE", "HUGE", "LONG"], "answer": "DEEP", "category": "down"},
]

# --- CROSSWORD SVG ---
CROSSWORD_SVG = """
<svg width="600" height="450" xmlns="http://www.w3.org/2000/svg">
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
</svg>
"""

# --- PAGE CONFIG ---
st.set_page_config(page_title=QUIZ_TITLE, page_icon="📚", layout="wide")

# --- SESSION STATE ---
def init_session():
    if 'page' not in st.session_state: st.session_state.page = 'home'
    if 'scores' not in st.session_state: st.session_state.scores = {'mcq': 0, 'pictorial': 0, 'crossword': 0}
    if 'q_index' not in st.session_state: st.session_state.q_index = 0
    if 'current_section' not in st.session_state: st.session_state.current_section = None
    if 'start_time' not in st.session_state: st.session_state.start_time = 0
    if 'answers' not in st.session_state: st.session_state.answers = {}
    if 'name' not in st.session_state: st.session_state.name = ""
    if 'email' not in st.session_state: st.session_state.email = ""

init_session()

def get_current_questions():
    if st.session_state.current_section == 'mcq':
        return mcq_questions
    elif st.session_state.current_section == 'pictorial':
        return pictorial_questions
    else:
        return crossword_questions

def get_section_info():
    sections = {
        'mcq': {'name': 'AthenaHealth MCQ', 'icon': '🏥', 'color': 'badge-mcq', 'total': len(mcq_questions)},
        'pictorial': {'name': 'Pictorial Charades', 'icon': '🎨', 'color': 'badge-pictorial', 'total': len(pictorial_questions)},
        'crossword': {'name': 'AI Crossword', 'icon': '🧩', 'color': 'badge-crossword', 'total': len(crossword_questions)}
    }
    return sections[st.session_state.current_section]

def next_section():
    if st.session_state.current_section == 'mcq':
        st.session_state.current_section = 'pictorial'
        st.session_state.q_index = 0
    elif st.session_state.current_section == 'pictorial':
        st.session_state.current_section = 'crossword'
        st.session_state.q_index = 0
    else:
        st.session_state.step = 'finish'

# --- 🎯 LOGIN SCREEN ---
if st.session_state.step == 'login':
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown(f'<h1 class="quiz-title">🚀 {QUIZ_TITLE}</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align:center; margin: 2rem 0;">
        <p style="font-size: 1.1rem; color: #4a5568;">Test your knowledge across <b>3 exciting sections</b>!</p>
        <div style="margin: 1.5rem 0;">
            <span class="section-badge badge-mcq">🏥 AthenaHealth MCQ (10Q)</span>
            <span class="section-badge badge-pictorial">🎨 Pictorial Charades (10Q)</span>
            <span class="section-badge badge-crossword">🧩 AI Crossword (10Q)</span>
        </div>
        <p style="color: #718096; font-size: 0.9rem;">⏱️ Total time: 10 minutes | 📝 30 questions</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        email = st.text_input("📧 Enter your Email Address", placeholder="your.email@example.com")
        name = st.text_input("👤 Enter your Name", placeholder="Your Name")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("🎮 Start Quiz", use_container_width=True)
        
        if submitted:
            if email and name:
                st.session_state.email = email
                st.session_state.name = name
                st.session_state.start_time = time.time()
                st.session_state.step = 'quiz'
                st.rerun()
            else:
                st.warning("⚠️ Please fill in both fields!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- 📝 QUIZ SCREEN ---
elif st.session_state.step == 'quiz':
    # Timer Logic
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, QUIZ_DURATION - elapsed)
    
    if remaining <= 0:
        st.session_state.step = 'finish'
        st.rerun()
    
    questions = get_current_questions()
    section_info = get_section_info()
    total_q = len(mcq_questions) + len(pictorial_questions) + len(crossword_questions)
    
    # Calculate overall progress
    overall_progress = 0
    if st.session_state.current_section == 'mcq':
        overall_progress = st.session_state.q_index
    elif st.session_state.current_section == 'pictorial':
        overall_progress = len(mcq_questions) + st.session_state.q_index
    else:
        overall_progress = len(mcq_questions) + len(pictorial_questions) + st.session_state.q_index
    
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    # Header with Timer
    col1, col2, col3 = st.columns([2, 3, 2])
    with col1:
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        timer_class = "timer-critical" if remaining < 60 else ""
        st.markdown(f'<div style="text-align:center;"><span style="font-size:2rem; font-weight:700;" class="{timer_class}">⏱️ {minutes:02d}:{seconds:02d}</span></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<span class="section-badge {section_info["color"]}">{section_info["icon"]} {section_info["name"]}</span>', unsafe_allow_html=True)
    
    with col3:
        current_score = sum(st.session_state.scores.values())
        st.markdown(f'<div style="text-align:center;"><span style="font-size:1.5rem; font-weight:600;">🏆 {current_score}</span></div>', unsafe_allow_html=True)
    
    # Progress
    st.progress((overall_progress + 1) / total_q)
    st.caption(f"Question {overall_progress + 1} of {total_q} • Section: {st.session_state.q_index + 1}/{section_info['total']}")
    
    # Question
    q = questions[st.session_state.q_index]
    st.markdown(f"""
    <div class="question-box">
        <div class="question-text">{q['question']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Options
    choice = st.radio("Select your answer:", q['options'], index=None, key=f"q_{st.session_state.current_section}_{st.session_state.q_index}", label_visibility="collapsed")
    
    # Hint for pictorial questions
    if st.session_state.current_section == 'pictorial' and 'hint' in q:
        if st.checkbox("💡 Show Hint", key=f"hint_{st.session_state.q_index}"):
            st.markdown(f'<div class="hint-box">💡 <b>Hint:</b> {q["hint"]}</div>', unsafe_allow_html=True)
    
    # Navigation
    col1, col2 = st.columns(2)
    
    with col2:
        is_last_q = st.session_state.q_index + 1 >= len(questions)
        is_last_section = st.session_state.current_section == 'crossword'
        btn_text = "🏁 Finish Quiz" if (is_last_q and is_last_section) else ("➜ Next Section" if is_last_q else "➜ Next Question")
        
        if st.button(btn_text, type="primary", use_container_width=True):
            if choice:
                # Score the answer
                if choice == q['answer']:
                    st.session_state.scores[st.session_state.current_section] += 1
                
                # Store answer
                st.session_state.answers[f"{st.session_state.current_section}_{st.session_state.q_index}"] = choice
                
                # Navigate
                if is_last_q:
                    next_section()
                else:
                    st.session_state.q_index += 1
                st.rerun()
            else:
                st.warning("⚠️ Please select an answer!")
    
    with col1:
        if st.session_state.q_index > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.q_index -= 1
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- 🏆 FINISH SCREEN ---
elif st.session_state.step == 'finish':
    st.balloons()
    
    total_q = len(mcq_questions) + len(pictorial_questions) + len(crossword_questions)
    total_score = sum(st.session_state.scores.values())
    percentage = (total_score / total_q) * 100
    
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<h1 class="quiz-title">🎉 Quiz Complete!</h1>', unsafe_allow_html=True)
    
    # Score Display
    if percentage >= 80:
        emoji, message = "🏆", "Outstanding Performance!"
    elif percentage >= 60:
        emoji, message = "🌟", "Great Job!"
    elif percentage >= 40:
        emoji, message = "👍", "Good Effort!"
    else:
        emoji, message = "💪", "Keep Learning!"
    
    st.markdown(f"""
    <div class="score-card">
        <div style="font-size: 3rem;">{emoji}</div>
        <div class="score-big">{percentage:.0f}%</div>
        <div style="font-size: 1.5rem; margin: 0.5rem 0;">{total_score} / {total_q}</div>
        <div style="font-size: 1.2rem; opacity: 0.9;">{message}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Section Breakdown
    st.markdown("### 📊 Section Breakdown")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mcq_pct = (st.session_state.scores['mcq'] / len(mcq_questions)) * 100
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #11998e, #38ef7d); padding: 1rem; border-radius: 12px; text-align: center; color: white;">
            <div style="font-size: 0.9rem;">🏥 AthenaHealth</div>
            <div style="font-size: 1.8rem; font-weight: 700;">{st.session_state.scores['mcq']}/{len(mcq_questions)}</div>
            <div style="font-size: 0.8rem;">{mcq_pct:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        pic_pct = (st.session_state.scores['pictorial'] / len(pictorial_questions)) * 100
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ee0979, #ff6a00); padding: 1rem; border-radius: 12px; text-align: center; color: white;">
            <div style="font-size: 0.9rem;">🎨 Pictorial</div>
            <div style="font-size: 1.8rem; font-weight: 700;">{st.session_state.scores['pictorial']}/{len(pictorial_questions)}</div>
            <div style="font-size: 0.8rem;">{pic_pct:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        cross_pct = (st.session_state.scores['crossword'] / len(crossword_questions)) * 100
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4776E6, #8E54E9); padding: 1rem; border-radius: 12px; text-align: center; color: white;">
            <div style="font-size: 0.9rem;">🧩 Crossword</div>
            <div style="font-size: 1.8rem; font-weight: 700;">{st.session_state.scores['crossword']}/{len(crossword_questions)}</div>
            <div style="font-size: 0.8rem;">{cross_pct:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="text-align: center; margin-top: 2rem; padding: 1rem; background: #f7fafc; border-radius: 12px;">
        <p style="color: #4a5568;">Thanks for playing, <b>{st.session_state.get('name', st.session_state.email)}</b>! 🙌</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Play Again", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
