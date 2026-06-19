import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from datetime import datetime
import os
import base64

st.set_page_config(
    page_title="AttendAI — Smart Attendance",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Inject CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0B1120 !important;
    color: #E8EDFB !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

[data-testid="stAppViewContainer"] > .main {
    background: #0B1120 !important;
}

[data-testid="stHeader"] { background: transparent !important; }

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0B1120; }
::-webkit-scrollbar-thumb { background: #1E2D4A; border-radius: 3px; }

/* ── Top Nav Bar ── */
.nav-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 32px;
    background: rgba(19, 28, 46, 0.85);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(0, 212, 255, 0.12);
    margin: -1rem -1rem 2rem -1rem;
    position: sticky;
    top: 0;
    z-index: 100;
}

.nav-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 1.2rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #E8EDFB;
}

.nav-logo .logo-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #00D4FF, #0088CC);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
}

.nav-logo .brand-accent { color: #00D4FF; }

.nav-pill {
    background: rgba(0, 212, 255, 0.08);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    color: #00D4FF;
    letter-spacing: 0.05em;
}

/* ── Section headers ── */
.section-eyebrow {
    font-size: 0.7rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.12em;
    color: #00D4FF;
    text-transform: uppercase;
    margin-bottom: 6px;
    opacity: 0.8;
}

.section-title {
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #E8EDFB;
    margin-bottom: 1.5rem;
}

/* ── Cards ── */
.card {
    background: #131C2E;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 28px;
    position: relative;
    overflow: hidden;
}

.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,212,255,0.25), transparent);
}

/* ── Form fields ── */
[data-testid="stTextInput"] label {
    font-size: 0.75rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    letter-spacing: 0.08em !important;
    color: #7B8DB0 !important;
    text-transform: uppercase !important;
    margin-bottom: 6px !important;
}

[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #E8EDFB !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 10px 14px !important;
    transition: border-color 0.2s !important;
}

[data-testid="stTextInput"] input:focus {
    border-color: rgba(0, 212, 255, 0.4) !important;
    box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.06) !important;
    outline: none !important;
}

/* ── Upload zone ── */
[data-testid="stFileUploader"] {
    background: rgba(0, 212, 255, 0.03) !important;
    border: 1.5px dashed rgba(0, 212, 255, 0.25) !important;
    border-radius: 14px !important;
    transition: border-color 0.2s, background 0.2s !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: rgba(0, 212, 255, 0.5) !important;
    background: rgba(0, 212, 255, 0.06) !important;
}

[data-testid="stFileUploader"] label {
    color: #7B8DB0 !important;
    font-size: 0.85rem !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] {
    color: #7B8DB0 !important;
}

/* ── Buttons ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #00D4FF, #0088CC) !important;
    color: #0B1120 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    width: 100% !important;
    letter-spacing: 0.01em !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 4px 20px rgba(0, 212, 255, 0.25) !important;
}

[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Alerts ── */
[data-testid="stSuccess"] {
    background: rgba(0, 229, 138, 0.08) !important;
    border: 1px solid rgba(0, 229, 138, 0.2) !important;
    border-radius: 10px !important;
    color: #00E58A !important;
}

[data-testid="stError"] {
    background: rgba(255, 77, 106, 0.08) !important;
    border: 1px solid rgba(255, 77, 106, 0.2) !important;
    border-radius: 10px !important;
    color: #FF4D6A !important;
}

[data-testid="stInfo"] {
    background: rgba(0, 212, 255, 0.06) !important;
    border: 1px solid rgba(0, 212, 255, 0.15) !important;
    border-radius: 10px !important;
    color: #7EC8E3 !important;
}

[data-testid="stWarning"] {
    background: rgba(255, 178, 50, 0.08) !important;
    border: 1px solid rgba(255, 178, 50, 0.2) !important;
    border-radius: 10px !important;
}

/* ── Images ── */
[data-testid="stImage"] img {
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
}

[data-testid="stDataFrame"] iframe {
    border-radius: 12px !important;
}

