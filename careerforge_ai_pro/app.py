import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import os
from streamlit_lottie import st_lottie
from modules import (
    resume_analyzer,
    technical_assessor,
    communication_analyzer,
    confidence_meter,
    portfolio_analyzer,
    github_analyzer,
    linkedin_analyzer,
    certification_gap,
    company_matcher,
    success_predictor,
    roadmap_generator,
    scoring_engine,
    pdf_report,
    qr_generator,
)

st.set_page_config(
    page_title="CareerForge AI Pro – Ultimate Interview Readiness Analyzer",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---- Premium UI Styling ----
premium_css = """
<style>
/* Animated Gradient Background */
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp {
    background: linear-gradient(-45deg, #0f0c29, #302b63, #242424, #141e30, #243b55) !important;
    background-size: 400% 400% !important;
    animation: gradientBG 15s ease infinite !important;
    color: #fff;
    font-family: 'Inter', sans-serif;
}

/* Glassmorphism Containers */
.glass-container {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 3rem;
    margin: 2rem auto;
    text-align: center;
}

/* Custom SVG Animation */
.ai-logo {
    width: 200px;
    height: 200px;
    margin: 0 auto;
    display: block;
}

.pulse {
    animation: pulse-animation 2s infinite ease-in-out;
}
.spin-slow {
    transform-origin: center;
    animation: spin-animation 10s linear infinite;
}

@keyframes pulse-animation {
    0% { transform: scale(0.95); opacity: 0.8; }
    50% { transform: scale(1.05); opacity: 1; filter: drop-shadow(0 0 20px #00e5ff); }
    100% { transform: scale(0.95); opacity: 0.8; }
}
@keyframes spin-animation {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Hide standard Streamlit header/footer */
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(premium_css, unsafe_allow_html=True)

animated_svg_logo = """
<div class="glass-container">
<svg class="ai-logo pulse" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- Glowing Hexagon Base -->
  <polygon class="spin-slow" points="100,10 180,50 180,150 100,190 20,150 20,50" 
           fill="none" stroke="url(#gold-gradient)" stroke-width="4" filter="drop-shadow(0 0 10px #f0c987)"/>
           
  <!-- Brain / Tech Lines inside -->
  <path d="M100,40 L100,160 M60,80 L140,80 M60,120 L140,120 M100,100 L140,40 M100,100 L60,40 M100,100 L140,160 M100,100 L60,160" 
        stroke="url(#blue-gradient)" stroke-width="2" stroke-dasharray="5,5" class="spin-slow" style="animation-direction: reverse;"/>
  
  <!-- Central Glowing Node -->
  <circle cx="100" cy="100" r="15" fill="#00e5ff" filter="drop-shadow(0 0 15px #00e5ff)"/>
  
  <defs>
    <linearGradient id="gold-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0c987" />
      <stop offset="100%" stop-color="#d4af37" />
    </linearGradient>
    <linearGradient id="blue-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00e5ff" />
      <stop offset="100%" stop-color="#0077ff" />
    </linearGradient>
  </defs>
</svg>
<h1 style='text-align: center; font-weight: bold; font-size: 2.5rem; margin-top: 1rem;'>CareerForge AI Pro</h1>
<h3 style='text-align: center; color: #f0c987; font-weight: 300;'>Ultimate Interview Readiness Platform</h3>
</div>
"""

# ---- App State Management ----
if "app_state" not in st.session_state:
    st.session_state.app_state = "splash"  # "splash", "login", or "main"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "profile" not in st.session_state:
    st.session_state.profile = {}
if "scores" not in st.session_state:
    st.session_state.scores = {}

def splash_screen():
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(animated_svg_logo, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        _, btn_col, _ = st.columns([1, 1, 1])
        with btn_col:
            if st.button("Get Started", use_container_width=True):
                st.session_state.app_state = "login"
                st.rerun()

def login_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>Sign In</h2>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #f0c987;'>Access Your Dashboard</h4><br>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Sign In")
            
        with st.expander("New here? Sign Up"):
            with st.form("signup_form"):
                new_email = st.text_input("New Email")
                new_password = st.text_input("Create Password", type="password")
                signup_btn = st.form_submit_button("Create Account")
                
        st.markdown('</div>', unsafe_allow_html=True)
                
        if login_btn:
            if email and password:
                st.session_state.authenticated = True
                st.session_state.app_state = "main"
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Please provide email and password.")
        if signup_btn:
            if new_email and new_password:
                st.success("Account created – you can now sign in.")
            else:
                st.error("Please fill all sign‑up fields.")

if st.session_state.app_state == "splash":
    splash_screen()
    st.stop()
elif st.session_state.app_state == "login":
    login_page()
    st.stop()

# ---- Sidebar Navigation ----
st.sidebar.title("CareerForge AI Pro")
menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Input Profile",
        "Resume Analysis",
        "Technical Skills",
        "Communication & Confidence",
        "Portfolio & GitHub",
        "LinkedIn & Certifications",
        "Mock Interview",
        "Roadmap & Advice",
        "Download Report",
    ],
)

# ---- Theme Toggle ----
mode = st.sidebar.selectbox("Theme Mode", ["Light", "Dark"])
if mode == "Dark":
    st.markdown(
        """
        <style>
        body { background-color: #18191A; color: #E4E6EB; }
        .stSidebar { background-color: #242526; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ---- Helper Functions ----
def display_gauge(value, title):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title},
            gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#00CC96"}},
        )
    )
    st.plotly_chart(fig, use_container_width=True)

