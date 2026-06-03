"""
Embedded Multimodal AI Legal Assistance System
FINAL PREMIUM VERSION (Login + Register + Dashboard + Multilingual)
"""

import streamlit as st
import json
import os
from lawbot_engine import get_nyaysetu
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile

# ---------------- FILE STORAGE ----------------
USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# ---------------- PAGE ----------------
st.set_page_config(page_title="Legal AI System", page_icon="⚖️", layout="wide")

# ---------------- MODERN STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    font-family: 'Segoe UI', sans-serif;
}

.title {
    text-align: center;
    font-size: 32px;
    font-weight: 600;
    margin-bottom: 20px;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-size: 15px;
    font-weight: 500;
    background: linear-gradient(90deg,#3b82f6,#6366f1);
    color: white;
    border: none;
}

.stButton>button:hover {
    background: linear-gradient(90deg,#2563eb,#4f46e5);
}

.stTextInput>div>div>input {
    border-radius: 10px;
    height: 45px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "nyaysetu" not in st.session_state:
    st.session_state.nyaysetu = get_nyaysetu()

# ---------------- LOGIN / REGISTER ----------------
if not st.session_state.logged_in:

    st.markdown("<div class='title'>⚖️ Legal AI Assistant</div>", unsafe_allow_html=True)

    users = load_users()

    tabs = st.tabs(["🔐 Login", "📝 Register"])

    # LOGIN TAB
    with tabs[0]:
        st.subheader("Welcome Back")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password")

        if st.button("Continue as Guest"):
            st.session_state.logged_in = True
            st.session_state.username = "Guest"
            st.success("Logged in as Guest")
            st.rerun()

    # REGISTER TAB
    with tabs[1]:
        st.subheader("Create Account")

        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Register"):
            if new_user in users:
                st.warning("User already exists")
            else:
                users[new_user] = new_pass
                save_users(users)
                st.success("Registered successfully")

    st.stop()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    if st.session_state.username == "Guest":
        st.write("👤 Guest User")
    else:
        st.write(f"👤 {st.session_state.username}")

    mode = st.selectbox("⚙ Mode", ["Edge (Offline)", "Cloud (Online)"])

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.chat_history = []
        st.rerun()

# ---------------- HEADER ----------------
st.markdown("## ⚙️ Embedded Multimodal Legal AI System")

st.markdown("""
### Ask Legal Questions Instantly  
Edge AI (offline) + Cloud AI (advanced)
""")

# ---------------- LANGUAGE ----------------
language = st.selectbox("🌐 Language", [
    "English","Hindi","Telugu","Kannada","Malayalam","Marathi","Tamil","Bengali"
])

lang_map = {
    "English":"en","Hindi":"hi","Telugu":"te","Kannada":"kn",
    "Malayalam":"ml","Marathi":"mr","Tamil":"ta","Bengali":"bn"
}

# ---------------- QUICK ACTIONS ----------------
st.markdown("### ⚡ Quick Actions")

c1, c2, c3 = st.columns(3)

if c1.button("FIR Help"):
    st.session_state.q = "Police is not registering my FIR, what should I do?"

if c2.button("Property Fraud"):
    st.session_state.q = "I bought land but seller cheated me, what should I do?"

if c3.button("Land Dispute"):
    st.session_state.q = "My neighbor occupied my land illegally, what should I do?"

# ---------------- CHAT ----------------
if not st.session_state.chat_history:
    st.info("💬 Start asking your legal question below...")

for sender, msg in st.session_state.chat_history:
    with st.chat_message("user" if sender=="User" else "assistant"):
        st.write(msg)

user_input = st.chat_input("Ask your legal question...")

if "q" in st.session_state:
    user_input = st.session_state.q
    del st.session_state.q

# ---------------- INTENT ----------------
def detect_intent(q):
    q = q.lower()
    if "fraud" in q or "cheat" in q:
        return "IPC 420"
    if "fir" in q or "police" in q:
        return "FIR"
    if "land" in q or "property" in q:
        return "Property Law"
    return "General"

# ---------------- EDGE DB ----------------
legal_db = {
    "FIR": """If police refuse FIR:
1. Approach SP under Sec 154(3) CrPC
2. File complaint to Magistrate (156(3))
3. Send complaint to higher authorities
You can approach court.""",

    "IPC 420": """Cheating case:
- File FIR
- Collect evidence
- Punishment up to 7 years""",

    "Property Law": """Property dispute:
- Verify ownership documents
- File civil case
- Apply injunction"""
}

# ---------------- PROCESS ----------------
if user_input:

    intent = detect_intent(user_input)

    translated_input = user_input
    if language != "English":
        try:
            translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)
        except:
            pass

    if mode == "Edge (Offline)":
        answer = legal_db.get(intent, "Please provide more details.")
    else:
        answer = st.session_state.nyaysetu.ask(translated_input, [])

    if language != "English":
        try:
            translated = GoogleTranslator(source='en', target=lang_map[language]).translate(answer[:300])
            answer = f"🔹 English:\n{answer}\n\n🔹 {language}:\n{translated}"
        except:
            pass

    st.session_state.chat_history.append(("User", user_input))
    st.session_state.chat_history.append(("AI", answer))

    st.rerun()

# ---------------- VOICE ----------------
if st.session_state.chat_history:
    if st.button("🔊 Speak Last Answer"):
        text = st.session_state.chat_history[-1][1]
        try:
            tts = gTTS(text=text, lang=lang_map[language])
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                tts.save(f.name)
                st.audio(open(f.name, "rb").read())
        except:
            st.error("Voice error")

# ---------------- FOOTER ----------------
st.warning("⚠ General legal info only. Not legal advice.")
st.caption("Legal AI System | FINAL VERSION 🚀")
