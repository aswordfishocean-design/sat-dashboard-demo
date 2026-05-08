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

# --- 2. ฐานข้อมูลวิเคราะห์ข้อที่ผิด (Incorrect Questions) จาก PDF จริง ---
# พี่รวบรวมข้อที่ผิดและหัวข้อ (Topics) มาให้เพื่อให้ข้อมูลหายเพี้ยนครับ
detailed_wrong_dict = {
    "Aphiphongphiphut Kaweeyarn": {
        "At 1": {"rw": "Q1, Q4, Q8, Q20 (Craft)", "math": "Q12, Q17, Q21 (Adv. Math/Algebra)"},
        "At 2": {"rw": "Q3, Q10, Q20 (Info & Ideas)", "math": "Q14, Q16, Q18 (Algebra)"},
        "At 3": {"rw": "Q6, Q10, Q22 (Expression)", "math": "Q10, Q19, Q21 (Additional)"},
        "At 4": {"rw": "Q4, Q15, Q27 (Standard English)", "math": "Q1, Q10, Q16 (Problem Solving)"},
        "At 5": {"rw": "Q3, Q9, Q14 (Info & Ideas)", "math": "Q22 (Algebra)"},
        "At 6": {"rw": "Q5, Q12, Q19 (Craft)", "math": "Q14, Q16 (Algebra)"},
        "At 7": {"rw": "Q8, Q16, Q20 (Info & Ideas)", "math": "Q3, Q9, Q13 (Adv. Math)"},
        "At 8": {"rw": "Q3, Q10, Q11 (Standard English)", "math": "Q14, Q20 (Adv. Math)"},
    },
    "Pharin Chantapakul": {
        "At 1": {"rw": "Q4, Q14, Q21 (Craft)", "math": "Q1, Q13, Q22 (Algebra/Add.)"},
        "At 2": {"rw": "Q2, Q12, Q19 (Info & Ideas)", "math": "Q3, Q15, Q21 (Problem Solving)"},
        "At 3": {"rw": "Q1, Q8, Q20 (Expression)", "math": "Q12, Q17, Q22 (Adv. Math)"},
        "At 4": {"rw": "Q4, Q10, Q18 (Craft)", "math": "Q1, Q10, Q21 (Problem Solving)"},
        "At 5": {"rw": "Q3, Q15, Q22 (Standard English)", "math": "Q4, Q7, Q22 (Adv. Math)"},
        "At 6": {"rw": "Q5, Q14, Q19 (Expression)", "math": "Q5, Q9, Q13 (Additional)"},
        "At 7": {"rw": "Q1, Q9, Q21 (Info & Ideas)", "math": "Q10, Q19, Q22 (Problem Solving)"},
        "At 8": {"rw": "Q3, Q12, Q27 (Standard English)", "math": "Q14, Q18, Q21 (Algebra)"},
    }
}

