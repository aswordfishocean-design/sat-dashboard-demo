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

# --- 2. ฐานข้อมูลวิเคราะห์ข้อที่ผิด (Incorrect Questions) ที่ถูกต้อง 100% ---
# สกัดจาก PDF จริงของน้องทั้ง 2 คน (At 1 - At 8)
detailed_incorrect_data = {
    "Aphiphongphiphut Kaweeyarn": {
        "At 1": {"rw": "Q14 (Ideas), Q19 (Std. Eng), Q20 (Std. Eng), Q21 (Std. Eng), Q27 (Expression)", "math": "Q12 (Adv. Math), Q16 (Adv. Math), Q17 (Additional), Q21 (Adv. Math)"},
        "At 2": {"rw": "Q3 (Craft), Q10 (Ideas), Q11 (Ideas), Q15 (Ideas), Q16 (Ideas), Q20 (Std. Eng)", "math": "Q1 (Algebra), Q14 (Algebra), Q16 (Algebra), Q18 (Algebra), Q20 (Algebra)"},
        "At 3": {"rw": "Q3 (Craft), Q6 (Craft), Q10 (Ideas), Q13 (Ideas), Q15 (Std. Eng), Q20 (Std. Eng)", "math": "Q10 (Algebra), Q14 (Algebra), Q16 (Algebra), Q18 (Algebra), Q19 (Additional)"},
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

# --- 3. การตั้งค่าหน้าตาแอป & CSS ---
st.set_page_config(page_title="aims SAT Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    /* Target Score Styling */
    .target-container { text-align: center; margin-bottom: 30px; }
    .target-label { font-size: 20px; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; }
    .target-huge { font-size: 120px; font-weight: 900; color: #002d56; line-height: 1; margin: 10px 0; }
    
    .stMetric { background-color: white; padding: 20px; border-radius: 20px; border: 1px solid #e0f2fe; }
    .attempt-card { background-color: white; padding: 25px; border-radius: 20px; border: 1px solid #e2e8f0; }
    .topic-box { background-color: white; padding: 12px 18px; border: 1px solid #f1f5f9; border-radius: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .insight-box { background-color: #f0f9ff; padding: 25px; border-radius: 20px; border: 1px solid #e0f2fe; margin-top: 20px; }
    .wrong-chip { background-color: #fff1f2; color: #e11d48; border: 1px solid #fecdd3; padding: 10px; border-radius: 12px; font-size: 13px; font-weight: 600; margin-top: 10px; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. Header & Branding Section ---
header_left, header_right = st.columns([2, 1])

with header_right:
    # โลโก้ และ ข้อมูลติดต่อสถาบัน
    st.image("https://aims.co.th/wp-content/uploads/2019/12/Logo-aims.png", width=180)
    st.markdown("""
        <div style='text-align: right; color: #002d56; font-size: 14px; font-weight: bold; line-height: 1.4;'>
            Siam Square: 02-254-9300-2<br>
            <a href='https://www.aims.co.th' style='color: #002d56; text-decoration: none;'>www.aims.co.th</a><br>
            Line ID: @aims2
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
        target = 1500
        if "active_student" not in st.session_state or st.session_state.active_student != student_name:
            st.session_state.active_student = student_name
            st.session_state.selected_idx = len(s_data) - 1

        c_idx = min(st.session_state.selected_idx, len(s_data) - 1)
        selected_attempt = s_data.iloc[c_idx]
        best_score = s_data['Total Score'].max()

        # 1. แสดงชื่อนักเรียน และ Target Score ตัวใหญ่ยักษ์
        st.markdown(f"<h1 style='color: #002d56;'>{student_name}</h1>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="target-container">
                <div class="target-label">Target Score</div>
                <div class="target-huge">{target}</div>
            </div>
        """, unsafe_allow_html=True)

        # Metrics
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("คะแนนครั้งที่เลือก", int(selected_attempt['Total Score']), f"At {c_idx+1}")
        with c2: st.metric("คะแนนสูงสุด (Best)", int(best_score))
        with c3:
            prog = int((best_score / target) * 100)
            st.metric("Progress", f"{prog}%", f"ขาดอีก {target - int(best_score)}")
            st.progress(prog/100)

        st.divider()

        # --- 6. Layout กราฟ (Blue & White) และรายละเอียด ---
        left, right = st.columns([1.8, 1.2])

        with left:
            st.subheader("📊 Score Trend (At 1 - At 8)")
            fig = go.Figure()
            labels = [f"At {i+1}" for i in range(len(s_data))]
            
            # Math Bar (สีฟ้าทึบ aims Blue)
            fig.add_trace(go.Bar(x=labels, y=s_data['Math Score'], name='Math', marker_color='#002d56'))
            # R&W Bar (สีขาวขอบฟ้า)
            fig.add_trace(go.Bar(x=labels, y=s_data['R&W Score'], name='Reading & Writing', 
                                 marker_color='rgba(0,0,0,0)', marker_line_color='#002d56', marker_line_width=3))
            
            fig.update_layout(
                barmode='group',
                xaxis=dict(title="Attempts"),
                yaxis=dict(title="Score", range=[200, 800], tickvals=[200, 300, 400, 500, 600, 700, 800]),
                height=450, margin=dict(l=0, r=0, t=20, b=0), plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # ปุ่มเลือกดู Attempt
            st.write("🔍 เลือกครั้งที่ต้องการเจาะลึกรายละเอียด:")
            btn_cols = st.columns(len(s_data))
            for i in range(len(s_data)):
                if btn_cols[i].button(f"At {i+1}", key=f"btn_{i}", use_container_width=True, type="primary" if i == c_idx else "secondary"):
                    st.session_state.selected_idx = i
                    st.rerun()

        with right:
            st.markdown("<div class='attempt-card'>", unsafe_allow_html=True)
            st.subheader("📍 Attempt Detail")
            # ใส่วันที่สอบที่นี่
            st.markdown(f"🗓️ **วันที่สอบ:** {selected_attempt['Date']}")
            
            sc1, sc2 = st.columns(2)
            sc1.metric("Math Score", int(selected_attempt['Math Score']))
            sc2.metric("R&W Score", int(selected_attempt['R&W Score']))
            
            st.write(f"**Test Form:** {selected_attempt['Test Form']}")
            
            tab_m, tab_r = st.tabs(["Math รายหัวข้อ", "R&W รายหัวข้อ"])
            with tab_m:
                m_t = {"Algebra": 'Math Algebra (%)', "Problem Solving": 'Math Problem Solving (%)', "Advanced Math": 'Math Advanced Math (%)', "Additional Topics": 'Math Additional Topics (%)'}
                for k, v in m_t.items(): st.markdown(f"<div class='topic-box'><span>{k}</span><b>{int(selected_attempt[v])}%</b></div>", unsafe_allow_html=True)
            with tab_r:
                r_t = {"Craft & Structure": 'R&W Craft & Structure (%)', "Info & Ideas": 'R&W Info & Ideas (%)', "Standard English": 'R&W Standard English (%)', "Expression of Ideas": 'R&W Expression of Ideas (%)'}
                for k, v in r_t.items(): st.markdown(f"<div class='topic-box'><span>{k}</span><b>{int(selected_attempt[v])}%</b></div>", unsafe_allow_html=True)

            # --- 7. ข้อเสนอแนะการเรียนเพิ่มเติม (วิเคราะห์ยาวขึ้น) ---
            st.markdown("<div class='insight-box'>", unsafe_allow_html=True)
            st.markdown("<b style='color: #0369a1; font-size: 16px;'>📖 ข้อเสนอแนะการเรียนเพิ่มเติม</b>", unsafe_allow_html=True)
            
            all_scores = {**{k: selected_attempt[v] for k, v in m_t.items()}, **{k: selected_attempt[v] for k, v in r_t.items()}}
            weakest = min(all_scores, key=all_scores.get)
            
            st.markdown(f"""
                <div style='font-size: 14px; color: #0c4a6e; line-height: 1.6; margin-top: 10px;'>
                    จากการวิเคราะห์ในครั้งนี้ จุดที่น้องต้องเร่งเสริมด่วนที่สุดคือหัวข้อ <b>{weakest}</b> เนื่องจากทำคะแนนได้เพียง <b>{int(all_scores[weakest])}%</b> เท่านั้นครับ 
                    พี่แนะนำให้เน้นทำโจทย์ในหัวข้อนี้เพิ่มเติมอย่างน้อยวันละ 20 ข้อ เพื่ออุดรอยรั่วของเนื้อหาและเพิ่มความคุ้นเคยกับลักษณะคำถามครับ <br><br>
                    สำหรับวิชา <b>Math</b> ควรเน้นทบทวนพื้นฐานในบทที่ % ยังไม่ถึง 80% ส่วนวิชา <b>Reading & Writing</b> แนะนำให้ฝึกวิเคราะห์โครงสร้างประโยคในส่วน Standard English ให้แม่นยำขึ้น จะช่วยให้คะแนนพุ่งสู่เป้าหมาย <b>1500</b> ได้แน่นอนครับ สู้ๆ!
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<hr style='border: 0.5px solid #e0f2fe;'>", unsafe_allow_html=True)
            st.markdown("<b style='color: #0369a1;'>📝 Incorrect Questions Analysis</b>", unsafe_allow_html=True)
            
            # แสดงข้อมูลข้อที่ผิดจริงตาม Attempt ที่เลือก
            at_key = f"At {c_idx+1}"
            w_info = detailed_incorrect_data.get(student_name, {}).get(at_key, {"math": "N/A", "rw": "N/A"})
            
            st.markdown(f"<div class='wrong-chip'><b>Math (ผิดข้อ):</b> {w_info['math']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='wrong-chip'><b>R&W (ผิดข้อ):</b> {w_info['rw']}</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

elif role == "Admin":
    st.title("⚙️ aims Admin Control")
    st.dataframe(df, use_container_width=True)

st.markdown("<br><center style='color: #94a3b8; font-size: 11px;'>aims SAT Dashboard • Professional Edition • Data Synced from PDF</center>", unsafe_allow_html=True)
