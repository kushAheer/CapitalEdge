import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="CoinWise — Bank Statement AI",
    
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 1rem; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #f8f9fa;
    border-right: 1px solid #e9ecef;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem;
}

/* Brand header */
.brand-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1.5rem;
}

.brand-icon {
    width: 36px; height: 36px;
    background: #0F6E56;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}

.brand-name {
    font-size: 20px;
    font-weight: 600;
    color: #0F6E56;
    letter-spacing: -0.3px;
}

/* Status badge */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #E1F5EE;
    color: #0F6E56;
    padding: 4px 10px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 500;
    margin-bottom: 1rem;
}

.status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #1D9E75;
}

/* File info card */
.file-card {
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 1rem;
    font-size: 13px;
}

.file-card-name {
    font-weight: 500;
    color: #212529;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.file-card-meta {
    color: #868e96;
    font-size: 12px;
    margin-top: 3px;
    font-family: 'DM Mono', monospace;
}

/* Chat messages */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 0.5rem 0;
}

.msg-user {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    align-items: flex-start;
}

.msg-bot {
    display: flex;
    justify-content: flex-start;
    gap: 8px;
    align-items: flex-start;
}

.avatar {
    width: 30px; height: 30px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px;
    font-weight: 600;
    flex-shrink: 0;
}

.avatar-user {
    background: #EEEDFE;
    color: #534AB7;
}

.avatar-bot {
    background: #E1F5EE;
    color: #0F6E56;
}

.bubble-user {
    background: #0F6E56;
    color: #E1F5EE;
    padding: 10px 14px;
    border-radius: 16px 16px 4px 16px;
    font-size: 14px;
    line-height: 1.55;
    max-width: 75%;
}

.bubble-bot {
    background: white;
    border: 1px solid #e9ecef;
    color: #212529;
    padding: 10px 14px;
    border-radius: 16px 16px 16px 4px;
    font-size: 14px;
    line-height: 1.55;
    max-width: 75%;
}

/* Page title */
.page-title {
    font-size: 22px;
    font-weight: 600;
    color: #212529;
    letter-spacing: -0.3px;
    margin-bottom: 4px;
}

.page-sub {
    font-size: 14px;
    color: #868e96;
    margin-bottom: 1.25rem;
}

/* Quick chips */
.chips-label {
    font-size: 12px;
    font-weight: 500;
    color: #868e96;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
}

/* Strimlit button override for chips */
div[data-testid="column"] .stButton > button {
    background: white !important;
    color: #495057 !important;
    border: 1px solid #dee2e6 !important;
    border-radius: 99px !important;
    font-size: 12px !important;
    padding: 4px 14px !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.15s !important;
}

div[data-testid="column"] .stButton > button:hover {
    background: #E1F5EE !important;
    border-color: #5DCAA5 !important;
    color: #0F6E56 !important;
}

/* Send button */
.stButton > button[kind="primary"] {
    background: #0F6E56 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
}

.stButton > button[kind="primary"]:hover {
    background: #1D9E75 !important;
}

