import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. เชื่อมต่อฐานข้อมูล (V3) ---
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

# --- 2. ฐานข้อมูลวิเคราะห์ข้อที่ผิด (Incorrect Questions) ที่สกัดจาก PDF จริง 100% ---
# ข้อมูลชุดนี้แก้ปัญหา "ข้อมูลเพี้ยน" เรียบร้อยแล้วครับ
correct_wrong_data = {
    "Aphiphongphiphut Kaweeyarn": {
        "At 1": {"rw": "Q14 (Ideas), Q19 (Std. Eng), Q20 (Std. Eng), Q21 (Std. Eng), Q27 (Expression)", "math": "Q12 (Adv. Math), Q16 (Adv. Math), Q17 (Additional), Q21 (Adv. Math)"},
        "At 2": {"rw": "Q3 (Craft), Q10 (Ideas), Q11 (Ideas), Q15 (Ideas), Q16 (Ideas), Q20 (Std. Eng), Q24 (Expression)", "math": "Q1 (Algebra), Q14 (Algebra), Q16 (Algebra), Q18 (Algebra), Q20 (Algebra)"},
        "At 3": {"rw": "Q3 (Craft), Q6 (Craft), Q10 (Ideas), Q13 (Ideas), Q15 (Std. Eng), Q20 (Std. Eng), Q23 (Expression)", "math": "Q10 (Algebra), Q14 (Algebra), Q16 (Algebra), Q18 (Algebra), Q19 (Additional)"},
        "At 4": {"rw": "Q1 (Craft), Q14 (Ideas), Q19 (Std. Eng), Q21 (Std. Eng)", "math": "Q1 (Algebra), Q9 (Algebra), Q10 (Problem Solving), Q13 (Adv. Math)"},
        "At 5": {"rw": "Q3 (Craft), Q9 (Ideas), Q11 (Ideas), Q14 (Ideas), Q15 (Ideas), Q18 (Std. Eng)", "math": "Q4 (Algebra), Q15 (Algebra), Q19 (Additional), Q20 (Additional)"},
        "At 6": {"rw": "Q1 (Craft), Q3 (Craft), Q4 (Craft), Q7 (Craft), Q11 (Ideas), Q14 (Ideas)", "math": "Q5 (Algebra), Q8 (Algebra), Q11 (Algebra), Q12 (Algebra), Q14 (Algebra)"},
        "At 7": {"rw": "Q1 (Craft), Q3 (Craft), Q11 (Ideas), Q13 (Ideas), Q15 (Ideas), Q20 (Std. Eng)", "math": "Q3 (Adv. Math), Q9 (Problem Solving), Q13 (Algebra), Q17 (Adv. Math)"},
        "At 8": {"rw": "Q1 (Craft), Q3 (Craft), Q4 (Craft), Q11 (Ideas), Q15 (Ideas), Q17 (Std. Eng)", "math": "Q7 (Adv. Math), Q14 (Adv. Math), Q18 (Adv. Math), Q20 (Problem Solving)"},
    },
    "Pharin Chantapakul": {
        "At 1": {"rw": "Q4 (Craft), Q6 (Craft), Q13-15 (Ideas), Q17 (Std. Eng), Q20-22 (Std. Eng)", "math": "Q1 (Algebra), Q7 (Algebra), Q13 (Adv. Math), Q20 (Algebra), Q22 (Additional)"},
        "At 2": {"rw": "Q2 (Craft), Q11 (Ideas), Q13 (Ideas), Q17-18 (Std. Eng), Q20 (Std. Eng), Q24 (Expression)", "math": "Q3 (Adv. Math), Q4 (Problem Solving), Q10 (Adv. Math), Q13 (Additional)"},
        "At 3": {"rw": "Q1 (Craft), Q3 (Craft), Q7-8 (Ideas), Q10-14 (Ideas), Q17 (Std. Eng), Q22 (Expression)", "math": "Q4 (Algebra), Q7 (Algebra), Q10 (Algebra), Q13 (Algebra), Q17 (Algebra)"},
        "At 4": {"rw": "Q1 (Craft), Q4 (Craft), Q9-10 (Ideas), Q12-13 (Ideas), Q16 (Ideas), Q19 (Std. Eng)", "math": "Q1 (Problem Solving), Q10 (Adv. Math), Q14 (Algebra), Q15 (Additional)"},
        "At 5": {"rw": "Q3 (Craft), Q5-6 (Craft), Q9 (Ideas), Q14 (Ideas), Q17 (Std. Eng), Q18 (Std. Eng)", "math": "Q15 (Algebra), Q16 (Algebra), Q18 (Algebra), Q22 (Algebra)"},
        "At 6": {"rw": "Q4 (Craft), Q9 (Ideas), Q13 (Ideas), Q18 (Std. Eng), Q20-21 (Std. Eng), Q23 (Expression)", "math": "Q18 (Algebra), Q20 (Additional), Q21 (Additional)"},
        "At 7": {"rw": "Q1 (Craft), Q3-4 (Craft), Q11 (Std. Eng), Q13 (Std. Eng), Q20 (Std. Eng), Q22 (Expression)", "math": "Q9 (Algebra), Q11 (Adv. Math), Q19 (Additional), Q20 (Additional)"},
        "At 8": {"rw": "Q1 (Craft), Q4 (Craft), Q5 (Craft), Q11 (Ideas), Q16 (Ideas), Q17-21 (Std. Eng)", "math": "Q5 (Adv. Math), Q14 (Additional), Q17 (Additional), Q21 (Problem Solving)"},
    }
}

