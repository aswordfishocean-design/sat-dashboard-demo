import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. การเชื่อมต่อข้อมูล (Google Sheet V2) ---
sheet_id = "1qTeQHY74MxOPx_gxXwrkB4pX8bRrqaG4WTox3vHIPVw" 
sheet_name = "SAT%20Information%20Dashboard%20V2"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(url)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"เชื่อมต่อข้อมูลไม่ได้: {e}")
    st.stop()

# --- 2. ตั้งค่าหน้าตาแอป & CSS (ตามแบบที่พี่มหาต้องการ) ---
st.set_page_config(page_title="aims SAT Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stMetric { background-color: white; padding: 20px; border-radius: 20px; border: 1px solid #e0f2fe; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    .attempt-card { background-color: white; padding: 25px; border-radius: 20px; border: 1px solid #e0f2fe; }
    .topic-box { background-color: white; padding: 12px 18px; border: 1px solid #e2e8f0; border-radius: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .insight-box { background-color: #f0f9ff; padding: 15px; border-radius: 15px; border: 1px solid #e0f2fe; margin-top: 15px; }
    .q-chip { background-color: white; border: 1px solid #e2e8f0; padding: 5px 12px; border-radius: 10px; font-size: 13px; font-weight: 500; margin-right: 5px; margin-bottom: 5px; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ระบบจัดการสถานะ (Session State) ---
# เริ่มต้นให้เลือก Attempt ล่าสุดไว้ก่อน
if 'selected_attempt_idx' not in st.session_state:
    st.session_state.selected_attempt_idx = len(df) - 1

# --- 4. Header & Top Metrics ---
# กรองข้อมูลนักเรียน (ตัวอย่าง: Aphiphongphiphut)
student_name = "Aphiphongphiphut Kaweeyarn"
s_data = df[df['Student Name'] == student_name].sort_values('Date').reset_index(drop=True)
best_score = s_data['Total Score'].max()
target = 1500  # กำหนดเป้าหมาย 1500 คะแนนเท่ากันทุกคนตามที่พี่มหาต้องการ

st.markdown("<div style='display: flex; align-items: center; gap: 10px;'><span style='background-color: #0284c7; color: white; padding: 4px 12px; border-radius: 20px; font-size: 14px; font-weight: bold;'>Digital SAT</span><span style='color: #64748b; font-size: 14px;'>Performance Report</span></div>", unsafe_allow_html=True)
st.title(student_name)
st.markdown(f"<p style='color: #64748b;'>Target Score: <b>{target}</b></p>", unsafe_allow_html=True)

# ข้อมูลของ Attempt ที่ถูกเลือก
current_idx = st.session_state.selected_attempt_idx
selected_data = s_data.iloc[current_idx]

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("✨ Latest Score", int(selected_data['Total Score']), f"Attempt {current_idx + 1} • {selected_data['Date']}")
with c2:
    st.metric("🏆 Best Score Achieved", int(best_score))
with c3:
    progress = int((best_score / target) * 100)
    st.metric("🎯 Progress to Target", f"{progress}%", f"Gap: {target - best_score}")
    st.progress(progress / 100)

st.divider()

# --- 5. Main Layout (2 Columns) ---
left_col, right_col = st.columns([2, 1])

# --- 5.1 ฝั่งซ้าย: กราฟ Score Trend & ปุ่มเลือก Attempt ---
with left_col:
    st.subheader("Score Trend (Click a bar to inspect)")
    
    fig = go.Figure()
    # Math Bar
    fig.add_trace(go.Bar(y=[f"Attempt {i+1}" for i in range(len(s_data))], x=s_data['Math Score'], name='Math', orientation='h', marker_color='#0284c7', width=0.4))
    # R&W Bar
    fig.add_trace(go.Bar(y=[f"Attempt {i+1}" for i in range(len(s_data))], x=s_data['R&W Score'], name='Reading & Writing', orientation='h', marker_color='rgba(0,0,0,0)', marker_line_color='#0284c7', marker_line_width=2, width=0.4))
    
    fig.update_layout(barmode='group', xaxis=dict(range=[200, 800]), yaxis=dict(autorange="reversed"), height=500, margin=dict(l=0, r=0, t=20, b=0), plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    
    # ปุ่มเลือก Attempt (เมื่อกดแล้วจะเปลี่ยนค่าใน Session State และรันใหม่)
    cols = st.columns(len(s_data))
    for i in range(len(s_data)):
        if cols[i].button(f"Attempt {i+1}", key=f"btn_{i}", use_container_width=True, type="primary" if i == current_idx else "secondary"):
            st.session_state.selected_attempt_idx = i
            st.rerun()

# --- 5.2 ฝั่งขวา: Attempt Detail (อัปเดตตามปุ่มที่กด) ---
with right_col:
    st.markdown("<div class='attempt-card'>", unsafe_allow_html=True)
    st.subheader("Attempt Detail")
    st.caption("Details reflect the selected attempt from the left.")
    
    # ส่วนหัว Card
    ca, cb = st.columns([2, 1])
    ca.markdown(f"**Attempt {current_idx + 1}**<br><span style='color: #64748b;'>{selected_data['Date']}</span>", unsafe_allow_html=True)
    cb.markdown(f"<span style='background-color: #e0f2fe; color: #0369a1; padding: 6px 12px; border-radius: 20px; font-weight: bold;'>Total {int(selected_data['Total Score'])}</span>", unsafe_allow_html=True)
    
    # คะแนนแยกวิชา
    s1, s2 = st.columns(2)
    m_score = int(selected_data['Math Score'])
    rw_score = int(selected_data['R&W Score'])
    s1.markdown(f"<div style='border: 1px solid #e2e8f0; padding: 15px; border-radius: 15px;'> <span style='font-size: 12px; color: #64748b;'>Math</span><br><b style='font-size: 24px;'>{m_score}</b><br><span style='font-size: 12px; color: #0284c7;'>{'Strong' if m_score >= 700 else 'Developing'}</span> </div>", unsafe_allow_html=True)
    s2.markdown(f"<div style='border: 1px solid #e2e8f0; padding: 15px; border-radius: 15px;'> <span style='font-size: 12px; color: #64748b;'>R&W</span><br><b style='font-size: 24px;'>{rw_score}</b><br><span style='font-size: 12px; color: #0284c7;'>{'Strong' if rw_score >= 700 else 'Developing'}</span> </div>", unsafe_allow_html=True)
    
    # Tabs สำหรับวิเคราะห์จุดอ่อนรายบท
    t_math, t_rw = st.tabs(["Math", "R&W"])
    
    with t_math:
        st.markdown("<div style='display: flex; justify-content: space-between; margin-top: 10px;'><b>Topic Breakdown</b> <span style='background-color: #0284c7; color: white; padding: 2px 10px; border-radius: 10px; font-size: 12px;'>📊</span></div>", unsafe_allow_html=True)
        math_topics = {
            "Algebra": selected_data['Math Algebra (%)'],
            "Problem Solving": selected_data['Math Problem Solving (%)'],
            "Advanced Math": selected_data['Math Advanced Math (%)'],
            "Additional Topics": selected_data['Math Additional Topics (%)']
        }
        for t, v in math_topics.items():
            st.markdown(f"<div class='topic-box'><span>{t}</span><b>{int(v)}%</b></div>", unsafe_allow_html=True)

    with t_rw:
        st.markdown("<div style='display: flex; justify-content: space-between; margin-top: 10px;'><b>Topic Breakdown</b> <span style='background-color: #0284c7; color: white; padding: 2px 10px; border-radius: 10px; font-size: 12px;'>📊</span></div>", unsafe_allow_html=True)
        rw_topics = {
            "Craft & Structure": selected_data['R&W Craft & Structure (%)'],
            "Info & Ideas": selected_data['R&W Info & Ideas (%)'],
            "Standard English": selected_data['R&W Standard English (%)'],
            "Expression of Ideas": selected_data['R&W Expression of Ideas (%)']
        }
        for t, v in rw_topics.items():
            st.markdown(f"<div class='topic-box'><span>{t}</span><b>{int(v)}%</b></div>", unsafe_allow_html=True)

    # Smart Insight & Incorrect Questions (ตามแบบ image_9.png)
    st.markdown(f"""
        <div class='insight-box'>
            <b style='color: #0369a1;'>ℹ️ Smart Insight</b><br>
            <span style='font-size: 13px; color: #0c4a6e;'>
                ครั้งนี้น้องทำได้ดีที่สุดในหัวข้อ <b>{max(math_topics, key=math_topics.get)}</b> ค่ะ 
                พยายามเน้นทบทวนบทเรียนที่คะแนนยังไม่ถึงเป้าเพื่อพุ่งสู่ 1500 นะคะ
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    st.write(" ")
    st.subheader("Incorrect Questions")
    # ตัวอย่างการแสดงเลขข้อที่ผิด (สามารถปรับให้ดึงจาก Sheet ได้ถ้ามีคอลัมน์เก็บไว้)
    wrong_qs = ["Q10", "Q14", "Q16", "Q18", "Q19", "Q21", "Q22"]
    for q in wrong_qs:
        st.markdown(f"<span class='q-chip'>{q}</span>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
