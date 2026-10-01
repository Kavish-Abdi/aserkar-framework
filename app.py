import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="The A.S.E.R.K.A.R. Framework",
    layout="wide",
    page_icon="🔺"
)

# --- HEADER SECTION ---
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
st.divider()

def get_cycle_name(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        year = dt.year
        month = dt.month
        
        cycles = {
            1: "Jan-Feb", 2: "Jan-Feb",
            3: "Mar-Apr", 4: "Mar-Apr",
            5: "May-Jun", 6: "May-Jun",
            7: "Jul-Aug", 8: "Jul-Aug",
            9: "Sep-Oct", 10: "Sep-Oct",
            11: "Nov-Dec", 12: "Nov-Dec"
        }
        return f"{cycles[month]} {year}"
    except ValueError:
        return "Unknown Cycle"

json_path = "data/intelligence.json"

if os.path.exists(json_path):
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
            
        if data and isinstance(data, list):
            # Group reports by their 2-month cycle
            cycles_dict = {}
            for report in data:
                cycle = get_cycle_name(report.get("date_collected", ""))
                if cycle not in cycles_dict:
                    cycles_dict[cycle] = []
                cycles_dict[cycle].append(report)
            
            available_cycles = list(cycles_dict.keys())
            
            # Global Dropdown controls both tabs
            col1, col2 = st.columns([1, 3])
            with col1:
                selected_cycle = st.selectbox("Select Analysis Cycle:", available_cycles)
            
            st.write(f"### Intelligence for {selected_cycle}")
            st.write("")
            
            # --- TAB NAVIGATION ---
            tab_archive, tab_wargame = st.tabs(["🌐 Disruption Archive", "⚔️ War Game Simulator"])
            
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
                st.write("Autonomous predictive modeling of 6-month compounding impacts based on the week's critical disruptions.")
                for report in cycles_dict[selected_cycle]:
                    st.caption(f"**Scenario Generated:** {report.get('date_collected')}")
                    with st.container(border=True):
                        # Safely load the wargame scenario or display a fallback message if missing
                        wargame_data = report.get("wargame_scenario", "No War Game Scenario generated for this cycle yet.")
                        st.markdown(wargame_data)
                    st.write("")
                    
        else:
            st.info("Awaiting next automated collection cycle to generate reports.")
            
    except json.JSONDecodeError:
        st.error("Intelligence database is corrupted or empty.")
else:
    st.warning("Intelligence database not found. Please run the collector script.")
