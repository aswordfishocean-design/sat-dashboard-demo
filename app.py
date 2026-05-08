import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. เชื่อมต่อฐานข้อมูล V3 (ล่าสุดที่มีข้อมูลน้อง Pharin และ Aphiphongphiphut ครบ 16 รายการ) ---
sheet_id = "1ZqScd-XtnaR6zTITejMVIbpIW-MAXa2YphOu6PXaCiI" 
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=10)
def load_data():
    df = pd.read_csv(url)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"เชื่อมต่อข้อมูลไม่ได้: {e}")
    st.stop()

# --- 2. ตั้งค่าหน้าตาแอป & CSS ---
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

# --- 3. Sidebar ---
st.sidebar.title("🔐 aims Portal")
role = st.sidebar.radio("เข้าสู่ระบบในฐานะ:", ["Student", "Admin"])

if role == "Student":
    student_list = df['Student Name'].unique()
    student_name = st.sidebar.selectbox("เลือกชื่อนักเรียน:", student_list)
    
    # กรองข้อมูลและ Reset Index เพื่อความแม่นยำ
    s_data = df[df['Student Name'] == student_name].sort_values('Date').reset_index(drop=True)
    
    if len(s_data) == 0:
        st.warning("ไม่พบข้อมูลนักเรียนคนนี้ในระบบ")
    else:
        # --- [จุดแก้ไขสำคัญ] ระบบล็อค Index ให้ปลอดภัย ---
        # 1. ถ้าเปลี่ยนชื่อคน ให้รีเซ็ตไปที่ครั้งล่าสุดของคนนั้นเสมอ
        if "active_student" not in st.session_state or st.session_state.active_student != student_name:
            st.session_state.active_student = student_name
            st.session_state.selected_idx = len(s_data) - 1
            
        # 2. ตรวจสอบว่า Index ที่จำไว้ ไม่เกินจำนวนครั้งที่สอบจริง
        if st.session_state.selected_idx >= len(s_data):
            st.session_state.selected_idx = len(s_data) - 1
        
        # 3. ดึงข้อมูลมาแสดงผล (ใช้ค่าที่ผ่านการเช็คแล้ว)
        current_idx = st.session_state.selected_idx
        selected_attempt = s_data.iloc[current_idx]
        
        best_score = s_data['Total Score'].max()
        target = 1500 

        # Header & Metrics
        st.markdown("<div style='display: flex; align-items: center; gap: 10px;'><span style='background-color: #0284c7; color: white; padding: 4px 12px; border-radius: 20px; font-size: 14px; font-weight: bold;'>Digital SAT</span><span style='color: #64748b; font-size: 14px;'>Performance Report</span></div>", unsafe_allow_html=True)
        st.title(f"{student_name}")
        st.markdown(f"<p style='color: #64748b;'>Target Score: <b>{target}</b></p>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1: st.metric("✨ Selected Score", int(selected_attempt['Total Score']), f"Attempt {current_idx + 1}")
        with c2: st.metric("🏆 Best Score Achieved", int(best_score))
        with c3:
            progress = int((best_score / target) * 100)
            gap = target - int(best_score)
            st.metric("🎯 Progress to Target", f"{progress}%", f"Gap: {gap}")
            st.progress(progress / 100)

        st.divider()

        # Layout 2 Columns
        left_col, right_col = st.columns([2, 1])

        with left_col:
            st.subheader("Score Trend")
            fig = go.Figure()
            fig.add_trace(go.Bar(y=[f"Attempt {i+1}" for i in range(len(s_data))], x=s_data['Math Score'], name='Math', orientation='h', marker_color='#0284c7', width=0.4))
            fig.add_trace(go.Bar(y=[f"Attempt {i+1}" for i in range(len(s_data))], x=s_data['R&W Score'], name='Reading & Writing', orientation='h', marker_color='rgba(0,0,0,0)', marker_line_color='#0284c7', marker_line_width=2, width=0.4))
            fig.update_layout(barmode='group', xaxis=dict(range=[200, 800]), yaxis=dict(autorange="reversed"), height=500, margin=dict(l=0, r=0, t=20, b=0), plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            
            # ปุ่มเลือก Attempt
            btn_cols = st.columns(len(s_data))
            for i in range(len(s_data)):
                if btn_cols[i].button(f"Attempt {i+1}", key=f"btn_{i}", use_container_width=True, type="primary" if i == current_idx else "secondary"):
                    st.session_state.selected_idx = i
                    st.rerun()

        with right_col:
            st.markdown("<div class='attempt-card'>", unsafe_allow_html=True)
            st.subheader("Attempt Detail")
            ca, cb = st.columns([2, 1])
            ca.markdown(f"**Attempt {current_idx + 1}**<br><span style='color: #64748b;'>{selected_attempt['Date']}</span>", unsafe_allow_html=True)
            cb.markdown(f"<span style='background-color: #e0f2fe; color: #0369a1; padding: 6px 12px; border-radius: 20px; font-weight: bold;'>Total {int(selected_attempt['Total Score'])}</span>", unsafe_allow_html=True)
            
            s1, s2 = st.columns(2)
            m_val, rw_val = int(selected_attempt['Math Score']), int(selected_attempt['R&W Score'])
            s1.markdown(f"<div style='border: 1px solid #e2e8f0; padding: 15px; border-radius: 15px;'> <span style='font-size: 12px; color: #64748b;'>Math</span><br><b style='font-size: 24px;'>{m_val}</b><br><span style='font-size: 12px; color: #0284c7;'>{'Strong' if m_val >= 700 else 'Developing'}</span> </div>", unsafe_allow_html=True)
            s2.markdown(f"<div style='border: 1px solid #e2e8f0; padding: 15px; border-radius: 15px;'> <span style='font-size: 12px; color: #64748b;'>R&W</span><br><b style='font-size: 24px;'>{rw_val}</b><br><span style='font-size: 12px; color: #0284c7;'>{'Strong' if rw_val >= 700 else 'Developing'}</span> </div>", unsafe_allow_html=True)
            
            t_math, t_rw = st.tabs(["Math Topics", "R&W Topics"])
            with t_math:
                m_t = {"Algebra": selected_attempt['Math Algebra (%)'], "Problem Solving": selected_attempt['Math Problem Solving (%)'], "Advanced Math": selected_attempt['Math Advanced Math (%)'], "Additional Topics": selected_attempt['Math Additional Topics (%)']}
                for t, v in m_t.items(): st.markdown(f"<div class='topic-box'><span>{t}</span><b>{int(v)}%</b></div>", unsafe_allow_html=True)
            with t_rw:
                r_t = {"Craft & Structure": selected_attempt['R&W Craft & Structure (%)'], "Info & Ideas": selected_attempt['R&W Info & Ideas (%)'], "Standard English": selected_attempt['R&W Standard English (%)'], "Expression of Ideas": selected_attempt['R&W Expression of Ideas (%)']}
                for t, v in r_t.items(): st.markdown(f"<div class='topic-box'><span>{t}</span><b>{int(v)}%</b></div>", unsafe_allow_html=True)

            st.markdown(f"<div class='insight-box'><b style='color: #0369a1;'>ℹ️ Smart Insight</b><br><span style='font-size: 13px; color: #0c4a6e;'>คะแนนสูงสุดของน้องคือ <b>{int(best_score)}</b> ขาดอีก <b>{target - int(best_score)}</b> คะแนนจะถึงเป้า 1500 ค่ะ</span></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

else:
    st.title("⚙️ aims Admin Control")
    st.dataframe(df, use_container_width=True)
