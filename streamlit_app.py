import streamlit as st
from datetime import datetime
from html import escape
import re

# ============================================================
# AI STUDY ASSISTANT - COMPLETE STREAMLIT FRONTEND
# ============================================================

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# Session state
# ------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"

if "question_input" not in st.session_state:
    st.session_state.question_input = ""


# ------------------------------------------------------------
# Demo answer
# IMPORTANT:
# Replace this function later with your real RAG pipeline.
# ------------------------------------------------------------
def clean_answer(answer: str):
    """Remove HTML/code markup from an answer before displaying it."""
    text = str(answer)
    text = re.sub(r"```(?:html|HTML)?", "", text)
    text = text.replace("```", "")
    text = re.sub(r"<[^>]*>", "", text)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def get_answer(question: str):
    q = question.lower().strip()

    if "artificial intelligence" in q:
        return (
            "Artificial Intelligence (AI) is the ability of machines or computer "
            "systems to perform tasks that normally require human intelligence, "
            "such as understanding information, learning from data, reasoning, "
            "and making decisions."
        )

    if "machine learning" in q:
        return (
            "Machine Learning (ML) is a branch of Artificial Intelligence in which "
            "computers learn patterns from data and use those patterns to make "
            "predictions or decisions without being explicitly programmed for "
            "every individual task."
        )

    if "supervised learning" in q:
        return (
            "Supervised learning is a machine learning method in which a model "
            "learns from labeled training data. The model learns the relationship "
            "between inputs and known outputs and then uses that knowledge to "
            "predict outputs for new data."
        )

    return (
        "I found relevant information for your question. Connect your existing "
        "RAG retrieval and LLM functions to the get_answer() function to return "
        "answers from your uploaded study documents."
    )