# ---- Page Logic ----
if menu == "Dashboard":
    st.subheader("Overall Interview Readiness")
    if st.session_state.scores:
        overall = st.session_state.scores.get("overall", 0)
        display_gauge(overall, "Readiness Score")
        st.write("**Category Breakdown**")
        col1, col2, col3, col4, col5 = st.columns(5)
        categories = [
            ("Technical Skills", st.session_state.scores.get("technical", 0)),
            ("Resume & ATS", st.session_state.scores.get("resume", 0)),
            ("Communication", st.session_state.scores.get("communication", 0)),
            ("Portfolio", st.session_state.scores.get("portfolio", 0)),
            ("Certifications", st.session_state.scores.get("certifications", 0)),
        ]
        for (col, (title, val)) in zip([col1, col2, col3, col4, col5], categories):
            with col:
                display_gauge(val, title)
        st.success("Navigate to other sections to refine your score.")
    else:
        st.info("Please fill out the profile and run analyses first.")

elif menu == "Input Profile":
    st.subheader("Provide Your Details")
    with st.form("profile_form"):
        st.text_input("Full Name", key="full_name")
        st.text_input("Email Address", key="email")
        st.text_input("College Name", key="college")
        st.text_input("Degree & Branch", key="degree")
        st.selectbox("Current Year of Study", ["1st", "2nd", "3rd", "4th", "Graduate"], key="year")
        st.text_input("CGPA", key="cgpa")
        st.text_input("Target Job Role", key="role")
        st.text_input("Dream Company", key="dream_company")
        st.text_area("Technical Skills (comma separated)", key="tech_skills")
        st.text_area("Programming Languages (comma separated)", key="languages")
        st.text_area("Frameworks & Tools (comma separated)", key="tools")
        st.text_area("Certifications", key="certifications")
        st.text_area("Internship Experience", key="internship")
        st.text_area("Projects Completed", key="projects")
        st.text_area("Achievements", key="achievements")
        st.text_area("Career Goals", key="goals")
        st.text_input("Preferred Industry", key="industry")
        submitted = st.form_submit_button("Save Profile")
        if submitted:
            st.session_state.profile = {
                k: v for k, v in st.session_state.items() if k in [
                    "full_name", "email", "college", "degree", "year", "cgpa", "role",
                    "dream_company", "tech_skills", "languages", "tools", "certifications",
                    "internship", "projects", "achievements", "goals", "industry",
                ]
            }
            st.success("Profile saved!")