/* ── Divider ── */
[data-testid="stDivider"] hr {
    border-color: rgba(255,255,255,0.06) !important;
    margin: 2rem 0 !important;
}

/* ── Metric cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 2rem;
}

.metric-card {
    background: #131C2E;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
}

.metric-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    border-radius: 0 0 0 14px;
}

.metric-card.blue::after  { background: #00D4FF; }
.metric-card.green::after { background: #00E58A; }
.metric-card.red::after   { background: #FF4D6A; }

.metric-label {
    font-size: 0.7rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #7B8DB0;
    margin-bottom: 8px;
}

.metric-value {
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1;
}

.metric-card.blue  .metric-value { color: #00D4FF; }
.metric-card.green .metric-value { color: #00E58A; }
.metric-card.red   .metric-value { color: #FF4D6A; }

.metric-sub {
    font-size: 0.75rem;
    color: #4A5A78;
    margin-top: 4px;
}

/* ── Scan badge ── */
.scan-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(0, 229, 138, 0.1);
    border: 1px solid rgba(0, 229, 138, 0.25);
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    color: #00E58A;
    letter-spacing: 0.06em;
    margin-bottom: 16px;
}

.scan-badge-absent {
    background: rgba(255, 77, 106, 0.1);
    border-color: rgba(255, 77, 106, 0.25);
    color: #FF4D6A;
}

.pulse-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #00E58A;
    animation: pulse 1.6s ease-in-out infinite;
    flex-shrink: 0;
}

.pulse-dot-red { background: #FF4D6A; }

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.7); }
}

/* ── Column wrappers ── */
[data-testid="column"] {
    padding: 0 8px !important;
}

/* ── Sticky section divider ── */
.divider-label {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 2.5rem 0 1.5rem;
}

.divider-label span {
    font-size: 0.7rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4A5A78;
    white-space: nowrap;
}

.divider-line {
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.06);
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 48px 24px;
    color: #4A5A78;
}

.empty-state .empty-icon {
    font-size: 2.5rem;
    margin-bottom: 12px;
    opacity: 0.5;
}

