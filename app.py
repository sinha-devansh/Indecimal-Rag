import streamlit as st
from rag_pipeline.retrieval import retrieve_chunks
from rag_pipeline.rag_generation import run_rag

# -----------------------------------------------------------------------------
# Page config
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Indecimal RAG Assistant",
    page_icon="🏗️",
    layout="wide",
)

@st.cache_resource
def warmup():
    try:
        retrieve_chunks("warmup")
        run_rag("warmup", [])
    except Exception as e:
        pass

warmup()

# -----------------------------------------------------------------------------
# Custom CSS
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Dark background without dots - clean gradient */
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #1a1f35 100%) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Add glowing orbs only */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 15% 20%, rgba(0, 255, 255, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 85% 70%, rgba(138, 43, 226, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 50% 90%, rgba(0, 191, 255, 0.12) 0%, transparent 40%);
        pointer-events: none;
        z-index: 0;
        animation: pulse 10s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 0.8; }
    }
    
    /* Ensure content is above background */
    .main > div {
        position: relative;
        z-index: 1;
    }
    
    /* Typography with larger fonts */
    h1 {
        color: #ffffff !important;
        font-weight: 700 !important;
        text-shadow: 0 0 30px rgba(0, 255, 255, 0.4), 0 2px 10px rgba(0, 0, 0, 0.5);
        margin-bottom: 0.8rem !important;
        font-size: 3rem !important;
    }
    
    h2 {
        color: #ffffff !important;
        font-weight: 600 !important;
        text-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
        font-size: 1.8rem !important;
    }
    
    h3 {
        color: #ffffff !important;
        font-weight: 600 !important;
        text-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
        font-size: 1.5rem !important;
    }
    
    /* Fix all text visibility with larger fonts */
    .stMarkdown, .stMarkdown p, .stMarkdown span {
        color: rgba(255, 255, 255, 0.95) !important;
        font-size: 1.1rem !important;
    }
    
    /* Labels */
    label {
        color: rgba(0, 255, 255, 0.9) !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
    }
    
    /* Strong text */
    strong {
        color: #00ffff !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    
    /* Input fields with enhanced glow */
    .stTextInput input {
        background: rgba(15, 23, 42, 0.85) !important;
        border: 2px solid rgba(0, 255, 255, 0.4) !important;
        color: #ffffff !important;
        border-radius: 14px !important;
        padding: 14px 20px !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), inset 0 1px 3px rgba(0, 255, 255, 0.1);
    }
    
    .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
        font-size: 1.05rem !important;
    }
    
    .stTextInput input:focus {
        border-color: rgba(0, 255, 255, 0.8) !important;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.5), 0 8px 25px rgba(0, 0, 0, 0.4) !important;
        background: rgba(15, 23, 42, 0.95) !important;
        transform: translateY(-1px);
    }
    
    /* Slider */
    .stSlider {
        padding: 10px 0;
    }
    
    .stSlider label {
        color: rgba(255, 255, 255, 0.95) !important;
        font-size: 1.05rem !important;
    }
    
    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"] {
        color: rgba(255, 255, 255, 0.7) !important;
        font-size: 0.95rem !important;
    }
    
    /* Horizontal rule with glow */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.6), transparent) !important;
        margin: 2rem 0 !important;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
    }
    
    /* Cards with glassmorphism */
    .element-container > div > div {
        background: rgba(15, 23, 42, 0.7) !important;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 255, 255, 0.2);
        border-radius: 16px;
    }
    
    /* Expanders with enhanced style */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(20, 30, 55, 0.9)) !important;
        border: 2px solid rgba(0, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        color: rgba(255, 255, 255, 0.95) !important;
        padding: 14px 20px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: rgba(0, 255, 255, 0.6) !important;
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.4), 0 4px 20px rgba(0, 0, 0, 0.4);
        background: linear-gradient(135deg, rgba(15, 23, 42, 1), rgba(20, 30, 55, 1)) !important;
        transform: translateY(-2px);
    }
    
    .streamlit-expanderContent {
        background: rgba(10, 15, 30, 0.9) !important;
        border: 2px solid rgba(0, 255, 255, 0.2) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        color: rgba(255, 255, 255, 0.9) !important;
        padding: 20px !important;
        box-shadow: inset 0 4px 10px rgba(0, 0, 0, 0.2);
    }
    
    .streamlit-expanderContent p {
        color: rgba(255, 255, 255, 0.9) !important;
        line-height: 1.7;
        font-size: 1.05rem !important;
    }
    
    .streamlit-expanderContent strong {
        color: #00ffff !important;
        font-size: 1.05rem !important;
    }
    
    /* Info boxes with better styling */
    .stInfo {
        background: linear-gradient(135deg, rgba(0, 191, 255, 0.15), rgba(0, 255, 255, 0.1)) !important;
        border: 2px solid rgba(0, 191, 255, 0.5) !important;
        border-left: 5px solid #00bfff !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0, 191, 255, 0.2), inset 0 1px 3px rgba(0, 191, 255, 0.1);
        padding: 16px 20px !important;
    }
    
    .stInfo p, .stInfo div {
        color: rgba(255, 255, 255, 0.95) !important;
        font-size: 1.05rem !important;
    }
    
    /* Code */
    code {
        background: rgba(0, 255, 255, 0.15) !important;
        color: #00ffff !important;
        border: 1px solid rgba(0, 255, 255, 0.2);
        padding: 2px 6px !important;
        border-radius: 4px !important;
    }
    
    /* Markdown containers */
    .stMarkdown {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: rgba(0, 255, 255, 0.3) !important;
        border-top-color: #00ffff !important;
    }
    
    /* Spinner text */
    .stSpinner > div + div {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Sidebar for source documents */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, rgba(10, 15, 30, 0.98), rgba(15, 20, 40, 0.98)) !important;
        border-right: 1px solid rgba(0, 255, 255, 0.2) !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.5);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: rgba(255, 255, 255, 0.95) !important;
    }
    
    [data-testid="stSidebar"] h3 {
        text-shadow: 0 0 15px rgba(0, 255, 255, 0.4);
    }
    
    /* Error messages */
    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(220, 38, 38, 0.1)) !important;
        border: 2px solid rgba(239, 68, 68, 0.5) !important;
        border-left: 5px solid #ef4444 !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.2);
    }
    
    .stError p {
        color: rgba(255, 255, 255, 0.95) !important;
        font-size: 1.05rem !important;
    }
    
    /* Remove default backgrounds */
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    [data-testid="stToolbar"] {
        display: none;
    }
    
    /* Main container background */
    [data-testid="stAppViewContainer"] {
        background: transparent !important;
    }
    
    /* Block container */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px !important;
    }
    
    /* Add card-like container for main content */
    .main .block-container > div:first-child {
        background: rgba(15, 23, 42, 0.3);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(0, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }</style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------
st.title("🏗️ Indecimal RAG Assistant")
st.markdown("**Answers are generated strictly from internal Indecimal documents**")
# -----------------------------------------------------------------------------
# Query Input
# -----------------------------------------------------------------------------
col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_input(
        "Ask a question about Indecimal policies, pricing, or processes:",
        placeholder="e.g. How are deviations in construction progress handled?",
    )

with col2:
    max_chunks = st.slider("Context chunks", 1, 4, 2, help="Number of document chunks to retrieve")

st.markdown("")
st.markdown("")

# -----------------------------------------------------------------------------
# Run RAG
# -----------------------------------------------------------------------------
if query and query.strip():
    with st.spinner("🔍 Retrieving relevant information..."):
        try:
            retrieved = retrieve_chunks(query)
            answer, used_chunks = run_rag(
                query=query,
                retrieved_results=retrieved,
                max_chunks=max_chunks,
            )
            
            # Answer section
            st.markdown("")
            st.markdown("### ✅ Answer")
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, rgba(0, 255, 255, 0.05), rgba(0, 191, 255, 0.05)); 
                            border-left: 4px solid #00ffff; 
                            border-radius: 12px; 
                            padding: 24px 28px; 
                            box-shadow: 0 4px 20px rgba(0, 255, 255, 0.15);
                            border: 1px solid rgba(0, 255, 255, 0.2);
                            color: rgba(255, 255, 255, 0.95);
                            line-height: 1.8;
                            font-size: 1.1rem;">
                    {answer}
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown("")
            st.markdown("")
            
            # Retrieved context
            st.markdown("### 📚 Retrieved Context")
            
            if not used_chunks:
                st.info("No relevant document sections were used.")
            else:
                for i, chunk in enumerate(used_chunks, 1):
                    meta = chunk["metadata"]
                    text = chunk["text"]
                    with st.expander(f"📄 Chunk {i}: {meta['section']}", expanded=(i == 1)):
                        st.markdown(f"**Source:** `{meta['source_file']}`")
                        st.markdown("---")
                        st.markdown(text)
            
            # Sidebar with sources
            with st.sidebar:
                st.markdown("### 📁 Source Documents")
                st.markdown("---")
                if used_chunks:
                    unique_sources = list(set([chunk["metadata"]["source_file"] for chunk in used_chunks]))
                    st.markdown(f"**Total Sources:** {len(unique_sources)}")
                    st.markdown("")
                    for idx, source in enumerate(unique_sources, 1):
                        st.markdown(f"{idx}. `{source}`")
                else:
                    st.info("No sources used")
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
else:
    st.markdown("")
    st.markdown(
        """
        <div style="text-align: center; 
                    padding: 60px 40px; 
                    background: linear-gradient(135deg, rgba(0, 255, 255, 0.03), rgba(138, 43, 226, 0.03));
                    border-radius: 16px;
                    border: 2px dashed rgba(0, 255, 255, 0.2);
                    margin-top: 40px;">
            <div style="font-size: 4rem; margin-bottom: 20px; filter: drop-shadow(0 0 10px rgba(0, 255, 255, 0.3));">💬</div>
            <h3 style="color: rgba(255, 255, 255, 0.95); 
                       font-weight: 600; 
                       margin-bottom: 12px;
                       font-size: 1.8rem;">Ready to Assist</h3>
            <p style="color: rgba(255, 255, 255, 0.7); 
                      margin: 0;
                      font-size: 1.15rem;">Enter your question above to get AI-powered answers from internal documents</p>
        </div>
        """,
        unsafe_allow_html=True,
    )