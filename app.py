import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- 1. การเชื่อมต่อข้อมูล (Google Sheet V2) ---
sheet_id = "1qTeQHY74MxOPx_gxXwrkB4pX8bRrqaG4WTox3vHIPVw" 
sheet_name = "SAT%20Information%20Dashboard%20V2"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

@st.cache_data(ttl=60) # รีเฟรชข้อมูลทุก 1 นาที
def load_data():
    df = pd.read_csv(url)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"เชื่อมต่อข้อมูลไม่ได้: {e}")
    st.stop()

# --- 2. การตั้งค่าหน้าตาแอป ---
st.set_page_config(page_title="aims SAT Dashboard", layout="wide")

# ปรับแต่ง CSS ให้ดูสะอาดตา (Theme Blue/White)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stMetric { background-color: white; padding: 20px; border-radius: 20px; border: 1px solid #e2e8f0; }
    .detail-card { background-color: white; padding: 25px; border-radius: 20px; border: 1px solid #e2e8f0; }
    .topic-row { display: flex; justify-content: space-between; padding: 8px; border-bottom: 1px solid #f1f5f9; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Sidebar (เหลือแค่ Student & Admin) ---
st.sidebar.title("🔐 aims Portal")
role = st.sidebar.radio("เข้าสู่ระบบในฐานะ:", ["Student", "Admin"])

# ==========================================
# 4. หน้า STUDENTS (Professional View)
# ==========================================
if role == "Student":
    student_list = df['Student Name'].unique()
    student_name = st.sidebar.selectbox("เลือกชื่อนักเรียน:", student_list)
    
    # กรองข้อมูลเฉพาะของนักเรียน
    s_data = df[df['Student Name'] == student_name].sort_values('Date')
    latest = s_data.iloc[-1]
    best_score = s_data['Total Score'].max()
    target = latest['Target Score']
    
    # Header
    st.markdown("<div style='display: flex; align-items: center; gap: 10px;'><span style='background-color: #0284c7; color: white; padding: 4px 12px; border-radius: 20px; font-size: 14px; font-weight: bold;'>Digital SAT</span><span style='color: #64748b; font-size: 14px;'>Performance Report</span></div>", unsafe_allow_html=True)
    st.title(f"{student_name}")
    st.markdown(f"<p style='color: #64748b;'>Target Score: <b>{int(target)}</b> | Course: {latest['Course Level']}</p>", unsafe_allow_html=True)

    # Top Metrics
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("✨ Latest Score", int(latest['Total Score']), f"Test: {latest['Test Form']}")
    with c2:
        st.metric("🏆 Best Score", int(best_score))
    with c3:
        progress = int((best_score / target) * 100)
        st.metric("🎯 Progress", f"{progress}%", f"Gap: {int(target - best_score)}")
        st.progress(progress / 100)

    st.divider()

    # Layout: กราฟเทรนด์ และ รายละเอียด
    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("📈 Score Trend")
        # กราฟแท่งแนวนอนแบบที่พี่มหาชอบ (Math ทึบ, RW โปร่ง)
        fig = go.Figure()
        fig.add_trace(go.Bar(y=s_data['Date'].astype(str), x=s_data['Math Score'], name='Math', orientation='h', marker_color='#0284c7', width=0.4))
        fig.add_trace(go.Bar(y=s_data['Date'].astype(str), x=s_data['R&W Score'], name='Reading & Writing', orientation='h', marker_color='rgba(0,0,0,0)', marker_line_color='#0284c7', marker_line_width=2, width=0.4))
        
        fig.update_layout(barmode='group', xaxis=dict(range=[200, 800]), yaxis=dict(autorange="reversed"), height=450, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with right_col:
        st.markdown("<div class='detail-card'>", unsafe_allow_html=True)
        st.subheader("Attempt Detail")
        st.write(f"**Date:** {latest['Date']}")
        
        # Breakdown รายบทเรียน (ดึงจาก % ใน Sheet)
        st.markdown("---")
        st.write("**Reading & Writing Breakdown**")
        rw_topics = {
            "Craft & Structure": latest['R&W Craft & Structure (%)'],
            "Information & Ideas": latest['R&W Info & Ideas (%)'],
            "Standard English": latest['R&W Standard English (%)'],
            "Expression of Ideas": latest['R&W Expression of Ideas (%)']
        }
        for t, v in rw_topics.items():
            st.markdown(f"<div class='topic-row'><span>{t}</span><b>{int(v)}%</b></div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("**Math Breakdown**")
        math_topics = {
            "Algebra": latest['Math Algebra (%)'],
            "Problem Solving": latest['Math Problem Solving (%)'],
            "Advanced Math": latest['Math Advanced Math (%)'],
            "Additional Topics": latest['Math Additional Topics (%)']
        }
        for t, v in math_topics.items():
            st.markdown(f"<div class='topic-row'><span>{t}</span><b>{int(v)}%</b></div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 5. หน้า ADMIN
# ==========================================
else:
    st.title("⚙️ Admin Control Center")
    st.subheader("ภาพรวมข้อมูลนักเรียนทั้งหมด (Database View)")
    
    # แสดงตารางข้อมูลดิบ
    st.dataframe(df, use_container_width=True)
    
    st.divider()
    st.subheader("📊 Class Statistics")
    avg_score = df['Total Score'].mean()
    st.info(f"ค่าเฉลี่ยคะแนนรวมของนักเรียนทุกคนในระบบ: {avg_score:.2f}")
