import os
import streamlit as st
from wargame_engine import run_aserkar_simulation, fetch_local_intelligence

st.set_page_config(page_title="The A.S.E.R.K.A.R. Framework", layout="wide")

st.title("🛡️ The A.S.E.R.K.A.R. Framework")
st.caption("Anticipatory Supply-chain Engine for Risk, Knowledge, and Automated Resilience")

st.sidebar.header("Command Center")
if st.sidebar.button("Generate Wargame Scenario"):
    with st.spinner("Analyzing intelligence feed and running multi-agent simulation..."):
        try:
            scenario = run_aserkar_simulation()
            st.success("Simulation Complete!")
            st.markdown(scenario)
        except Exception as e:
            st.error(f"Error during simulation: {e}")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("📡 Live Background Intelligence Feed")
    st.info("This data is collected automatically every 12 hours by GitHub Actions.")
    intel = fetch_local_intelligence()
    st.text_area("Latest Data Payload", intel, height=300)

with col2:
    st.header("📋 Scenario Archive")
    if os.path.exists("scenarios"):
        files = [f for f in os.listdir("scenarios") if f.endswith(".md")]
        files.sort(reverse=True)
        if files:
            selected_file = st.selectbox("Review past stress-tests:", files)
            if selected_file:
                with open(os.path.join("scenarios", selected_file), "r") as f:
                    st.markdown(f.read())
        else:
            st.info("No scenarios generated yet. Click the sidebar button to generate one.")
