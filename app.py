
import streamlit as st
import time

from summarizer import TextSummarizer


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Sumi AI | Text Summarizer",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "summary" not in st.session_state:
    st.session_state.summary = None

if "processing_time" not in st.session_state:
    st.session_state.processing_time = 0

if "original_words" not in st.session_state:
    st.session_state.original_words = 0


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --primary: #7657E8;
    --primary-dark: #6241D8;
    --background: #F7F7FC;
    --text: #20213A;
    --muted: #85869C;
    --border: #EBEAF3;
}

.stApp {
    background: var(--background);
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Hide Streamlit branding */

#MainMenu, footer {
    visibility: hidden;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] * {
    color: var(--text);
}

/* Header */

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 25px;
}

.brand-icon {
    background: linear-gradient(135deg, #8567F5, #6140D8);
    color: white !important;
    width: 48px;
    height: 48px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 25px;
    box-shadow: 0 7px 18px rgba(118,87,232,.25);
}

.brand-name {
    font-size: 23px;
    font-weight: 800;
    color: var(--text);
}

.brand-name span {
    color: var(--primary);
}

.hero {
    background: linear-gradient(120deg, #FFFFFF 5%, #F0EDFF 100%);
    border: 1px solid #E9E3FF;
    border-radius: 24px;
    padding: 35px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}

.hero-tag {
    display: inline-block;
    background: #E8E1FF;
    color: #6948D9 !important;
    border-radius: 30px;
    padding: 7px 14px;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 14px;
}

.hero h1 {
    color: #20213A;
    font-size: 38px;
    font-weight: 800;
    margin: 0;
    line-height: 1.25;
}

.hero h1 span {
    color: #7657E8;
}

.hero p {
    color: #77788F;
    font-size: 15px;
    margin-top: 12px;
}

/* Section headings */

.section-heading {
    color: #20213A;
    font-size: 19px;
    font-weight: 700;
    margin-bottom: 12px;
}

/* Input */

.stTextArea textarea {
    background: #FFFFFF !important;
    border: 1px solid #E5E3EF !important;
    border-radius: 15px !important;
    color: #25263D !important;
    font-size: 15px !important;
    line-height: 1.7 !important;
    padding: 17px !important;
}

.stTextArea textarea:focus {
    border: 1px solid #896EF0 !important;
    box-shadow: 0 0 0 3px rgba(118,87,232,.10) !important;
}

/* Selectbox */

.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px;
}

/* Buttons */

.stButton > button {
    border-radius: 12px;
    height: 49px;
    font-weight: 700;
    border: none;
    transition: all .2s ease;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(110deg, #8062F0, #6241D8);
    color: white;
    box-shadow: 0 6px 15px rgba(118,87,232,.20);
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(110deg, #6948E0, #5030C4);
    transform: translateY(-2px);
}

/* Metrics */

div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #ECEAF4;
    border-radius: 15px;
    padding: 17px;
}

[data-testid="stMetricLabel"] {
    color: #85869C !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #25263D !important;
    font-weight: 800;
}

/* Summary */

.summary-card {
    background: #FFFFFF;
    border: 1px solid #E9E5F5;
    border-left: 4px solid #7657E8;
    border-radius: 15px;
    padding: 25px;
    color: #30314A;
    line-height: 1.9;
    font-size: 15px;
    box-shadow: 0 5px 20px rgba(30,30,70,.035);
    white-space: pre-wrap;
}

/* Footer */

.footer {
    text-align: center;
    padding: 25px 0;
    color: #9999AB;
    font-size: 12px;
}

hr {
    border-color: #EAE8F2;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# MODEL
# --------------------------------------------------

@st.cache_resource
def load_model():
    return TextSummarizer()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("""
    <div class="brand">
        <div class="brand-icon">✦</div>
        <div class="brand-name">Sumi<span>AI</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚙️ Preferences")

    summary_length = st.selectbox(
        "Summary Length",
        ["Short", "Medium", "Long"],
        index=1
    )

    st.caption(
        "Choose how detailed your summary should be."
    )

    st.divider()

    st.markdown("### 🤖 AI Engine")

    st.info("DistilBART CNN")

    st.markdown("### 🛠️ Powered By")

    st.markdown("""
    - 🐍 Python
    - 🤗 Hugging Face
    - 🔥 PyTorch
    - 🎈 Streamlit
    """)

    st.divider()

    st.caption("DAY 11 / 30 DAYS – 30 AI PROJECTS")

    if st.button("🗑️ Clear Results"):
        st.session_state.summary = None
        st.session_state.processing_time = 0
        st.session_state.original_words = 0
        st.rerun()


# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-tag">✦ YOUR AI WRITING ASSISTANT</div>
    <h1>Less Reading.<br><span>More Understanding.</span></h1>
    <p>
        Transform lengthy articles, documents and notes into
        clear, meaningful summaries with AI.
    </p>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">📄 Your Content</div>',
    unsafe_allow_html=True
)

input_text = st.text_area(
    "Input Text",
    height=250,
    placeholder="Paste your article, research paper, notes or any lengthy content here...",
    label_visibility="collapsed"
)

word_count = len(input_text.split())
character_count = len(input_text)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📝 Total Words", f"{word_count:,}")

with col2:
    st.metric("🔤 Characters", f"{character_count:,}")

with col3:
    st.metric("🎯 Summary Style", summary_length)


# --------------------------------------------------
# GENERATE
# --------------------------------------------------

st.write("")

if st.button("✨  Generate AI Summary", type="primary",
             use_container_width=True):

    if not input_text.strip():
        st.warning("Please enter some text first.")

    elif word_count < 30:
        st.warning("Please enter at least 30 words.")

    else:
        try:
            with st.spinner("✨ AI is analyzing your content..."):

                start_time = time.time()

                ai = load_model()

                summary = ai.summarize(
                    input_text,
                    summary_length.lower()
                )

                processing_time = time.time() - start_time

            st.session_state.summary = summary
            st.session_state.processing_time = processing_time
            st.session_state.original_words = word_count

            st.success("Your summary is ready!")

        except Exception as error:
            st.error(f"Unable to generate summary: {error}")


# --------------------------------------------------
# SUMMARY OUTPUT
# --------------------------------------------------

if st.session_state.summary:

    summary = st.session_state.summary

    summary_words = len(summary.split())

    original_words = st.session_state.original_words

    reduction = (
        (original_words - summary_words) / original_words
    ) * 100 if original_words else 0

    st.divider()

    st.markdown(
        '<div class="section-heading">✨ AI Generated Summary</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="summary-card">{summary}</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.download_button(
        "⬇️ Download Summary",
        data=summary,
        file_name="Sumi_AI_Summary.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.write("")

    st.markdown("### 📊 Summary Analytics")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric("Original Words", f"{original_words:,}")

    with m2:
        st.metric("Summary Words", f"{summary_words:,}")

    with m3:
        st.metric("Text Reduction", f"{reduction:.1f}%")

    st.caption(
        f"⏱️ Generated in {st.session_state.processing_time:.2f} seconds"
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown("""
<div class="footer">
    Crafted with 💜 using Python, Streamlit & Hugging Face
    <br><br>
    SUMI AI © 2026 | Intelligent Text Simplification
</div>
""", unsafe_allow_html=True)
