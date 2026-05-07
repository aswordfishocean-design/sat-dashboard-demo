import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- 1. เชื่อมต่อข้อมูลจาก Google Sheet V2 ---
sheet_id = "1qTeQHY74MxOPx_gxXwrkB4pX8bRrqaG4WTox3vHIPVw" 
sheet_name = "SAT%20Information%20Dashboard%20V2"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

@st.cache_data(ttl=60) # อัปเดตข้อมูลทุก 1 นาที
def load_data():
    df = pd.read_csv(url)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"เชื่อมต่อข้อมูลไม่ได้: {e}")
    st.stop()

# --- 2. ตั้งค่าหน้าตาแอป (aims Branding) ---
st.set_page_config(page_title="aims SAT Dashboard", layout="wide")

# ปรับ CSS ให้ดู Professional เหมือนแอปจริง
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    div[data-testid="metric-container"] {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        border: 1px solid #e2e8f0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ส่วน Login ---
st.sidebar.title("🔐 Login Portal")
role = st.sidebar.radio("บทบาท:", ["Student", "Teacher", "Admin"])

if role == "Student":
    # เลือกชื่อนักเรียน
    student_list = df['Student Name'].unique()
    student_name = st.sidebar.selectbox("เลือกชื่อนักเรียน:", student_list)
    student_data = df[df['Student Name'] == student_name].sort_values('Date')
    
    # ส่วนหัว Dashboard
    st.title(f"✨ Performance Report: {student_name}")
    st.caption(f"Digital SAT Tracker • {student_data['Course Level'].iloc[0]}")
    
    # --- KPIs สรุปผล ---
    latest = student_data.iloc[-1]
    target = latest['Target Score']
    best = student_data['Total Score'].max()
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("คะแนนล่าสุด", int(latest['Total Score']), f"{int(latest['Total Score'] - target)} vs Target")
    with c2:
        st.metric("คะแนนสูงสุด (Best)", int(best))
    with c3:
        progress = int((best / target) * 100)
        st.metric("ความสำเร็จ", f"{progress}%")
        st.progress(progress / 100)

    st.divider()

    # --- กราฟวิเคราะห์ ---
    col_left, col_right = st.columns([2, 1.2])
    
    with col_left:
        st.subheader("📈 Score Trend (พัฒนาการย้อนหลัง)")
        fig_trend = px.line(student_data, x='Date', y='Total Score', markers=True, text='Total Score', template="plotly_white")
        fig_trend.update_traces(textposition="top center", line_color='#0284c7', marker=dict(size=10))
        fig_trend.update_layout(yaxis_range=[400, 1600])
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_right:
        st.subheader("🎯 Skill Radar (วิเคราะห์จุดแข็ง-อ่อน)")
        # ข้อมูลสำหรับ Radar Chart
        rw_cats = ['Craft & Structure', 'Info & Ideas', 'Standard English', 'Expression of Ideas']
        rw_vals = [latest['R&W Craft & Structure (%)'], latest['R&W Info & Ideas (%)'], 
                   latest['R&W Standard English (%)'], latest['R&W Expression of Ideas (%)']]
        
        math_cats = ['Algebra', 'Problem Solving', 'Advanced Math', 'Additional Topics']
        math_vals = [latest['Math Algebra (%)'], latest['Math Problem Solving (%)'], 
                     latest['Math Advanced Math (%)'], latest['Math Additional Topics (%)']]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=rw_vals, theta=rw_cats, fill='toself', name='Reading & Writing', line_color='#f43f5e'))
        fig_radar.add_trace(go.Scatterpolar(r=math_vals, theta=math_cats, fill='toself', name='Math', line_color='#0ea5e9'))
        
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True)
        st.plotly_chart(fig_radar, use_container_width=True)

    # --- ส่วนแนะนำจากน้องใจดี ---
    st.subheader("📝 Smart Insights โดยน้องใจดี")
    with st.container():
        st.info(f"💡 สำหรับครั้งล่าสุด น้อง {student_name} ทำได้ดีมากในพาร์ทที่คะแนนสูงสุดคือ {max(rw_vals + math_vals)}% ค่ะ! พยายามเน้นหัวข้อที่กราฟใยแมงมุมยุบตัวลงไปเพื่อเพิ่มคะแนนให้ถึง {int(target)} นะคะ")

else:
    # หน้าสำหรับบทบาทอื่น
    st.title(f"🛠️ ระบบจัดการสำหรับ {role}")
    st.write("ตารางข้อมูลนักเรียนทั้งหมด:")
    st.dataframe(df, use_container_width=True)
