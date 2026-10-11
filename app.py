import streamlit as st
import json
import os
import base64
from datetime import datetime
import pandas as pd

st.set_page_config(
    page_title="The A.S.E.R.K.A.R. Framework",
    layout="wide",
    page_icon="🔺"
)

# --- IMAGE ENCODER FOR INLINE HTML ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

logo_base64 = get_base64_image("logo1.png")
logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="height: 65px; margin-right: 20px;">' if logo_base64 else ''

# --- HEADER SECTION (FLEXBOX ALIGNMENT) ---
st.markdown(
    f"""
    <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 25px;">
        {logo_html}
        <div style="display: flex; flex-direction: column; justify-content: center;">
            <h1 style="margin: 0; padding: 0; font-weight: 800; letter-spacing: 0.5px; line-height: 1.2;">
                The A.S.E.R.K.A.R. Framework
            </h1>
            <p style="color: #94A3B8; font-size: 15px; margin: 0; padding: 0; font-weight: 400; padding-top: 5px;">
                ( Anticipatory Supply-chain Engine for Risk, Knowledge, and Automated Resilience )
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.divider()

def get_cycle_name(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        year = dt.year
        month = dt.month
        cycles = {
            1: "Jan-Feb", 2: "Jan-Feb", 3: "Mar-Apr", 4: "Mar-Apr",
            5: "May-Jun", 6: "May-Jun", 7: "Jul-Aug", 8: "Jul-Aug",
            9: "Sep-Oct", 10: "Sep-Oct", 11: "Nov-Dec", 12: "Nov-Dec"
        }
        return f"{cycles[month]} {year}"
    except ValueError:
        return "Unknown Cycle"

json_path = "data/intelligence.json"
cfg_path = "data/config.json"

if os.path.exists(json_path):
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
            
        if data and isinstance(data, list):
            cycles_dict = {}
            for report in data:
                cycle = get_cycle_name(report.get("date_collected", ""))
                if cycle not in cycles_dict:
                    cycles_dict[cycle] = []
                cycles_dict[cycle].append(report)
            
            available_cycles = list(cycles_dict.keys())
            
            col1, col2 = st.columns([1, 3])
            with col1:
                selected_cycle = st.selectbox("Select Analysis Cycle:", available_cycles)
            
            st.write(f"### Intelligence for {selected_cycle}")
            st.write("")
            
            # --- TAB NAVIGATION ---
            tab_archive, tab_wargame, tab_settings = st.tabs([
                "🌐 Disruption Archive", 
                "⚔️ War Game Simulator", 
                "⚙️ Feed & Filter Settings"
            ])
            
            # --- TAB 1: ARCHIVE ---
            with tab_archive:
                st.markdown("#### Macro-level intelligence tracking critical disruption vectors.")
                for report in cycles_dict[selected_cycle]:
                    st.caption(f"**Synthesis Generated:** {report.get('date_collected')} | **Articles Analyzed:** {report.get('articles_analyzed', 'N/A')}")
                    with st.container(border=True):
                        st.markdown(report.get("master_report", "Report empty."))
                    st.write("") 
            
            # --- TAB 2: WAR GAME SIMULATOR ---
            with tab_wargame:
                st.markdown("#### Strategic Impact Forecasting & Scenario Analysis")
                for report in cycles_dict[selected_cycle]:
                    st.caption(f"**Scenario Generated:** {report.get('date_collected')}")
                    with st.container(border=True):
                        wargame_data = report.get("wargame_scenario", "No War Game Scenario generated for this cycle yet.")
                        
                        # Backwards compatibility check for older string-based reports
                        if isinstance(wargame_data, str):
                            st.markdown(wargame_data)
                        elif isinstance(wargame_data, dict):
                            if "error" in wargame_data:
                                st.error(wargame_data["error"])
                            else:
                                st.markdown("### 📋 Executive Scenario Table")
                                st.markdown(wargame_data.get("table", ""))
                                
                                col_visual1, col_visual2 = st.columns([1, 1])
                                with col_visual1:
                                    st.markdown("### 🗺️ Global Disruption Map")
                                    coords = wargame_data.get("coordinates", [])
                                    if coords:
                                        df = pd.DataFrame(coords)
                                        if not df.empty and "lat" in df.columns and "lon" in df.columns:
                                            st.map(df, size=20)
                                        else:
                                            st.info("No geospatial data triggered this cycle.")
                                    else:
                                        st.info("No geospatial data triggered this cycle.")

                                with col_visual2:
                                    st.markdown("### 🔀 Supply Chain Flowchart")
                                    mermaid_code = wargame_data.get("mermaid", "")
                                    if mermaid_code:
                                        st.mermaid_chart(mermaid_code)
                                    else:
                                        st.info("No routing flowchart triggered this cycle.")
                                        
                                st.divider()
                                st.markdown("### 📚 References")
                                st.markdown(wargame_data.get("references", ""))
                    st.write("")
                    
            # --- TAB 3: SETTINGS (ADMIN) ---
            with tab_settings:
                st.markdown("#### Dynamic Source & Keyword Management")
                st.caption("Add or modify RSS feeds and filtration keywords dynamically for Professor Aserkar. Changes take effect on the next collection cycle.")
                
                if os.path.exists(cfg_path):
                    with open(cfg_path, "r") as f:
                        cfg = json.load(f)
                else:
                    cfg = {"rss_urls": [], "target_keywords": []}
                
                col_sources, col_kw = st.columns(2)
                with col_sources:
                    st.subheader("Monitored RSS Feeds")
                    current_urls_str = "\n".join(cfg.get("rss_urls", []))
                    updated_urls = st.text_area(
                        "RSS Feed URLs (one per line):", 
                        value=current_urls_str, 
                        height=260
                    )
                    
                with col_kw:
                    st.subheader("Filter Keywords")
                    current_kw_str = ", ".join(cfg.get("target_keywords", []))
                    updated_kw = st.text_area(
                        "Keywords (comma-separated):", 
                        value=current_kw_str, 
                        height=260
                    )
                    
                if st.button("Save Configuration", type="primary"):
                    parsed_urls = [u.strip() for u in updated_urls.split("\n") if u.strip()]
                    parsed_kw = [k.strip().lower() for k in updated_kw.split(",") if k.strip()]
                    
                    os.makedirs("data", exist_ok=True)
                    with open(cfg_path, "w") as f:
                        json.dump({"rss_urls": parsed_urls, "target_keywords": parsed_kw}, f, indent=4)
                    
                    st.success("Configuration successfully updated. Next automated cycle will use these new parameters.")
                    
        else:
            st.info("Awaiting next automated collection cycle to generate reports.")
            
    except json.JSONDecodeError:
        st.error("Intelligence database is corrupted or empty.")
else:
    st.warning("Intelligence database not found. Please run the collector script.")
