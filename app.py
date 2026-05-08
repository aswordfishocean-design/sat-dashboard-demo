import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. เชื่อมต่อฐานข้อมูล V3 ---
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

# --- 2. ฐานข้อมูลวิเคราะห์ข้อที่ผิด (Incorrect Questions) สกัดจาก PDF จริง ---
# พี่แก้ข้อมูลส่วนนี้ให้ถูกต้องตาม Attempt 1-8 ของน้องทั้ง 2 คนแล้วครับ
incorrect_mapping = {
    "Aphiphongphiphut Kaweeyarn": {
        "At 1": "Math: Q12, Q16, Q17, Q21 (Adv. Math/Add.) | R&W: Q14, Q19, Q20, Q21, Q27 (Ideas/Std. Eng)",
        "At 2": "Math: Q1, Q14, Q16, Q18, Q20 (Algebra) | R&W: Q3, Q10, Q11, Q15, Q16 (Info & Ideas)",
        "At 3": "Math: Q10, Q14, Q16, Q18, Q19 (Algebra/Add.) | R&W: Q3, Q6, Q10, Q13, Q15 (Craft/Ideas)",
        "At 4": "Math: Q1, Q9, Q10, Q13 (Algebra/Problem) | R&W: Q1, Q14, Q19, Q21 (Craft/Std. Eng)",
        "At 5": "Math: Q4, Q15, Q19, Q20 (Algebra/Add.) | R&W: Q3, Q9, Q11, Q14, Q15 (Info & Ideas)",
        "At 6": "Math: Q5, Q8, Q11, Q12, Q14 (Algebra) | R&W: Q1, Q3, Q4, Q7, Q11, Q14 (Craft/Ideas)",
        "At 7": "Math: Q3, Q9, Q13, Q17 (Adv. Math/Algebra) | R&W: Q1, Q3, Q11, Q13, Q15 (Craft/Ideas)",
        "At 8": "Math: Q7, Q14, Q18, Q20 (Adv. Math/Problem) | R&W: Q1, Q3, Q4, Q11, Q15 (Craft/Ideas)"
    },
    "Pharin Chantapakul": {
        "At 1": "Math: Q1, Q7, Q13, Q20, Q22 (Algebra/Add.) | R&W: Q4, Q6, Q13, Q15, Q17 (Craft/Ideas)",
        "At 2": "Math: Q3, Q4, Q10, Q13 (Adv. Math/Problem) | R&W: Q2, Q11, Q13, Q17, Q20 (Craft/Ideas)",
        "At 3": "Math: Q4, Q7, Q10, Q13, Q17 (Algebra) | R&W: Q1, Q3, Q7, Q10, Q14 (Craft/Ideas)",
        "At 4": "Math: Q1, Q10, Q14, Q15 (Problem/Adv. Math) | R&W: Q1, Q4, Q9, Q12, Q16 (Craft/Ideas)",
        "At 5": "Math: Q15, Q16, Q18, Q22 (Algebra) | R&W: Q3, Q5, Q9, Q14, Q17 (Craft/Ideas)",
        "At 6": "Math: Q18, Q20, Q21 (Algebra/Add.) | R&W: Q4, Q9, Q13, Q18, Q20 (Craft/Ideas)",
        "At 7": "Math: Q9, Q11, Q19, Q20 (Algebra/Add.) | R&W: Q1, Q3, Q11, Q13, Q20 (Craft/Std. Eng)",
        "At 8": "Math: Q5, Q14, Q17, Q21 (Adv. Math/Add.) | R&W: Q1, Q4, Q5, Q11, Q16 (Craft/Ideas)"
    }
}

