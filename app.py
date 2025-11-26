import streamlit as st
from orchestrator import Orchestrator
from llm import LLMClient
from dotenv import load_dotenv
import os
import base64

load_dotenv()

st.set_page_config(page_title='Debate Arena', layout='wide')
def load_base64_image(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
logo_base64 = load_base64_image("company_logo.png")

# ------------------- HEADER WITH BG + LOCAL LOGO + CENTERED TITLE -------------------
st.markdown(f"""
<style>
.header-box {{
    width: 100%;
    padding: 20px 30px;
    background: linear-gradient(to right, 90deg, #4a6cf7, #6ca8f7);
    border-radius: 12px;
    margin-bottom: 25px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    position: relative;
    display: flex;
    align-items: center;
    justify-content: right;
    position: relative;
}}
.header-logo {{
    position: absolute;
    left: 80px;
    width: 250px;
    height: 250px;
    border-radius: 10px;
}}
.header-title {{
    margin: 0;
    font-size: 34px;
    font-weight: 800;
    color: white;
    text-align: center;
}}
</style>

<div class="header-box">
    <img src="data:image/png;base64,{logo_base64}" class="header-logo">
    <h1 class="header-title">Debate — Multi AI Agent Conversational Thinkers</h1>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUTS ----------------
topic = st.text_area(
    "Enter a debate topic or question",
    height=100,
    placeholder="Is AI creativity real?"
)

num_agents = st.selectbox(
    "Number of AI agents",
    options=[2, 3, 4],
    index=0
)

rounds = st.slider("Rounds per agent", 1, 5, 2)

start_btn = st.button("Start Debate")
if start_btn:
    if num_agents == "Select number of agents":
        st.error("Please select the number of agents.")
        st.stop()

# Init engines
llm_client = LLMClient()
orch = Orchestrator(llm_client=llm_client)

# ---------------- WHEN DEBATE STARTS ----------------
if start_btn:
    if not topic.strip():
        st.error("Please enter a topic.")
    else:
        with st.spinner("Running debate...please wait..."):
            transcript, summary = orch.run_debate(topic, num_agents, rounds)

        st.success("Debate complete")

        # ---------- TWO AGENTS (Pro / Con OR Side-A / Side-B) ----------
        if num_agents == 2:
            col1, col2 = st.columns(2)

            # ---------------- PRO BOX ----------------
            with col1:
                pro_html = """
                <div style="
                    background-color: #eef2ff;
                    border: 1px solid #c7c9ff;
                    padding: 20px;
                    border-radius: 12px;
                    margin-top: 25px;
                ">
                """
                pro_html += f"<h3 style='margin-top:0'>{transcript['agents'][0]['name']}</h3>"

                for turn in transcript["agents"][0]["turns"]:
                    pro_html += (
                        f"<p><b>Round {turn['round']}:</b> {turn['text']}</p>"
                    )

                pro_html += "</div>"

                st.markdown(pro_html, unsafe_allow_html=True)

            # ---------------- CON BOX ----------------
            with col2:
                con_html = """
                <div style="
                    background-color: #fff1f2;
                    border: 1px solid #ffccd0;
                    padding: 20px;
                    border-radius: 12px;
                    margin-top: 25px;
                ">
                """
                con_html += f"<h3 style='margin-top:0'>{transcript['agents'][1]['name']}</h3>"

                for turn in transcript["agents"][1]["turns"]:
                    con_html += (
                        f"<p><b>Round {turn['round']}:</b> {turn['text']}</p>"
                    )

                con_html += "</div>"

                st.markdown(con_html, unsafe_allow_html=True)

        # ---------- MULTIPLE AGENTS ----------
        else:
            for agent in transcript["agents"]:
                box_html = """
                <div style="
                    background-color: #f4f6fb;
                    border: 1px solid #c7ccd9;
                    padding: 20px;
                    border-radius: 12px;
                    margin-top: 25px;
                ">
                """
                box_html += f"<h3 style='margin-top:0'>{agent['name']}</h3>"

                for turn in agent["turns"]:
                    box_html += (
                        f"<p><b>Round {turn['round']}:</b> {turn['text']}</p>"
                    )

                box_html += "</div>"
                st.markdown(box_html, unsafe_allow_html=True)

        # ---------- SUMMARY BOX ----------
        summary_html = """
        <div style="
            background-color: #e6ffed;
            border: 1px solid #9ad8a6;
            padding: 25px;
            border-radius: 12px;
            margin-top: 35px;
        ">
        <h2 style="margin-top:0;">Summary of the debate</h2>
        """

        summary_html += f"<p>{summary['summary_text']}</p>"

       
        st.markdown(summary_html, unsafe_allow_html=True)
        # ==============================
# FOOTER
# ==============================
st.markdown(
    """
    <div style='text-align:center; color:#555; margin-top:25px;'>
        <hr style="border: none; height: 2px; background: linear-gradient(to right, #1976d2, #42a5f5); margin: 20px 0;">
        <p> Designed by <b>Taviti Naidu</b> || IncubXperts </p>
    </div>
    """,
    unsafe_allow_html=True
)

