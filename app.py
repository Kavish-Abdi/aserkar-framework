import streamlit as st
import json
import os

st.set_page_config(
    page_title="The A.S.E.R.K.A.R. Framework",
    layout="wide",
    page_icon="🔺"
)

# Centered Logo and New Framework Heading
header_col1, header_col2, header_col3 = st.columns([1.5, 1, 1.5])

with header_col2:
    if os.path.exists("logo1.png"):
        st.image("logo1.png", use_container_width=True)
    else:
        st.warning("logo1.png not found. Please upload it to the repository.")

st.markdown(
    """
    <div style="text-align: center; margin-top: 0px; margin-bottom: 25px;">
        <h1 style="margin-bottom: 4px; font-weight: 800; letter-spacing: 0.5px;">The A.S.E.R.K.A.R. Framework</h1>
        <p style="color: #94A3B8; font-size: 15px; margin-top: 0px; font-weight: 400;">
            ( Anticipatory Supply-chain Engine for Risk, Knowledge, and Automated Resilience )
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Original Dashboard Section Header
st.title("🌐 Supply Chain Intelligence Hub")
st.markdown("Autonomous multi-source ingestion, AI executive briefings, and logistics risk monitoring.")
st.divider()

# Backend JSON Loading and Grid Display
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
                # Thumbnail
                thumbnail = article.get("thumbnail", "https://images.unsplash.com/photo-1586528116311-ad8ed7c663c0?w=800&q=80")
                try:
                    st.image(thumbnail, use_container_width=True)
                except Exception:
                    st.image("https://images.unsplash.com/photo-1586528116311-ad8ed7c663c0?w=800&q=80", use_container_width=True)
                
                # Metadata & Title
                st.caption(f"**{article.get('source', 'Industry Intelligence')}** • {article.get('date_collected', 'Recent')}")
                st.subheader(article.get("title", "Untitled Intelligence Brief"))
                
                # --- NEW: Visual Risk Tags ---
                risk_tags = article.get("risk_tags", [])
                if risk_tags:
                    # Create HTML badges for each risk category triggered
                    badges_html = " ".join([
                        f"<span style='background-color: #ef4444; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; display: inline-block; margin-bottom: 5px; margin-right: 4px;'>{tag}</span>" 
                        for tag in risk_tags
                    ])
                    st.markdown(f"<div style='margin-bottom: 10px;'>{badges_html}</div>", unsafe_allow_html=True)
                
                # AI Summary & Link
                st.write(article.get("summary", "No summary available."))
                link = article.get("link", "#")
                st.markdown(f"[**Click to Read Full Article ↗**]({link})")
else:
    st.warning("Intelligence database not found. Please run the collector script or wait for the GitHub Action to execute.")
