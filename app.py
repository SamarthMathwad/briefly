import streamlit as st
import time
import fitz  # PyMuPDF
from summarizer import summarize_text, extract_entities

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Briefly",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THE "MIDNIGHT PRO" UI (Safe & Beautiful) ---
st.markdown("""
<style>
    /* 1. Force Dark Background & White Text (Prevents Blank Screen) */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* 2. Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1E1E2E;
        border-right: 1px solid #333;
    }

    /* 3. Metric Cards */
    div.metric-container {
        background-color: #262730;
        border: 1px solid #41424C;
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 10px;
    }
    div.metric-container h3 { margin: 0; font-size: 1.5rem; color: white; }
    div.metric-container p { margin: 0; font-size: 0.9rem; color: #AAA; }

    /* 4. Entity Badges (The "WTF" Fix) */
    .entity-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 4px;
        color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    /* Specific Colors for Specific Types */
    .ORG { background-color: #8b5cf6; border: 1px solid #7c3aed; } /* Purple */
    .PERSON { background-color: #ec4899; border: 1px solid #db2777; } /* Pink */
    .GPE { background-color: #10b981; border: 1px solid #059669; } /* Green */
    .DATE { background-color: #f59e0b; border: 1px solid #d97706; } /* Orange */
    
    /* 5. Summary Box */
    .summary-box {
        background-color: #1E1E2E;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #6366f1;
        font-size: 1.1rem;
        line-height: 1.6;
        color: #E0E0E0;
    }
    
    /* 6. Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def read_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def calculate_reading_time(word_count):
    return round(word_count / 200, 1)

# --- SIDEBAR ---
with st.sidebar:
    st.title("Briefly.")
    st.markdown("### Settings")
    summary_ratio = st.slider("Density", 10, 80, 30, 10)
    st.info("💡 **Pro Tip:** Upload legal or financial docs to test the Entity Extraction.")

# --- MAIN UI ---
st.markdown("<h1 style='text-align: center;'>Simplify Your Reading.</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #AAA;'>Intelligent Summarization & Entity Recognition</p>", unsafe_allow_html=True)

# --- INPUT SECTION ---
col1, col2 = st.columns(2)
input_text = ""

with col1:
    uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])
    if uploaded_file:
        with st.spinner("Processing PDF..."):
            input_text = read_pdf(uploaded_file)
            st.success(f"File Loaded: {uploaded_file.name}")

with col2:
    text_area_input = st.text_area("Or Paste Text Here", height=150)
    if not uploaded_file:
        input_text = text_area_input

# --- PROCESS ---
st.markdown("---")
if st.button("✨ Analyze Document", type="primary"):
    if not input_text:
        st.warning("⚠️ Please provide text first.")
    else:
        # Metrics
        original_words = len(input_text.split())
        original_time = calculate_reading_time(original_words)
        
        with st.spinner("Extracting Insights & Entities..."):
            time.sleep(0.5)
            # Call your Local Engine
            summary, keywords = summarize_text(input_text, percentage=(summary_ratio/100))
            entities = extract_entities(input_text)
            
            # Calc Savings
            summary_words = len(summary.split())
            summary_time = calculate_reading_time(summary_words)
            time_saved = round(original_time - summary_time, 1)
            reduction = 100 - int((summary_words / original_words) * 100)

        # --- RESULTS DASHBOARD ---
        
        # 1. ENTITIES (The "Wow" Factor)
        if entities:
            st.subheader("🧩 Key Entities Detected")
            # Loop through the raw list and make HTML badges
            html_content = ""
            for text, label in entities[:20]: # Show top 20
                html_content += f"<span class='entity-tag {label}'>{text} <span style='opacity:0.6; font-size:0.7em;'>{label}</span></span>"
            st.markdown(html_content, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

        # 2. METRICS ROW
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f"<div class='metric-container'><h3>{original_words}</h3><p>Words</p></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='metric-container'><h3>{reduction}%</h3><p>Conciseness</p></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='metric-container' style='border-color:#10b981'><h3 style='color:#10b981'>{time_saved} min</h3><p>Saved</p></div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='metric-container'><h3>{len(entities)}</h3><p>Entities</p></div>", unsafe_allow_html=True)

        # 3. SUMMARY
        st.subheader("📝 Executive Summary")
        st.markdown(f"<div class='summary-box'>{summary}</div>", unsafe_allow_html=True)
        
        st.download_button("📥 Download Brief", summary, "brief.txt")

# --- PROFESSIONAL FOOTER ---
st.sidebar.markdown("---")

# 1. Your Name (Bold and Professional)
st.sidebar.markdown("### Developed by Samarth Mathwad")

# 2. The "Elevator Pitch" (Subtle text)
st.sidebar.caption("Automated Legal & Technical Document Analysis.")

# 3. The Links (Clean text, no emojis)
# IMPORTANT: Replace the 'YOUR_URL_HERE' part below with your actual LinkedIn profile link
st.sidebar.markdown("[LinkedIn Profile](https://www.linkedin.com/in/samarth-mathwad-4589b9315/)  •  [GitHub Repository](https://github.com/SamarthMathwad)")

# 4. The Copyright (Adds authority)
st.sidebar.caption("© 2026 Briefly AI. All Rights Reserved.")