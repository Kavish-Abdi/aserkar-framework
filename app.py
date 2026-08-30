import streamlit as st
import json
import os

st.set_page_config(page_title="The A.S.E.R.K.A.R. Framework", layout="wide", page_icon="🌐")

st.title("🌐 Supply Chain Intelligence Hub")
st.markdown("Live multi-source data extraction and AI-summarized threat intelligence.")
st.divider()

json_path = "data/intelligence.json"

if os.path.exists(json_path):
    with open(json_path, "r") as f:
        try:
            articles = json.load(f)
        except json.JSONDecodeError:
            articles = []
            
    if not articles:
        st.info("The intelligence database is currently empty. Waiting for the next background collection cycle.")
    else:
        # Create a dynamic 3-column grid for the magazine layout
        cols = st.columns(3)
        
        for index, article in enumerate(articles):
            # Distribute articles evenly across the 3 columns
            col = cols[index % 3]
            
            with col.container(border=True):
                # Display the extracted thumbnail image
                thumbnail = article.get("thumbnail", "https://images.unsplash.com/photo-1586528116311-ad8ed7c663c0?w=800&q=80")
                try:
                    st.image(thumbnail, use_container_width=True)
                except Exception:
                    st.image("https://images.unsplash.com/photo-1586528116311-ad8ed7c663c0?w=800&q=80", use_container_width=True)
                
                # Display metadata and title
                st.caption(f"**{article.get('source', 'Industry Source')}** • {article.get('date_collected', 'Recent')}")
                st.subheader(article.get("title", "Untitled Intelligence Report"))
                
                # Display Gemini's executive summary
                st.write(article.get("summary", "No summary available."))
                
                # Provide direct canonical link
                link = article.get("link", "#")
                st.markdown(f"[**Read Original Article ↗**]({link})")
else:
    st.warning("Intelligence database not found. Ensure the GitHub Actions collector has successfully run.")