# --- 3. ตั้งค่าหน้าตาแอป & CSS ---
st.set_page_config(page_title="aims SAT Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .target-container { text-align: center; padding: 20px; background: white; border-radius: 25px; border: 2px solid #e0f2fe; margin-bottom: 20px; }
    .target-label { font-size: 20px; color: #64748b; font-weight: 600; }
    .target-score { font-size: 80px; font-weight: 900; color: #0284c7; line-height: 1; }
    .stMetric { background-color: white; padding: 20px; border-radius: 20px; border: 1px solid #e2e8f0; }
    .attempt-card { background-color: white; padding: 25px; border-radius: 20px; border: 1px solid #e2e8f0; }
    .topic-box { background-color: white; padding: 12px 18px; border: 1px solid #e2e8f0; border-radius: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .insight-box { background-color: #f0f9ff; padding: 20px; border-radius: 20px; border: 1px solid #e0f2fe; margin-top: 15px; }
    .error-chip { background-color: #fff1f2; color: #e11d48; border: 1px solid #fecdd3; padding: 6px 12px; border-radius: 10px; font-size: 13px; font-weight: 600; margin-bottom: 8px; display: block; }
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

        # 1. เป้าหมายคะแนนตัวใหญ่ๆ
        st.markdown(f"""
            <div class="target-container">
                <div class="target-label">เป้าหมายคะแนนสูงสุด (Common Target)</div>
                <div class="target-score">{target}</div>
            </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1: st.metric("คะแนนครั้งที่เลือก", int(selected_attempt['Total Score']), f"Attempt {c_idx+1}")
        with c2: st.metric("คะแนนสูงสุด (Best)", int(best_score))
        with c3:
            prog = int((best_score / target) * 100)
            st.metric("Progress", f"{prog}%", f"ขาดอีก {target - int(best_score)}")
            st.progress(prog/100)

        st.divider()

        # --- 5. Layout ---
        left, right = st.columns([1.8, 1.2])

        with left:
            st.subheader("📊 Score Trend")
            fig = go.Figure()
            labels = [f"At {i+1}" for i in range(len(s_data))]
            fig.add_trace(go.Bar(x=labels, y=s_data['Math Score'], name='Math', marker_color='#0284c7'))
            fig.add_trace(go.Bar(x=labels, y=s_data['R&W Score'], name='Reading & Writing', marker_color='rgba(0,0,0,0)', marker_line_color='#0284c7', marker_line_width=2))
            fig.update_layout(barmode='group', xaxis=dict(title="ครั้งที่สอบ"), yaxis=dict(title="คะแนน", range=[200, 800], tickvals=[200, 400, 600, 800]), height=450, plot_bgcolor='rgba(0,0,0,0)')
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
            sc1, sc2 = st.columns(2)
            sc1.metric("Math Score", int(selected_attempt['Math Score']))
            sc2.metric("R&W Score", int(selected_attempt['R&W Score']))
            
            tab_m, tab_r = st.tabs(["Math Topics", "R&W Topics"])
            with tab_m:
                m_t = {"Algebra": 'Math Algebra (%)', "Problem Solving": 'Math Problem Solving (%)', "Advanced Math": 'Math Advanced Math (%)', "Additional Topics": 'Math Additional Topics (%)'}
                for k, v in m_t.items(): st.markdown(f"<div class='topic-box'><span>{k}</span><b>{int(selected_attempt[v])}%</b></div>", unsafe_allow_html=True)
            with tab_r:
                r_t = {"Craft & Structure": 'R&W Craft & Structure (%)', "Info & Ideas": 'R&W Info & Ideas (%)', "Standard English": 'R&W Standard English (%)', "Expression of Ideas": 'R&W Expression of Ideas (%)'}
                for k, v in r_t.items(): st.markdown(f"<div class='topic-box'><span>{k}</span><b>{int(selected_attempt[v])}%</b></div>", unsafe_allow_html=True)

            # --- 2 & 3. Smart Insight & Incorrect Analysis (ข้อมูลจริง) ---
            st.markdown("<div class='insight-box'>", unsafe_allow_html=True)
            st.markdown("<b style='color: #0369a1;'>📖 ข้อแนะนำการเรียนเพิ่มเติม</b>", unsafe_allow_html=True)
            
            # คำนวณหัวข้อที่ควรเรียนเพิ่ม
            all_scores = {**{k: selected_attempt[v] for k, v in m_t.items()}, **{k: selected_attempt[v] for k, v in r_t.items()}}
            weakest = min(all_scores, key=all_scores.get)
            
            st.markdown(f"หัวข้อที่ควรเร่งเสริมคือ **{weakest}** เนื่องจากครั้งนี้ทำได้เพียง **{int(all_scores[weakest])}%** ครับ")
            st.markdown("<hr style='border: 0.5px solid #e0f2fe;'>", unsafe_allow_html=True)
            st.markdown("<b style='color: #0369a1;'>📝 Incorrect Questions Analysis</b>", unsafe_allow_html=True)
            
            # ดึงข้อมูลข้อที่ผิดจริงตาม Attempt ที่กด
            at_key = f"At {c_idx+1}"
            w_info = detailed_wrong_dict.get(student_name, {}).get(at_key, {"math": "N/A", "rw": "N/A"})
            
            st.markdown(f"<span class='error-chip'>Math: {w_info['math']}</span>", unsafe_allow_html=True)
            st.markdown(f"<span class='error-chip'>R&W: {w_info['rw']}</span>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

elif role == "Admin":
    st.title("⚙️ aims Admin Control")
    st.dataframe(df)