/* Divider */
hr { border-color: #e9ecef; }

/* Input */
.stTextInput > div > div > input, .stTextArea textarea {
    border-radius: 10px !important;
    border: 1px solid #dee2e6 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
}

.stTextInput > div > div > input:focus, .stTextArea textarea:focus {
    border-color: #1D9E75 !important;
    box-shadow: 0 0 0 2px #E1F5EE !important;
}

/* Success/info message */
.stSuccess, .stInfo {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Spinner */
.stSpinner > div { border-top-color: #0F6E56 !important; }

/* Empty state */
.empty-state {
    text-align: center;
    padding: 3rem 2rem;
    color: #868e96;
}

.empty-state .emoji { font-size: 40px; margin-bottom: 1rem; }
.empty-state p { font-size: 14px; line-height: 1.6; max-width: 280px; margin: 0 auto; }
</style>
""", unsafe_allow_html=True)



@st.cache_resource(show_spinner=False)
def get_chatbot():
    from ai import ChatBot
    return ChatBot()



if "messages" not in st.session_state:
    st.session_state.messages = []
if "doc_loaded" not in st.session_state:
    st.session_state.doc_loaded = False
if "doc_name" not in st.session_state:
    st.session_state.doc_name = ""
if "doc_size" not in st.session_state:
    st.session_state.doc_size = ""



with st.sidebar:
    st.markdown("""
    <div class="brand-header">
        <div class="brand-icon">🏦</div>
        <div class="brand-name">CoinWise</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="status-badge">
        <div class="status-dot"></div>
        AI ready
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Upload statement**")
    uploaded_file = st.file_uploader(
        label="Bank statement PDF",
        type=["pdf"],
        label_visibility="collapsed",
        help="Upload your bank statement PDF to begin chatting"
    )

    if uploaded_file and not st.session_state.doc_loaded:
        with st.spinner("Indexing document…"):
            try:
                bot = get_chatbot()
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name

                bot.load_document(tmp_path)
                bot.split_document()
                bot.embed_and_store()
                os.unlink(tmp_path)

                st.session_state.doc_loaded = True
                st.session_state.doc_name = uploaded_file.name
                size_kb = round(uploaded_file.size / 1024)
                st.session_state.doc_size = f"{size_kb} KB"
                st.session_state.messages = [{
                    "role": "assistant",
                    "content": f"I've indexed **{uploaded_file.name}**. Ask me anything about your finances — transactions, balances, spending patterns, or recurring payments."
                }]
                st.rerun()
            except Exception as e:
                st.error(f"Failed to process document: {e}")

    if st.session_state.doc_loaded:
        st.markdown(f"""
        <div class="file-card">
            <div class="file-card-name">📄 {st.session_state.doc_name}</div>
            <div class="file-card-meta">{st.session_state.doc_size} · indexed</div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        if st.button("🗑 Clear & start over", use_container_width=True):
            st.session_state.messages = []
            st.session_state.doc_loaded = False
            st.session_state.doc_name = ""
            st.session_state.doc_size = ""
            st.rerun()

    st.divider()
    st.markdown("""
    <div style="font-size: 12px; color: #868e96; line-height: 1.6;">
        Powered by <strong>Groq · LLaMA 3.3</strong><br>
        Indexed via <strong>Pinecone</strong><br>
        Embeddings by <strong>multilingual-e5-large</strong>
    </div>
    """, unsafe_allow_html=True)


st.markdown('<div class="page-title">Bank Statement AI</div>', unsafe_allow_html=True)

if st.session_state.doc_loaded:
    st.markdown(f'<div class="page-sub">Chatting with <strong>{st.session_state.doc_name}</strong></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="page-sub">Upload a PDF in the sidebar to get started</div>', unsafe_allow_html=True)



if st.session_state.doc_loaded:
    st.markdown('<div class="chips-label">Quick questions</div>', unsafe_allow_html=True)
    chips = [
        "Total credits this month",
        "Largest transaction",
        "Spending by category",
        "Recurring payments",
        "Closing balance",
        "Any unusual transactions?",
    ]
    cols = st.columns(len(chips))
    chip_clicked = None
    for col, chip in zip(cols, chips):
        with col:
            if st.button(chip, key=f"chip_{chip}"):
                chip_clicked = chip

chat_placeholder = st.container()

with chat_placeholder:
    if not st.session_state.messages and not st.session_state.doc_loaded:
        st.markdown("""
        <div class="empty-state">
            <div class="emoji">🏦</div>
            <p>Upload your bank statement PDF in the sidebar and ask anything about your finances.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="msg-user">
                    <div class="bubble-user">{msg["content"]}</div>
                    <div class="avatar avatar-user">You</div>
                </div>
                <br>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="msg-bot">
                    <div class="avatar avatar-bot">CW</div>
                    <div class="bubble-bot">{msg["content"]}</div>
                </div>
                <br>
                """, unsafe_allow_html=True)


st.divider()

if st.session_state.doc_loaded:
    col_input, col_btn = st.columns([6, 1])
    with col_input:
        user_input = st.text_input(
            label="Message",
            label_visibility="collapsed",
            placeholder="Ask about your statement…",
            key="user_input",
            disabled=not st.session_state.doc_loaded,
        )
    with col_btn:
        send = st.button("Send →", type="primary", use_container_width=True)

    query = chip_clicked or (user_input if send and user_input.strip() else None)

    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.spinner("Thinking…"):
            try:
                bot = get_chatbot()
                answer = bot.chat(query)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Sorry, I ran into an error: {e}"
                })
        st.rerun()
else:
    st.text_input(
        label="Message",
        label_visibility="collapsed",
        placeholder="Upload a statement to start chatting…",
        disabled=True,
    )