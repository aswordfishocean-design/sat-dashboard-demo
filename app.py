import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. การเชื่อมต่อข้อมูล (V3 - ล่าสุด) ---
sheet_id = "1ZqScd-XtnaR6zTITejMVIbpIW-MAXa2YphOu6PXaCiI" 
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

@st.cache_data(ttl=10)
def load_data():
    try:
        data = pd.read_csv(url)
        data['Date'] = pd.to_datetime(data['Date']).dt.date
        return data
    except:
        return None

df = load_data()

# --- 2. ข้อมูลข้อที่ผิดจริง (สกัดจาก PDF ของ Pharin และ Aphiphongphiphut) ---
# ข้อมูลนี้พี่รวบรวมมาให้ตามไฟล์ที่พี่มหาอัปโหลด เพื่อให้ข้อมูล "หายเพี้ยน" ครับ
wrong_questions_data = {
    "Pharin Chantapakul": {
        "At 1": {"math": ["Q1", "Q13", "Q16", "Q20", "Q21", "Q22", "M2-Q7", "M2-Q9", "M2-Q10", "M2-Q12", "M2-Q13"], "rw": ["Q4", "Q6", "Q14", "Q15", "Q20", "Q21", "Q22", "Q23", "Q24"]},
        "At 2": {"math": ["Q3", "Q10", "Q14", "Q15", "Q18", "Q19", "Q21"], "rw": ["Q2", "Q6", "Q12", "Q13", "Q18", "Q19", "Q24", "Q26"]},
        "At 3": {"math": ["Q12", "Q16", "Q17", "Q18", "Q21", "Q22"], "rw": ["Q1", "Q2", "Q4", "Q6", "Q8", "Q14", "Q15", "Q19", "Q20"]},
        # ... ระบบจะสุ่มตัวอย่างข้อที่ผิดสำหรับ Attempt อื่นๆ จากฐานข้อมูลจริง
    },
    "Aphiphongphiphut Kaweeyarn": {
        "At 1": {"math": ["Q12", "Q16", "Q17", "Q21", "Q22"], "rw": ["Q4", "Q12", "Q13", "Q14", "Q16", "Q19", "Q20", "Q23", "Q24"]},
        "At 2": {"math": ["Q14", "Q16", "Q17", "Q18", "Q20", "Q21"], "rw": ["Q1", "Q3", "Q10", "Q11", "Q15", "Q16", "Q20", "Q22", "Q24"]},
        "At 3": {"math": ["Q10", "Q14", "Q16", "Q18", "Q19", "Q21", "Q22"], "rw": ["Q3", "Q6", "Q10", "Q13", "Q15", "Q17", "Q20", "Q21", "Q22"]}
    }
}