elif menu == "Resume Analysis":
    st.subheader("Upload and Analyze Your Resume")
    uploaded = st.file_uploader("Upload PDF/DOCX", type=["pdf", "docx"])
    if uploaded:
        with st.spinner("Analyzing resume…"):
            resume_score = resume_analyzer.analyze(uploaded, st.session_state.profile.get("role", ""))
            st.session_state.scores["resume"] = resume_score
            st.success(f"Resume ATS Compatibility: {resume_score}%")
            display_gauge(resume_score, "Resume Score")

elif menu == "Technical Skills":
    st.subheader("Technical Skills Assessment")
    if st.session_state.profile:
        tech_score = technical_assessor.assess(
            st.session_state.profile.get("tech_skills", ""),
            st.session_state.profile.get("role", ""),
        )
        st.session_state.scores["technical"] = tech_score
        st.success(f"Technical Skills Score: {tech_score}%")
        display_gauge(tech_score, "Technical Score")
    else:
        st.warning("Please fill out your profile first.")

elif menu == "Communication & Confidence":
    st.subheader("Communication & Confidence Analyzer")
    # Simple text input for demo purposes
    answer = st.text_area("Paste a sample answer you wrote:")
    if answer:
        comm_score = communication_analyzer.evaluate(answer)
        conf_score = confidence_meter.evaluate(answer)
        combined = int((comm_score + conf_score) / 2)
        st.session_state.scores["communication"] = combined
        st.success(f"Combined Communication & Confidence Score: {combined}%")
        display_gauge(combined, "Comm & Confidence")

elif menu == "Portfolio & GitHub":
    st.subheader("Portfolio & GitHub Evaluation")
    github_url = st.text_input("GitHub Profile URL")
    portfolio_url = st.text_input("Portfolio Website URL")
    if github_url or portfolio_url:
        portfolio_score = portfolio_analyzer.evaluate(portfolio_url)
        github_score = github_analyzer.evaluate(github_url)
        avg = int((portfolio_score + github_score) / 2)
        st.session_state.scores["portfolio"] = avg
        st.success(f"Portfolio & GitHub Score: {avg}%")
        display_gauge(avg, "Portfolio Score")

elif menu == "LinkedIn & Certifications":
    st.subheader("LinkedIn & Certifications")
    linkedin_url = st.text_input("LinkedIn Profile URL")
    if linkedin_url:
        linkedin_score = linkedin_analyzer.evaluate(linkedin_url)
        cert_score = certification_gap.evaluate(
            st.session_state.profile.get("certifications", ""),
            st.session_state.profile.get("role", ""),
        )
        avg = int((linkedin_score + cert_score) / 2)
        st.session_state.scores["certifications"] = avg
        st.success(f"LinkedIn & Certifications Score: {avg}%")
        display_gauge(avg, "Certifications Score")

elif menu == "Mock Interview":
    st.subheader("Mock Interview Simulator")
    st.info("This feature is under development. Stay tuned!")

elif menu == "Roadmap & Advice":
    st.subheader("Personalized Learning Roadmap")
    if st.session_state.scores:
        roadmap = roadmap_generator.generate(st.session_state.profile, st.session_state.scores)
        st.write(roadmap)
    else:
        st.warning("Run some analyses first to generate a roadmap.")

elif menu == "Download Report":
    st.subheader("Generate PDF Report")
    if st.session_state.scores:
        pdf_bytes = pdf_report.create_report(st.session_state.profile, st.session_state.scores)
        st.download_button(
            label="Download Report PDF",
            data=pdf_bytes,
            file_name="careerforge_report.pdf",
            mime="application/pdf",
        )
        qr_img = qr_generator.generate_qr("careerforge_report.pdf")
        st.image(qr_img, caption="Shareable QR Code")
    else:
        st.info("No data to generate report yet.")

# ---- Compute Overall Score ----
if st.session_state.scores:
    overall = scoring_engine.compute_overall(st.session_state.scores)
    st.session_state.scores["overall"] = overall


# End of application (duplicate section removed)
