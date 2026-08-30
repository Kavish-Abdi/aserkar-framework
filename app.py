import streamlit as st
import json
import os

st.set_page_config(
    page_title="The A.S.E.R.K.A.R. Framework",
    layout="wide",
    page_icon="🔺"
)

# SVG Vector Logo and Centered Typography
header_html = """
<div style="text-align: center; margin-bottom: 20px;">
    <svg width="120" height="120" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad" x1="0%" y1="100%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#4A90E2;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#50E3C2;stop-opacity:1" />
            </linearGradient>
        </defs>
        <!-- The Monogram 'A' -->
        <path d="M50 15 L20 85 L35 85 L45 60 L70 45 L60 85 L75 85 Z" fill="url(#grad)" />
        <!-- The Glowing Apex Node -->
        <circle cx="50" cy="15" r="5" fill="#50E3C2" />
        <!-- Converging Transit Arrow -->
        <path d="M25 70 L90 25" stroke="#50E3C2" stroke-width="5" stroke-linecap="round"/>
        <path d="M75 25 L90 25 L85 40" fill="none" stroke="#50E3C2" stroke-width="5" stroke-linecap="round"/>
    </svg>
    <h1 style="margin-top: 15px; margin-bottom: 5px; font-weight: 700;">The A.S.E.R.K.A.R. Framework</h1>
    <p style="color: #A0AEC0; font-size: 17px; margin-top: 0px; font-weight: 400;">( Anticipatory Supply-chain Engine for Risk, Knowledge, and Automated Resilience )</p>
</div>
"""

st.markdown(header_html, unsafe_allow_html=True)
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
        cols = st.columns(3)
        
        for index, article in enumerate(articles):
            col = cols[index % 3]
            
            with col.container(border=True):
                thumbnail = article.get("thumbnail", "https://images.unsplash.com/photo-1586528116311-ad8ed7c663c0?w=800&q=80")
                try:
                    st.image(thumbnail, use_container_width=True)
                except Exception:
                    st.image("https://images.unsplash.com/photo-1586528116311-ad8ed7c663c0?w=800&q=80", use_container_width=True)
                
                st.caption(f"**{article.get('source', 'Industry Intelligence')}** • {article.get('date_collected', 'Recent')}")
                st.subheader(article.get("title", "Untitled Intelligence Brief"))
                st.write(article.get("summary", "No summary available."))
                
                link = article.get("link", "#")
                st.markdown(f"[**Click to Read Full Article ↗**]({link})")
else:
    st.warning("Intelligence database not found. Please run the collector script or wait for the GitHub Action to execute.")