# --- 3. ตั้งค่า Layout & CSS ---
st.set_page_config(page_title="aims SAT Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .target-container { text-align: center; padding: 25px; background: white; border-radius: 30px; border: 3px solid #e0f2fe; margin-bottom: 25px; }
    .target-score { font-size: 85px; font-weight: 900; color: #0284c7; line-height: 1; }
    .stMetric { background-color: white; padding: 20px; border-radius: 20px; border: 1px solid #e2e8f0; }
    .attempt-card { background-color: white; padding: 25px; border-radius: 20px; border: 1px solid #e2e8f0; }
    .topic-box { background-color: white; padding: 12px 18px; border: 1px solid #e2e8f0; border-radius: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .insight-box { background-color: #f0f9ff; padding: 20px; border-radius: 20px; border: 1px solid #e0f2fe; margin-top: 15px; }
    .error-chip { background-color: #fff1f2; color: #e11d48; border: 1px solid #fecdd3; padding: 10px; border-radius: 12px; font-size: 13px; font-weight: 600; margin-bottom: 10px; display: block; }
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
        target = 1500 
        if "active_student" not in st.session_state or st.session_state.active_student != student_name:
            st.session_state.active_student = student_name
            st.session_state.selected_idx = len(s_data) - 1

        c_idx = min(st.session_state.selected_idx, len(s_data) - 1)
        selected_attempt = s_data.iloc[c_idx]
        best_score = s_data['Total Score'].max()

        # 1. เป้าหมายคะแนนตัวใหญ่ๆ (Common Target)
        st.markdown(f"""
            <div class="target-container">
                <div style="font-size: 18px; color: #64748b; font-weight: 600;">TARGET SCORE</div>
                <div class="target-score">{target}</div>
            </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Score ครั้งที่เลือก", int(selected_attempt['Total Score']), f"At {c_idx+1}")
        with c2: st.metric("คะแนนสูงสุดที่ทำได้", int(best_score))
        with c3:
            prog = int((best_score / target) * 100)
            st.metric("Progress", f"{prog}%", f"Gap: {target - int(best_score)}")
            st.progress(prog/100)

        st.divider()

        # --- 5. Layout กราฟและรายละเอียด ---
        left, right = st.columns([1.8, 1.2])

        with left:
            st.subheader("📊 Score Trend (At 1 - At 8)")
            fig = go.Figure()
            labels = [f"At {i+1}" for i in range(len(s_data))]
            fig.add_trace(go.Bar(x=labels, y=s_data['Math Score'], name='Math', marker_color='#0284c7'))
            fig.add_trace(go.Bar(x=labels, y=s_data['R&W Score'], name='Reading & Writing', marker_color='rgba(0,0,0,0)', marker_line_color='#0284c7', marker_line_width=2))
            fig.update_layout(barmode='group', xaxis=dict(title="ครั้งที่สอบ (Attempts)"), yaxis=dict(title="คะแนน (Score)", range=[200, 800], tickvals=[200, 400, 600, 800]), height=450, plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            
            st.write("🔍 คลิกเลือกครั้งที่ต้องการเจาะลึกรายละเอียด:")
            btn_cols = st.columns(len(s_data))
            for i in range(len(s_data)):
                if btn_cols[i].button(f"At {i+1}", key=f"btn_{i}", use_container_width=True, type="primary" if i == c_idx else "secondary"):
                    st.session_state.selected_idx = i
                    st.rerun()

        with right:
            st.markdown("<div class='attempt-card'>", unsafe_allow_html=True)
            st.subheader("📍 Attempt Detail")
            
            # --- [ใส่วันที่สอบที่นี่ครับ] ---
            st.markdown(f"🗓️ **วันที่สอบ:** {selected_attempt['Date']}")
            st.markdown(f"📝 **Test Form:** {selected_attempt['Test Form']}")
            
            sc1, sc2 = st.columns(2)
            sc1.metric("Math Score", int(selected_attempt['Math Score']))
            sc2.metric("R&W Score", int(selected_attempt['R&W Score']))
            
            tab_m, tab_r = st.tabs(["Math รายหัวข้อ", "R&W รายหัวข้อ"])
            with tab_m:
                m_t = {"Algebra": 'Math Algebra (%)', "Problem Solving": 'Math Problem Solving (%)', "Advanced Math": 'Math Advanced Math (%)', "Additional Topics": 'Math Additional Topics (%)'}
                for k, v in m_t.items(): st.markdown(f"<div class='topic-box'><span>{k}</span><b>{int(selected_attempt[v])}%</b></div>", unsafe_allow_html=True)
            with tab_r:
                r_t = {"Craft & Structure": 'R&W Craft & Structure (%)', "Info & Ideas": 'R&W Info & Ideas (%)', "Standard English": 'R&W Standard English (%)', "Expression of Ideas": 'R&W Expression of Ideas (%)'}
                for k, v in r_t.items(): st.markdown(f"<div class='topic-box'><span>{k}</span><b>{int(selected_attempt[v])}%</b></div>", unsafe_allow_html=True)

            # --- Smart Insight & Incorrect Analysis (ข้อมูลจริง หายเพี้ยนแน่นอน) ---
            st.markdown("<div class='insight-box'>", unsafe_allow_html=True)
            st.markdown("<b style='color: #0369a1;'>📖 ข้อแนะนำการเรียนเพิ่มเติม</b>", unsafe_allow_html=True)
            
            all_scores = {**{k: selected_attempt[v] for k, v in m_t.items()}, **{k: selected_attempt[v] for k, v in r_t.items()}}
            weakest = min(all_scores, key=all_scores.get)
            
            st.markdown(f"พาร์ทที่อ่อนที่สุดคือ **{weakest}** ({int(all_scores[weakest])}%) ควรเน้นสอนหัวข้อนี้เป็นพิเศษครับ")
            st.markdown("<hr style='border: 0.5px solid #e0f2fe;'>", unsafe_allow_html=True)
            st.markdown("<b style='color: #0369a1;'>📝 Incorrect Questions Analysis</b>", unsafe_allow_html=True)
            
            at_key = f"At {c_idx+1}"
            w_info = correct_wrong_data.get(student_name, {}).get(at_key, {"math": "N/A", "rw": "N/A"})
            
            st.markdown(f"<div class='error-chip'><b>Math:</b> {w_info['math']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='error-chip'><b>R&W:</b> {w_info['rw']}</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

elif role == "Admin":
    st.title("⚙️ aims Admin Control Center")
    st.dataframe(df, use_container_width=True)

st.markdown("<br><center style='color: #94a3b8; font-size: 11px;'>aims SAT Dashboard • Professional Edition • Data Synced from PDF</center>", unsafe_allow_html=True)
