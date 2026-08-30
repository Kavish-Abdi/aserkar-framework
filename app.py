import streamlit as st
import json
import os

st.set_page_config(
    page_title="The A.S.E.R.K.A.R. Framework",
    layout="wide",
    page_icon="🔺"
)

# Centered Top Branding with the Sharp Monogram 'A' Apex Vector
header_html = """
<div style="text-align: center; margin-top: 10px; margin-bottom: 20px;">
    <svg width="90" height="90" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style="margin-bottom: 5px;">
        <defs>
            <linearGradient id="apexGrad" x1="0%" y1="100%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#3B82F6;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#14B8A6;stop-opacity:1" />
            </linearGradient>
        </defs>
        <!-- Monogram 'A' Structure -->
        <path d="M50 12 L18 88 L34 88 L44 62 L72 46 L58 88 L74 88 Z" fill="url(#apexGrad)" />
        <!-- Glowing Apex Summit Node -->
        <circle cx="50" cy="12" r="5" fill="#2DD4BF" />
        <!-- Converging Transit Vector Stream -->
        <path d="M22 72 L88 28" stroke="#2DD4BF" stroke-width="4.5" stroke-linecap="round"/>
        <path d="M72 28 L88 28 L82 44" fill="none" stroke="#2DD4BF" stroke-width="4.5" stroke-linecap="round"/>
    </svg>
    <h1 style="margin-bottom: 4px; font-weight: 800; letter-spacing: 0.5px;">The A.S.E.R.K.A.R. Framework</h1>
    <p style="color: #94A3B8; font-size: 15px; margin-top: 0px; font-weight: 400;">
        ( Anticipatory Supply-chain Engine for Risk, Knowledge, and Automated Resilience )
    </p>
</div>
"""

st.markdown(header_html, unsafe_allow_html=True)

# Original Dashboard Section Header
st.title("🌐 Supply Chain Intelligence Hub")
st.markdown("Autonomous multi-source ingestion, AI executive briefings, and logistics risk monitoring.
Named after Prof. Rajiv Aserkar")
st.divider()

json_path = "data/intelligence.json"

if os.path.exists(json_path):
    try:
        with open(json_path, "r") as f:
            articles = json.load(f)
    except json.JSONDecodeError:
        articles = []
        
    if not articles:
        st.info("The intelligence database is currently empty. Waiting for the next automated collection cycle.")
    else:
        # Dynamic 3-column responsive card grid
        cols = st.columns(3)
        
        for index, article in enumerate(articles):
            col = cols[index % 3]
            
            with col.container(border=True):
                # Thumbnail preview
                thumbnail = article.get("thumbnail", "https://images.unsplash.com/photo-1586528116311-ad8ed7c663c0?w=800&q=80")
                try:
                    st.image(thumbnail, use_container_width=True)
                except Exception:
                    st.image("https://images.unsplash.com/photo-1586528116311-ad8ed7c663c0?w=800&q=80", use_container_width=True)
                
                # Metadata & Title
                st.caption(f"**{article.get('source', 'Industry Intelligence')}** • {article.get('date_collected', 'Recent')}")
                st.subheader(article.get("title", "Untitled Intelligence Brief"))
                
                # Briefing summary paragraph
                st.write(article.get("summary", "No summary available."))
                
                # Compact article link
                link = article.get("link", "#")
                st.markdown(f"[**Click to Read Full Article ↗**]({link})")
else:
    st.warning("Intelligence database not found. Please run the collector script or wait for the GitHub Action to execute.")