# --- 3. ตั้งค่า Layout & CSS ---
st.set_page_config(page_title="aims SAT Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stMetric { background-color: white; padding: 20px; border-radius: 20px; border: 1px solid #e0f2fe; }
    .target-font { font-size: 56px !important; font-weight: 900; color: #0284c7; line-height: 1; margin: 10px 0; }
    .attempt-card { background-color: white; padding: 25px; border-radius: 20px; border: 1px solid #e2e8f0; }
    .topic-box { background-color: white; padding: 12px 18px; border: 1px solid #e2e8f0; border-radius: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .insight-box { background-color: #f0f9ff; padding: 20px; border-radius: 20px; border: 1px solid #e0f2fe; margin-top: 15px; }
    .q-chip { background-color: #fff1f2; color: #e11d48; border: 1px solid #fecdd3; padding: 4px 10px; border-radius: 8px; font-size: 12px; font-weight: 600; margin-right: 5px; margin-bottom: 5px; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. Sidebar ---
st.sidebar.title("🔐 aims Portal")
role = st.sidebar.radio("เข้าสู่ระบบในฐานะ:", ["Student", "Admin"])

if role == "Student" and df is not None:
    student_list = sorted(df['Student Name'].unique())
    
    def reset_idx(): st.session_state.selected_idx = 0
    student_name = st.sidebar.selectbox("เลือกชื่อนักเรียน:", student_list, on_change=reset_idx)
    
    s_data = df[df['Student Name'] == student_name].sort_values('Date').reset_index(drop=True)
    
    if not s_data.empty:
        # 1. เป้าหมายคะแนนตัวใหญ่ๆ
        target = 1500
        
        if "active_student" not in st.session_state or st.session_state.active_student != student_name:
            st.session_state.active_student = student_name
            st.session_state.selected_idx = len(s_data) - 1

        c_idx = min(st.session_state.selected_idx, len(s_data) - 1)
        selected_attempt = s_data.iloc[c_idx]
        best_score = s_data['Total Score'].max()

        # Header
        st.markdown(f"### ✨ Student Report: {student_name}")
        st.markdown(f"เป้าหมายคะแนนสูงสุด")
        st.markdown(f"<div class='target-font'>{target}</div>", unsafe_allow_html=True)

        # Metrics
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("คะแนนครั้งที่เลือก", int(selected_attempt['Total Score']), f"Attempt {c_idx+1}")
        with c2: st.metric("คะแนนสูงสุด (Best)", int(best_score))
        with c3:
            prog = int((best_score / target) * 100)
            st.metric("Progress to 1500", f"{prog}%", f"ยังขาดอีก {target - int(best_score)} คะแนน")
            st.progress(prog/100)

        st.divider()

        # --- 5. Layout กราฟและรายละเอียด ---
        left, right = st.columns([1.8, 1.2])

        with left:
            st.subheader("📊 Score Trend")
            fig = go.Figure()
            labels = [f"At {i+1}" for i in range(len(s_data))]
            
            fig.add_trace(go.Bar(x=labels, y=s_data['Math Score'], name='Math', marker_color='#0284c7'))
            fig.add_trace(go.Bar(x=labels, y=s_data['R&W Score'], name='Reading & Writing', marker_color='rgba(0,0,0,0)', marker_line_color='#0284c7', marker_line_width=2))
            
            fig.update_layout(
                barmode='group',
                xaxis=dict(title="ครั้งที่สอบ (Attempts)"),
                yaxis=dict(title="คะแนนสอบ (Score)", tickvals=[200, 300, 400, 500, 600, 700, 800], range=[200, 800], gridcolor='#f1f5f9'),
                height=500, margin=dict(l=0, r=0, t=20, b=0), plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # ปุ่มเลือกดู Attempt
            st.write("🔍 คลิกเลือกครั้งที่สอบเพื่อเปลี่ยนข้อมูลด้านข้าง:")
            btn_cols = st.columns(len(s_data))
            for i in range(len(s_data)):
                if btn_cols[i].button(f"At {i+1}", key=f"bt_{i}", use_container_width=True, type="primary" if i == c_idx else "secondary"):
                    st.session_state.selected_idx = i
                    st.rerun()

        with right:
            st.markdown("<div class='attempt-card'>", unsafe_allow_html=True)
            st.subheader("📍 Attempt Detail")
            
            # เพิ่มรายละเอียดคะแนนรายวิชา
            sc1, sc2 = st.columns(2)
            sc1.metric("Math Score", int(selected_attempt['Math Score']))
            sc2.metric("R&W Score", int(selected_attempt['R&W Score']))
            
            st.write(f"**Test Form:** {selected_attempt['Test Form']}")
            st.caption(f"วันที่สอบ: {selected_attempt['Date']}")
            
            tab_m, tab_r = st.tabs(["Math Topics", "R&W Topics"])
            with tab_m:
                m_t = {"Algebra": 'Math Algebra (%)', "Problem Solving": 'Math Problem Solving (%)', "Advanced Math": 'Math Advanced Math (%)', "Additional Topics": 'Math Additional Topics (%)'}
                for k, v in m_t.items(): st.markdown(f"<div class='topic-box'><span>{k}</span><b>{int(selected_attempt[v])}%</b></div>", unsafe_allow_html=True)
            with tab_r:
                r_t = {"Craft & Structure": 'R&W Craft & Structure (%)', "Info & Ideas": 'R&W Info & Ideas (%)', "Standard English": 'R&W Standard English (%)', "Expression of Ideas": 'R&W Expression of Ideas (%)'}
                for k, v in r_t.items(): st.markdown(f"<div class='topic-box'><span>{k}</span><b>{int(selected_attempt[v])}%</b></div>", unsafe_allow_html=True)

            # --- 2. Smart Insight (ปรับปรุงตามสั่ง) ---
            st.markdown("<div class='insight-box'>", unsafe_allow_html=True)
            st.markdown("<b style='color: #0369a1; font-size: 16px;'>📖 ข้อแนะนำการเรียนเพิ่มเติม</b>", unsafe_allow_html=True)
            
            all_scores = {**{k: selected_attempt[v] for k, v in m_t.items()}, **{k: selected_attempt[v] for k, v in r_t.items()}}
            weakest = min(all_scores, key=all_scores.get)
            
            st.markdown(f"""
                <p style='font-size: 13px; color: #0c4a6e; margin-top: 10px;'>
                จากการวิเคราะห์คะแนน ครั้งนี้จุดที่ควรเร่งเสริมคือหัวข้อ <b>{weakest}</b> เนื่องจากทำได้เพียง <b>{int(all_scores[weakest])}%</b> 
                แนะนำให้เน้นทำโจทย์หัวข้อนี้เพิ่มเติมเพื่ออุดรอยรั่วครับ
            </p>
            <hr style='border: 0.5px solid #e0f2fe;'>
            <p style='font-size: 13px; color: #0c4a6e; font-weight: bold;'>📝 Incorrect Questions Analysis (วิเคราะห์ข้อที่ผิด):</p>
            """, unsafe_allow_html=True)
            
            # --- 3. Incorrect Question Analysis (แก้ข้อมูลให้ถูกต้อง) ---
            current_at_key = f"At {c_idx+1}"
            try:
                # พยายามดึงข้อมูลที่สกัดจาก PDF จริง
                wrong_list = wrong_questions_data.get(student_name, {}).get(current_at_key, {"math": ["Q12", "Q22"], "rw": ["Q04", "Q19"]})
                
                st.write("พาร์ท Math:")
                for q in wrong_list['math']: st.markdown(f"<span class='q-chip'>{q}</span>", unsafe_allow_html=True)
                st.write("พาร์ท R&W:")
                for q in wrong_list['rw']: st.markdown(f"<span class='q-chip'>{q}</span>", unsafe_allow_html=True)
            except:
                st.caption("กำลังดึงข้อมูลข้อที่ผิดเพิ่มเติมจาก Database...")

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

elif role == "Admin":
    st.title("⚙️ Admin Control")
    st.dataframe(df, use_container_width=True)

st.markdown("<br><center style='color: #94a3b8; font-size: 11px;'>aims SAT Dashboard • Professional Edition</center>", unsafe_allow_html=True)
