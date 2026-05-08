import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. การเชื่อมต่อข้อมูล (V3) ---
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

# --- 2. ฐานข้อมูล Incorrect Questions (At 1 - At 8) สกัดจาก PDF จริง ---
# หนูแก้ไขข้อมูลส่วนนี้ให้แม่นยำตามข้อที่ผิดและหัวข้อจริงของน้องๆ แล้วค่ะ
incorrect_mapping = {
    "Aphiphongphiphut Kaweeyarn": {
        "At 1": "Math: Q12 (Adv. Math), Q16 (Adv. Math), Q17 (Additional), Q21 (Adv. Math) | R&W: Q14, Q19, Q20, Q21, Q27 (Ideas/Std. Eng)",
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

# --- 3. การตั้งค่าหน้าตาแอป & CSS ---
st.set_page_config(page_title="aims SAT Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    /* Branding Header - Top Right */
    .branding-box {
        position: fixed;
        top: 60px;
        right: 40px;
        text-align: right;
        z-index: 1000;
        line-height: 1.4;
    }
    .branding-box img { width: 150px; margin-bottom: 5px; }
    .branding-box p { margin: 0; font-size: 14px; color: #002d56; font-weight: bold; }
    .branding-box a { color: #002d56; text-decoration: none; }

    /* Target Score Section */
    .target-container { text-align: center; margin-top: 20px; }
    .target-label { font-size: 22px; color: #64748b; font-weight: 700; letter-spacing: 2px; }
    .target-huge { font-size: 150px; font-weight: 900; color: #002d56; line-height: 1; margin: 5px 0; }
    
    .stMetric { background-color: white; padding: 20px; border-radius: 20px; border: 1px solid #e0f2fe; }
    .attempt-card { background-color: white; padding: 25px; border-radius: 20px; border: 1px solid #e2e8f0; }
    .topic-box { background-color: white; padding: 12px 18px; border: 1px solid #f1f5f9; border-radius: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .insight-box { background-color: #f0f9ff; padding: 25px; border-radius: 20px; border: 1px solid #e0f2fe; margin-top: 20px; }
    .error-chip { background-color: #fff1f2; color: #e11d48; border: 1px solid #fecdd3; padding: 10px 15px; border-radius: 12px; font-size: 14px; font-weight: 600; margin-top: 10px; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. แสดง Branding มุมขวาบน ---
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
        best_of_all = s_data['Total Score'].max()

        # แสดงชื่อนักเรียนและ Target Score ใหญ่ยักษ์
        st.markdown(f"<h1 style='color: #002d56; margin-bottom: -10px;'>{student_name}</h1>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="target-container">
                <div class="target-label">TARGET SCORE</div>
                <div class="target-huge">{target_score}</div>
            </div>
        """, unsafe_allow_html=True)

        # Metrics
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("คะแนนครั้งที่เลือก", int(selected_attempt['Total Score']), f"At {c_idx+1}")
        with c2: st.metric("คะแนนสูงสุด (Best)", int(best_of_all))
        with c3:
            prog = int((best_of_all / target_score) * 100)
            st.metric("Progress", f"{prog}%", f"ขาดอีก {target_score - int(best_of_all)} คะแนน")
            st.progress(prog/100)

        st.divider()

        # --- 6. Layout กราฟ Blue & White และรายละเอียด ---
        left, right = st.columns([1.8, 1.2])

        with left:
            st.subheader("📊 Score Trend (At 1 - At 8)")
            fig = go.Figure()
            labels = [f"At {i+1}" for i in range(len(s_data))]
            
            # Math: สีฟ้าทึบ (aims Blue)
            fig.add_trace(go.Bar(x=labels, y=s_data['Math Score'], name='Math', marker_color='#002d56'))
            # R&W: สีขาวขอบฟ้า
            fig.add_trace(go.Bar(x=labels, y=s_data['R&W Score'], name='Reading & Writing', 
                                 marker_color='rgba(0,0,0,0)', marker_line_color='#002d56', marker_line_width=3))
            
            fig.update_layout(
                barmode='group',
                xaxis=dict(title="Attempts"),
                yaxis=dict(title="Score", range=[200, 800], tickvals=[200, 300, 400, 500, 600, 700, 800]),
                height=500, margin=dict(l=0, r=0, t=20, b=0), plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.write("🔍 เลือกครั้งที่ต้องการเจาะลึกรายละเอียด:")
            btn_cols = st.columns(len(s_data))
            for i in range(len(s_data)):
                if btn_cols[i].button(f"At {i+1}", key=f"btn_{i}", use_container_width=True, type="primary" if i == c_idx else "secondary"):
                    st.session_state.selected_idx = i
                    st.rerun()

        with right:
            st.markdown("<div class='attempt-card'>", unsafe_allow_html=True)
            st.subheader("📍 Attempt Detail")
            # แสดงวันที่สอบ
            st.markdown(f"🗓️ **วันที่สอบ:** {selected_attempt['Date']}")
            
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

            # --- 7. ข้อเสนอแนะการเรียนเพิ่มเติม (วิเคราะห์เจาะลึก) ---
            st.markdown("<div class='insight-box'>", unsafe_allow_html=True)
            st.markdown("<b style='color: #0369a1; font-size: 18px;'>📖 ข้อแนะนำการเรียนเพิ่มเติม</b>", unsafe_allow_html=True)
            
            all_topics = {**{k: selected_attempt[v] for k, v in m_t.items()}, **{k: selected_attempt[v] for k, v in r_t.items()}}
            weak_t = min(all_topics, key=all_topics.get)
            
            st.markdown(f"""
                <div style='font-size: 14px; color: #0c4a6e; line-height: 1.6; margin-top: 10px;'>
                    หนูวิเคราะห์แล้วนะคะ ครั้งนี้น้องทำคะแนนในหัวข้อ <b>{weak_t}</b> ได้น้อยที่สุดเพียง <b>{int(all_topics[weak_t])}%</b> เท่านั้นค่ะ <br><br>
                    หนูแนะนำว่าควรให้เวลาทำโจทย์หัวข้อนี้เพิ่มขึ้นเป็นพิเศษเพื่ออุดรอยรั่วค่ะ ในส่วนของ <b>Math</b> ถ้าน้องยังไม่แม่นบทไหนควรกลับไปทบทวนพื้นฐานก่อนทำโจทย์ใหม่นะคะ และพยายามรักษาระดับคะแนนในส่วนที่เก่งอยู่แล้วให้คงที่ค่ะ เพื่อให้คะแนนพุ่งสู่เป้าหมาย <b>1500</b> ได้แน่นอนค่ะ สู้ๆ นะคะ!
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<hr style='border: 0.5px solid #e0f2fe;'>", unsafe_allow_html=True)
            st.markdown("<b style='color: #0369a1;'>📝 Incorrect Questions Analysis</b>", unsafe_allow_html=True)
            
            # ดึงข้อมูลจาก Mapping At 1-8 ที่หายเพี้ยนแล้วค่ะ
            at_key = f"At {c_idx+1}"
            incorrect_info = detailed_incorrect_mapping.get(student_name, {}).get(at_key, "ข้อมูลกำลังปรับปรุงตามฐานข้อมูล PDF ค่ะ")
            st.markdown(f"<div class='error-chip'>{incorrect_info}</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

elif role == "Admin":
    st.title("⚙️ aims Admin Control")
    st.dataframe(df, use_container_width=True)

st.markdown("<br><center style='color: #94a3b8; font-size: 11px;'>aims SAT Dashboard • Professional Edition • Data Synced from PDF</center>", unsafe_allow_html=True)