# ------------------------------------------------------------
# CSS
# ------------------------------------------------------------
st.markdown(
    """
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", Arial, sans-serif;
}

.stApp {
    background: #f7faff;
}

#MainMenu, footer {
    visibility: hidden;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    display: none;
}

/* ================= SIDEBAR ================= */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1a33 0%, #101f3d 100%);
    min-width: 325px;
    max-width: 325px;
    border-right: 0;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 0;
}

.sidebar-content {
    padding: 28px 24px 22px 24px;
    min-height: 100vh;
    color: white;
}

.brand {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 32px;
}

.brand-icon {
    font-size: 39px;
    line-height: 1;
}

.brand-title {
    color: white;
    font-size: 22px;
    font-weight: 800;
    line-height: 1.1;
}

.brand-subtitle {
    color: #b8c7e3;
    font-size: 13px;
    margin-top: 6px;
}

.nav-title {
    color: #ffffff;
    font-size: 14px;
    font-weight: 700;
    margin: 18px 0 10px 12px;
}

/* Radio navigation */
[data-testid="stSidebar"] [data-testid="stRadio"] {
    width: 100%;
}

[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 5px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    color: #eaf0fb !important;
    background: transparent;
    border-radius: 9px;
    padding: 10px 12px;
    min-height: 43px;
    font-size: 14px;
    font-weight: 650;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(65, 105, 170, 0.35);
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: #31598f !important;
    color: white !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    color: inherit !important;
}

.sidebar-divider {
    height: 1px;
    background: rgba(255,255,255,.14);
    margin: 20px 0;
}

[data-testid="stSidebar"] .clear-chat button {
    width: 100%;
    min-height: 44px;
    background: white !important;
    color: #31435e !important;
    border: 0 !important;
    border-radius: 9px !important;
    font-weight: 650 !important;
}

[data-testid="stSidebar"] .clear-chat button:hover {
    background: #edf3fb !important;
}

.status-box {
    margin-top: 24px;
    background: #213e70;
    border-radius: 12px;
    padding: 17px 16px;
}

.status-row {
    display: flex;
    align-items: center;
    gap: 10px;
    color: white;
    font-size: 14px;
    font-weight: 750;
}

.status-dot {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #27d993;
    box-shadow: 0 0 10px rgba(39,217,147,.35);
}

.status-sub {
    color: #c3d1e8;
    font-size: 12px;
    margin: 7px 0 0 24px;
}

.production-box {
    margin-top: 18px;
    padding-top: 17px;
    border-top: 1px solid rgba(255,255,255,.14);
}

.production-title {
    color: white;
    font-size: 13px;
    font-weight: 700;
}

.production-sub {
    color: #b6c4dd;
    font-size: 12px;
    margin-top: 5px;
}

/* ================= MAIN ================= */

.main-shell {
    padding: 18px 34px 35px 34px;
}

.hero {
    min-height: 135px;
    border-radius: 14px;
    padding: 22px 32px;
    background: linear-gradient(100deg, #e2f3ff 0%, #f0efff 50%, #ebe8ff 100%);
    border: 1px solid #d4e4f7;
    box-shadow: 0 4px 16px rgba(36,79,130,.07);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.hero-left {
    display: flex;
    align-items: center;
    gap: 27px;
}

.hero-book {
    font-size: 68px;
}

.hero-title {
    color: #132b52;
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -1.2px;
}

.hero-subtitle {
    color: #315072;
    font-size: 16px;
    margin-top: 8px;
}

.powered {
    background: rgba(255,255,255,.48);
    border-radius: 25px;
    padding: 11px 18px;
    color: #1764cf;
    font-weight: 700;
    font-size: 14px;
    white-space: nowrap;
}

.card {
    background: rgba(255,255,255,.95);
    border: 1px solid #e0e7f2;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(27,63,105,.045);
}

.welcome {
    margin-top: 17px;
    padding: 20px 24px;
    display: flex;
    align-items: flex-start;
    gap: 18px;
}

.welcome-icon {
    width: 43px;
    height: 43px;
    min-width: 43px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #e9f2ff;
    color: #1674e9;
    font-size: 23px;
}

.welcome-title {
    color: #18345e;
    font-size: 19px;
    font-weight: 750;
}

.welcome-main {
    color: #29415f;
    font-size: 15px;
    line-height: 1.55;
    margin-top: 3px;
}

.welcome-small {
    color: #6a82a3;
    font-size: 14px;
    margin-top: 3px;
}

.section-title {
    display: flex;
    align-items: center;
    gap: 13px;
    margin: 22px 0 10px 5px;
    color: #17355f;
    font-size: 18px;
    font-weight: 750;
}

.example-icon {
    font-size: 25px;
}

.example-button button {
    background: #eef6ff !important;
    border: 1px solid #d3e4fa !important;
    color: #1264c7 !important;
    min-height: 49px !important;
    border-radius: 9px !important;
}

.example-button button:hover {
    background: #e2efff !important;
}

.ask-card {
    margin-top: 18px;
}

.ask-heading {
    padding: 16px 18px 8px 18px;
    color: #17355f;
    font-size: 17px;
    font-weight: 750;
}

.stTextInput > div > div > input {
    height: 53px !important;
    border-radius: 11px !important;
    border: 1px solid #cbd9eb !important;
    background: white !important;
    color: #29415f !important;
    font-size: 14px !important;
    padding-left: 16px !important;
}

.answer-button button {
    min-height: 53px !important;
    background: #ff4b4b !important;
    color: white !important;
    border: 0 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
}

/* ================= CHAT ================= */

.chat-card {
    margin-top: 15px;
    padding: 20px 24px 24px 24px;
}

.user-bubble {
    max-width: 390px;
    margin-left: auto;
    background: linear-gradient(100deg,#e8f2ff,#dceaff);
    border: 1px solid #cbdff8;
    border-radius: 12px;
    padding: 12px 17px;
    color: #2363b6;
    font-weight: 650;
    font-size: 14px;
}

.message-time {
    text-align: right;
    color: #7790af;
    font-size: 11px;
    margin-top: 5px;
    margin-right: 7px;
}

.ai-answer {
    max-width: 82%;
    margin-top: 16px;
    background: #effcf8;
    border: 1px solid #cdeee2;
    border-radius: 11px;
    padding: 17px 20px;
}

.ai-header {
    color: #159b70;
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 8px;
}

.ai-text {
    color: #34516d;
    font-size: 14px;
    line-height: 1.65;
    white-space: normal;
    overflow-wrap: anywhere;
}

.meta {
    display: flex;
    gap: 22px;
    margin-top: 13px;
    color: #66819d;
    font-size: 12px;
}

.features {
    margin-top: 18px;
    display: grid;
    grid-template-columns: repeat(4,1fr);
    border-radius: 12px;
    overflow: hidden;
    background: rgba(255,255,255,.82);
    border: 1px solid #e4eaf3;
}

.feature {
    padding: 18px 20px;
    display: flex;
    align-items: center;
    gap: 13px;
    border-right: 1px solid #edf0f5;
}

.feature:last-child {
    border-right: none;
}

.feature-icon {
    width: 43px;
    height: 43px;
    min-width: 43px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #edf5ff;
    color: #1673e8;
    font-size: 20px;
}

.feature-title {
    color: #4e6380;
    font-size: 13px;
    font-weight: 700;
}

.feature-sub {
    color: #6f86a3;
    font-size: 12px;
    margin-top: 4px;
}

/* ================= OTHER PAGES ================= */

.page-panel {
    margin-top: 18px;
    padding: 25px;
    background: white;
    border: 1px solid #e0e7f2;
    border-radius: 12px;
}

.page-panel h2 {
    color: #17355f;
    margin-top: 0;
}

.page-panel p,
.page-panel li {
    color: #536b88;
    line-height: 1.6;
}

@media (max-width: 1050px) {
    .powered {
        display: none;
    }

    .features {
        grid-template-columns: repeat(2,1fr);
    }
}

@media (max-width: 700px) {
    [data-testid="stSidebar"] {
        min-width: 280px;
        max-width: 280px;
    }

    .main-shell {
        padding: 10px 12px 20px 12px;
    }

    .hero {
        padding: 18px;
    }

    .hero-title {
        font-size: 27px;
    }

    .hero-book {
        font-size: 48px;
    }

    .features {
        grid-template-columns: 1fr;
    }

    .feature {
        border-right: none;
        border-bottom: 1px solid #edf0f5;
    }

    .ai-answer {
        max-width: 100%;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
<div class="sidebar-content">
    <div class="brand">
        <div class="brand-icon">📖</div>
        <div>
            <div class="brand-title">AI Study Assistant</div>
            <div class="brand-subtitle">Your PDF Study Companion</div>
        </div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="nav-title">Navigation</div>', unsafe_allow_html=True)

    page_options = [
        "⌂ Home",
        "ⓘ About",
        "▤ Document Tracking System",
        "⌕ Hybrid Retrieval System",
        "⚙ System Information",
    ]

    current_display = {
        "Home": "⌂ Home",
        "About": "ⓘ About",
        "Document Tracking System": "▤ Document Tracking System",
        "Hybrid Retrieval System": "⌕ Hybrid Retrieval System",
        "System Information": "⚙ System Information",
    }.get(st.session_state.active_page, "⌂ Home")

    selected_display = st.radio(
        "Navigation",
        page_options,
        index=page_options.index(current_display),
        label_visibility="collapsed",
        key="navigation_radio",
    )

    display_to_page = {
        "⌂ Home": "Home",
        "ⓘ About": "About",
        "▤ Document Tracking System": "Document Tracking System",
        "⌕ Hybrid Retrieval System": "Hybrid Retrieval System",
        "⚙ System Information": "System Information",
    }

    new_page = display_to_page[selected_display]

    if new_page != st.session_state.active_page:
        st.session_state.active_page = new_page
        st.rerun()

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="clear-chat">', unsafe_allow_html=True)
    if st.button("♲  Clear Chat", use_container_width=True, key="clear_chat_button"):
        st.session_state.messages = []
        st.session_state.question_input = ""
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
<div class="status-box">
    <div class="status-row">
        <span class="status-dot"></span>
        <span>System Online</span>
    </div>
    <div class="status-sub">Ready to answer your questions</div>
</div>

<div class="production-box">
    <div class="production-title">✦ Production RAG System</div>
    <div class="production-sub">Hybrid Retrieval • Local LLM</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# MAIN
# ============================================================

st.markdown('<div class="main-shell">', unsafe_allow_html=True)

page = st.session_state.active_page


# ============================================================
# HOME
# ============================================================

if page == "Home":

    st.markdown(
        """
<div class="hero">
    <div class="hero-left">
        <div class="hero-book">📚</div>
        <div>
            <div class="hero-title">AI Study Assistant</div>
            <div class="hero-subtitle">Ask questions from your PDF study materials using Retrieval-Augmented Generation.</div>
        </div>
    </div>
    <div class="powered">🔗 &nbsp; Powered by RAG + Llama 3</div>
</div>

<div class="card welcome">
    <div class="welcome-icon">✦</div>
    <div>
        <div class="welcome-title">Welcome!</div>
        <div class="welcome-main">I'm your AI study assistant. Ask me anything from your uploaded PDF documents.</div>
        <div class="welcome-small">I will search through your study materials, find relevant information and give you accurate answers.</div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="section-title">
    <span class="example-icon">♧</span>
    <span>Example Questions</span>
</div>
""",
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3, gap="small")

    with c1:
        st.markdown('<div class="example-button">', unsafe_allow_html=True)
        if st.button(
            "What is Artificial Intelligence? ›",
            key="example_ai",
            use_container_width=True,
        ):
            st.session_state.question_input = "What is Artificial Intelligence?"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="example-button">', unsafe_allow_html=True)
        if st.button(
            "What is Machine Learning? ›",
            key="example_ml",
            use_container_width=True,
        ):
            st.session_state.question_input = "What is Machine Learning?"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="example-button">', unsafe_allow_html=True)
        if st.button(
            "What is supervised learning? ›",
            key="example_sl",
            use_container_width=True,
        ):
            st.session_state.question_input = "What is supervised learning?"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
<div class="card ask-card">
    <div class="ask-heading">▣ &nbsp; Ask your question</div>
</div>
""",
        unsafe_allow_html=True,
    )

    input_col, button_col = st.columns([5.8, 1], gap="small")

    with input_col:
        question = st.text_input(
            "Question",
            value=st.session_state.question_input,
            placeholder="Type your question about the study material...",
            label_visibility="collapsed",
            key="question_box",
        )

    with button_col:
        st.markdown('<div class="answer-button">', unsafe_allow_html=True)
        ask_clicked = st.button(
            "➤  Get Answer",
            use_container_width=True,
            key="get_answer_button",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    if ask_clicked and question.strip():
        answer = get_answer(question.strip())
        now = datetime.now().strftime("%I:%M %p").lstrip("0")

        st.session_state.messages.append(
            {
                "question": question.strip(),
                "answer": answer,
                "time": now,
            }
        )

        st.session_state.question_input = ""

    # --------------------------------------------------------
    # CHAT RESULTS
    #
    # IMPORTANT:
    # The HTML is deliberately NOT indented inside the
    # triple-quoted string. This prevents Streamlit from
    # displaying the HTML tags as a code block.
    #
    # The answer is also HTML-escaped so an answer containing
    # <div>, <p>, etc. can never become visible HTML code.
    # --------------------------------------------------------

    for msg in st.session_state.messages:
        safe_question = escape(str(msg["question"]))
        safe_answer = escape(clean_answer(msg["answer"]))
        safe_time = escape(str(msg["time"]))

        st.markdown(
            f"""<div class="card chat-card"><div class="user-bubble">👤 &nbsp; {safe_question}</div><div class="message-time">{safe_time}</div><div class="ai-answer"><div class="ai-header">🤖 &nbsp; AI Answer</div><div class="ai-text">{safe_answer}</div><div class="meta"><span>◷ &nbsp; Response time: 2.34s</span><span>▣ &nbsp; Retrieved documents: 3</span></div></div></div>""",
            unsafe_allow_html=True,
        )

    st.markdown(
        """
<div class="features">
    <div class="feature">
        <div class="feature-icon">⌕</div>
        <div>
            <div class="feature-title">Hybrid Retrieval</div>
            <div class="feature-sub">BM25 + Vector Search</div>
        </div>
    </div>

    <div class="feature">
        <div class="feature-icon">♧</div>
        <div>
            <div class="feature-title">Local LLM</div>
            <div class="feature-sub">Ollama + Llama 3</div>
        </div>
    </div>

    <div class="feature">
        <div class="feature-icon">▤</div>
        <div>
            <div class="feature-title">Vector Database</div>
            <div class="feature-sub">ChromaDB</div>
        </div>
    </div>

    <div class="feature">
        <div class="feature-icon">♥</div>
        <div>
            <div class="feature-title">Built with</div>
            <div class="feature-sub">Python &amp; Streamlit</div>
        </div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# ABOUT
# ============================================================

elif page == "About":
    st.markdown(
        """
<div class="hero">
    <div class="hero-left">
        <div class="hero-book">📚</div>
        <div>
            <div class="hero-title">About</div>
            <div class="hero-subtitle">AI Study Assistant</div>
        </div>
    </div>
</div>

<div class="page-panel">
    <h2>AI Study Assistant</h2>
    <p>This application allows students to ask questions about PDF study materials using Retrieval-Augmented Generation (RAG).</p>
    <ul>
        <li>PDF-based question answering</li>
        <li>Hybrid BM25 + vector retrieval</li>
        <li>ChromaDB vector database</li>
        <li>Local LLM support with Ollama and Llama 3</li>
        <li>Streamlit chatbot interface</li>
    </ul>
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# DOCUMENT TRACKING
# ============================================================

elif page == "Document Tracking System":
    st.markdown(
        """
<div class="hero">
    <div class="hero-left">
        <div class="hero-book">📄</div>
        <div>
            <div class="hero-title">Document Tracking System</div>
            <div class="hero-subtitle">Manage your PDF study materials</div>
        </div>
    </div>
</div>

<div class="page-panel">
    <h2>📄 Study Documents</h2>
    <p>Connect this page to your existing document ingestion and PDF processing pipeline.</p>
    <p>The project can process PDFs, clean text, split content into chunks, create embeddings and store vectors for retrieval.</p>
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# HYBRID RETRIEVAL
# ============================================================

elif page == "Hybrid Retrieval System":
    st.markdown(
        """
<div class="hero">
    <div class="hero-left">
        <div class="hero-book">🔎</div>
        <div>
            <div class="hero-title">Hybrid Retrieval System</div>
            <div class="hero-subtitle">BM25 + Vector Search</div>
        </div>
    </div>
</div>

<div class="page-panel">
    <h2>Hybrid Retrieval</h2>
    <ul>
        <li><b>BM25:</b> keyword-based retrieval for exact terms.</li>
        <li><b>Vector Search:</b> semantic retrieval using embeddings.</li>
        <li><b>Hybrid Search:</b> combines keyword and semantic retrieval.</li>
        <li><b>Reranking:</b> retrieved chunks can be ranked again before generation.</li>
    </ul>
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# SYSTEM INFORMATION
# ============================================================

elif page == "System Information":
    st.markdown(
        """
<div class="hero">
    <div class="hero-left">
        <div class="hero-book">⚙️</div>
        <div>
            <div class="hero-title">System Information</div>
            <div class="hero-subtitle">AI Study Assistant configuration</div>
        </div>
    </div>
</div>

<div class="page-panel">
    <h2>System Information</h2>
    <ul>
        <li><b>Frontend:</b> Streamlit</li>
        <li><b>RAG:</b> Retrieval-Augmented Generation</li>
        <li><b>Retrieval:</b> BM25 + Vector Search</li>
        <li><b>Vector Database:</b> ChromaDB</li>
        <li><b>Local LLM:</b> Ollama + Llama 3</li>
        <li><b>Language:</b> Python</li>
    </ul>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)