.empty-state p {
    font-size: 0.875rem;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ── Setup ───────────────────────────────────────────────────────────────────
os.makedirs("data", exist_ok=True)
os.makedirs("output", exist_ok=True)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ── Nav Bar ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav-bar">
    <div class="nav-logo">
        <div class="logo-icon">🎓</div>
        <span>Attend<span class="brand-accent">AI</span></span>
    </div>
    <div class="nav-pill">v2.0 · LIVE</div>
</div>
""", unsafe_allow_html=True)

# ── Metric Summary (if data exists) ─────────────────────────────────────────
FILE_PATH = "data/attendance_ui.csv"
if os.path.exists(FILE_PATH):
    df_all = pd.read_csv(FILE_PATH)
    total   = len(df_all)
    present = len(df_all[df_all["Status"] == "Present"])
    absent  = total - present
    rate    = f"{(present/total*100):.0f}%" if total > 0 else "—"

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card blue">
            <div class="metric-label">Total Records</div>
            <div class="metric-value">{total}</div>
            <div class="metric-sub">All-time entries</div>
        </div>
        <div class="metric-card green">
            <div class="metric-label">Present</div>
            <div class="metric-value">{present}</div>
            <div class="metric-sub">Face detected</div>
        </div>
        <div class="metric-card red">
            <div class="metric-label">Absent</div>
            <div class="metric-value">{absent}</div>
            <div class="metric-sub">No face detected</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Main Columns ─────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("""
    <div class="section-eyebrow">Step 01</div>
    <div class="section-title">Register Student</div>
    """, unsafe_allow_html=True)

    with st.container():
        student_id   = st.text_input("Student ID",   "S001", placeholder="e.g. S001")
        student_name = st.text_input("Student Name", "Student_1", placeholder="e.g. Jane Doe")

        uploaded_file = st.file_uploader(
            "Drop a face image here, or click to browse",
            type=["jpg", "jpeg", "png"],
            label_visibility="visible"
        )

with col2:
    st.markdown("""
    <div class="section-eyebrow">Step 02</div>
    <div class="section-title">Detection Result</div>
    """, unsafe_allow_html=True)

    if uploaded_file is not None:
        image    = Image.open(uploaded_file)
        image_np = np.array(image)
        gray     = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5
        )

        for (x, y, w, h) in faces:
            # Draw a cyan rounded rectangle
            cv2.rectangle(image_np, (x, y), (x + w, y + h), (0, 212, 255), 3)
            # Corner ticks
            tick = 14
            cv2.line(image_np, (x, y), (x + tick, y), (0, 212, 255), 5)
            cv2.line(image_np, (x, y), (x, y + tick), (0, 212, 255), 5)
            cv2.line(image_np, (x + w, y), (x + w - tick, y), (0, 212, 255), 5)
            cv2.line(image_np, (x + w, y), (x + w, y + tick), (0, 212, 255), 5)
            cv2.line(image_np, (x, y + h), (x + tick, y + h), (0, 212, 255), 5)
            cv2.line(image_np, (x, y + h), (x, y + h - tick), (0, 212, 255), 5)
            cv2.line(image_np, (x + w, y + h), (x + w - tick, y + h), (0, 212, 255), 5)
            cv2.line(image_np, (x + w, y + h), (x + w, y + h - tick), (0, 212, 255), 5)

        if len(faces) > 0:
            status = "Present"
            st.markdown("""
            <div class="scan-badge">
                <div class="pulse-dot"></div>
                FACE DETECTED · PRESENT
            </div>""", unsafe_allow_html=True)
            st.success(f"✓ Identity confirmed — {len(faces)} face(s) located in frame.")
        else:
            status = "Absent"
            st.markdown("""
            <div class="scan-badge scan-badge-absent">
                <div class="pulse-dot pulse-dot-red"></div>
                NO FACE · ABSENT
            </div>""", unsafe_allow_html=True)
            st.error("✗ No face detected. Attendance marked absent.")

        st.image(image_np, caption="Scan output", use_container_width=True)

        attendance_record = {
            "Student_ID":    student_id,
            "Name":          student_name,
            "Date":          datetime.now().strftime("%Y-%m-%d"),
            "Time":          datetime.now().strftime("%H:%M:%S"),
            "Face_Detected": 1 if len(faces) > 0 else 0,
            "Status":        status
        }

        if st.button("💾  Save Attendance Record"):
            if os.path.exists(FILE_PATH):
                df_existing = pd.read_csv(FILE_PATH)
                df_new = pd.concat(
                    [df_existing, pd.DataFrame([attendance_record])],
                    ignore_index=True
                )
            else:
                df_new = pd.DataFrame([attendance_record])

            df_new.to_csv(FILE_PATH, index=False)
            st.success("Record saved — refresh the page to update analytics.")

    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🔍</div>
            <p>Upload a student image on the left<br>to begin face detection.</p>
        </div>
        """, unsafe_allow_html=True)

# ── Records Table ────────────────────────────────────────────────────────────
st.markdown("""
<div class="divider-label">
    <div class="divider-line"></div>
    <span>Attendance Log</span>
    <div class="divider-line"></div>
</div>
""", unsafe_allow_html=True)

if os.path.exists(FILE_PATH):
    df_show = pd.read_csv(FILE_PATH)
    # Color-code Status column
    st.dataframe(
        df_show,
        use_container_width=True,
        height=320,
        column_config={
            "Student_ID":    st.column_config.TextColumn("ID"),
            "Name":          st.column_config.TextColumn("Student Name"),
            "Date":          st.column_config.TextColumn("Date"),
            "Time":          st.column_config.TextColumn("Time"),
            "Face_Detected": st.column_config.NumberColumn("Face", format="%d"),
            "Status":        st.column_config.TextColumn("Status"),
        }
    )
else:
    st.markdown("""
    <div class="empty-state" style="border:1px solid rgba(255,255,255,0.06);border-radius:14px;">
        <div class="empty-icon">📋</div>
        <p>No records yet.<br>Save your first attendance entry above.</p>
    </div>
    """, unsafe_allow_html=True)