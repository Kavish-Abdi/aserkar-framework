import streamlit as st
import json
import os

st.set_page_config(
    page_title="The A.S.E.R.K.A.R. Framework",
    layout="wide",
    page_icon="🌐"
)

st.title("🌐 Supply Chain Intelligence Hub")
st.markdown("Autonomous multi-source ingestion, AI executive briefings, and logistics risk monitoring.")
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
        # Dynamic 3-column magazine layout
        cols = st.columns(3)
        
        for index, article in enumerate(articles):
            col = cols[index % 3]
            
            with col.container(border=True):
                # Thumbnail image
                thumbnail = article.get("thumbnail", "https://images.unsplash.com/photo-1586528116311-ad8ed7c663c0?w=800&q=80")
                try:
                    st.image(thumbnail, use_container_width=True)
                except Exception:
                    st.image("https://images.unsplash.com/photo-1586528116311-ad8ed7c663c0?w=800&q=80", use_container_width=True)
                
                # Metadata & Title
                st.caption(f"**{article.get('source', 'Industry Intelligence')}** • {article.get('date_collected', 'Recent')}")
                st.subheader(article.get("title", "Untitled Intelligence Brief"))
                
                # Full AI Briefing Paragraph
                st.write(article.get("summary", "No summary available."))
                
                # Clean embedded hyperlink
                link = article.get("link", "#")
                st.markdown(f"[**Click to Read Full Article ↗**]({link})")
else:
    st.warning("Intelligence database not found. Please run the collector script or wait for the GitHub Action to execute.")