# --- 3. ตั้งค่าหน้าตาแอป & Branding CSS ---
st.set_page_config(page_title="aims SAT Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    /* Branding Box - Right Top */
    .branding-box {
        position: fixed;
        top: 60px;
        right: 40px;
        text-align: right;
        z-index: 1000;
        line-height: 1.2;
    }
    .branding-box img { width: 140px; margin-bottom: 5px; }
    .branding-box p { margin: 0; font-size: 13px; color: #002d56; font-weight: 600; }
    .branding-box a { color: #002d56; text-decoration: none; }

    /* Target Score Styling */
    .target-title { font-size: 18px; color: #64748b; font-weight: 600; margin-bottom: -10px; }
    .target-value { font-size: 100px; font-weight: 900; color: #002d56; line-height: 1; margin: 10px 0; }
    
    .stMetric { background-color: white; padding: 20px; border-radius: 20px; border: 1px solid #e0f2fe; }
    .attempt-card { background-color: white; padding: 25px; border-radius: 20px; border: 1px solid #e2e8f0; }
    .topic-box { background-color: white; padding: 10px 15px; border: 1px solid #f1f5f9; border-radius: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
    .insight-box { background-color: #f0f9ff; padding: 18px; border-radius: 18px; border: 1px solid #e0f2fe; margin-top: 15px; }
    .error-tag { background-color: #fff1f2; color: #e11d48; border: 1px solid #fecdd3; padding: 8px 12px; border-radius: 10px; font-size: 13px; font-weight: 600; margin-top: 10px; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. แสดงผล Branding ---
st.markdown(f"""
    <div class="branding-box">
        <img src="https://aims.co.th/wp-content/uploads/2019/12/Logo-aims.png" alt="aims logo">
        <p>Siam Square: 02-254-9300-2</p>
        <p><a href="https://www.aims.co.th">www.aims.co.th</a></p>
        <p>Line ID: @aims2</p>
    </div>
""", unsafe_allow_html=True)

# --- 5. ระบบ Dashboard ---
st.sidebar.title("🔐 aims Portal")
role = st.sidebar.radio("เข้าสู่ระบบในฐานะ:", ["Student", "Admin"])

if role == "Student" and df is not None:
    student_list = sorted(df['Student Name'].unique())
    def reset_idx(): st.session_state.selected_idx = 0
    student_name = st.sidebar.selectbox("เลือกชื่อนักเรียน:", student_list, on_change=reset_idx)
    
    s_data = df[df['Student Name'] == student_name].sort_values('Date').reset_index(drop=True)
    
    if not s_data.empty:
        target_score = 1500
        if "active_student" not in st.session_state or st.session_state.active_student != student_name:
            st.session_state.active_student = student_name
            st.session_state.selected_idx = len(s_data) - 1

        c_idx = min(st.session_state.selected_idx, len(s_data) - 1)
        selected_attempt = s_data.iloc[c_idx]
        best_total = s_data['Total Score'].max()

        # Header Section
        st.markdown(f"<h2 style='color: #002d56; margin-bottom: 0;'>{student_name}</h2>", unsafe_allow_html=True)
        st.markdown("<p class='target-title'>TARGET SCORE</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='target-value'>{target_score}</p>", unsafe_allow_html=True)

        # KPI Cards
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("คะแนนครั้งที่เลือก", int(selected_attempt['Total Score']), f"At {c_idx+1}")
        with c2: st.metric("คะแนนสูงสุด (Best)", int(best_total))
        with c3:
            prog = int((best_total / target_score) * 100)
            st.metric("Progress", f"{prog}%", f"ขาดอีก {target_score - int(best_total)}")
            st.progress(prog/100)

        st.divider()

        # --- 6. Layout กราฟและรายละเอียด ---
        left, right = st.columns([1.8, 1.2])

        with left:
            st.subheader("📊 Score Trend (At 1 - At 8)")
            fig = go.Figure()
            labels = [f"At {i+1}" for i in range(len(s_data))]
            fig.add_trace(go.Bar(x=labels, y=s_data['Math Score'], name='Math', marker_color='#002d56'))
            fig.add_trace(go.Bar(x=labels, y=s_data['R&W Score'], name='Reading & Writing', marker_color='rgba(0,0,0,0)', marker_line_color='#002d56', marker_line_width=2))
            fig.update_layout(barmode='group', xaxis=dict(title="Attempts"), yaxis=dict(title="Score", range=[200, 800], tickvals=[200, 400, 600, 800]), height=450, plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            
            # ปุ่มกด
            btn_cols = st.columns(len(s_data))
            for i in range(len(s_data)):
                if btn_cols[i].button(f"At {i+1}", key=f"btn_{i}", use_container_width=True, type="primary" if i == c_idx else "secondary"):
                    st.session_state.selected_idx = i
                    st.rerun()

        with right:
            st.markdown("<div class='attempt-card'>", unsafe_allow_html=True)
            st.subheader("📍 Attempt Detail")
            st.markdown(f"🗓️ **วันที่สอบ:** {selected_attempt['Date']}")
            
            # แสดงคะแนน Math และ R&W ชัดๆ
            sc1, sc2 = st.columns(2)
            sc1.metric("Math Score", int(selected_attempt['Math Score']))
            sc2.metric("R&W Score", int(selected_attempt['R&W Score']))
            
            tab_m, tab_r = st.tabs(["Math Topics", "R&W Topics"])
            with tab_m:
                for k, v in {"Algebra": 'Math Algebra (%)', "Problem Solving": 'Math Problem Solving (%)', "Advanced Math": 'Math Advanced Math (%)', "Additional Topics": 'Math Additional Topics (%)'}.items():
                    st.markdown(f"<div class='topic-box'><span>{k}</span><b>{int(selected_attempt[v])}%</b></div>", unsafe_allow_html=True)
            with tab_r:
                for k, v in {"Craft & Structure": 'R&W Craft & Structure (%)', "Info & Ideas": 'R&W Info & Ideas (%)', "Standard English": 'R&W Standard English (%)', "Expression of Ideas": 'R&W Expression of Ideas (%)'}.items():
                    st.markdown(f"<div class='topic-box'><span>{k}</span><b>{int(selected_attempt[v])}%</b></div>", unsafe_allow_html=True)

            # --- 7. Smart Insight & Incorrect Analysis (หายเพี้ยนแล้ว) ---
            st.markdown("<div class='insight-box'>", unsafe_allow_html=True)
            st.markdown("<b style='color: #0369a1;'>📖 ข้อแนะนำการเรียนเพิ่มเติม</b>", unsafe_allow_html=True)
            
            # คำนวณหัวข้อที่เปอร์เซ็นต์น้อยที่สุด
            m_topics = {k: selected_attempt[v] for k, v in {"Algebra": 'Math Algebra (%)', "Problem Solving": 'Math Problem Solving (%)', "Advanced Math": 'Math Advanced Math (%)', "Additional Topics": 'Math Additional Topics (%)'}.items()}
            r_topics = {k: selected_attempt[v] for k, v in {"Craft & Structure": 'R&W Craft & Structure (%)', "Info & Ideas": 'R&W Info & Ideas (%)', "Standard English": 'R&W Standard English (%)', "Expression of Ideas": 'R&W Expression of Ideas (%)'}.items()}
            all_topics = {**m_topics, **r_topics}
            weakest_topic = min(all_topics, key=all_topics.get)
            
            st.markdown(f"ครั้งนี้ควรเร่งเสริมหัวข้อ **{weakest_topic}** เนื่องจากทำได้เพียง **{int(all_topics[weakest_topic])}%** ครับ")
            st.markdown("<hr style='border: 0.5px solid #e0f2fe;'>", unsafe_allow_html=True)
            st.markdown("<b style='color: #0369a1;'>📝 Incorrect Questions Analysis</b>", unsafe_allow_html=True)
            
            # ดึงข้อมูลจาก Mapping ที่เตรียมไว้
            at_key = f"At {c_idx+1}"
            wrong_info = incorrect_mapping.get(student_name, {}).get(at_key, "กำลังประมวลผลข้อมูลข้อที่ผิด...")
            st.markdown(f"<span class='error-tag'>{wrong_info}</span>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

elif role == "Admin":
    st.title("⚙️ aims Admin Control Center")
    st.dataframe(df)
