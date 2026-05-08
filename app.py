import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# --- 1. การเชื่อมต่อข้อมูล ---
sheet_id = "1ZqScd-XtnaR6zTITejMVIbpIW-MAXa2YphOu6PXaCiI" 
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

@st.cache_data(ttl=10)
def load_data():
    try:
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip() 
        data['Date'] = pd.to_datetime(data['Date']).dt.date
        return data
    except Exception as e:
        st.error(f"หนูเชื่อมต่อข้อมูลไม่ได้ค่ะ: {e}")
        return None

df = load_data()

# --- 2. ฐานข้อมูล Incorrect Questions จริง (At 1 - At 8) สกัดจาก PDF ---
incorrect_mapping = {
    "Aphiphongphiphut Kaweeyarn": {
        "At 1": "Math: Q12, Q16, Q17, Q21 (Advanced Math/Additional) | R&W: Q14, Q19, Q20, Q21, Q27 (Ideas/Std. Eng)",
        "At 2": "Math: Q1, Q6, Q14, Q16, Q17, Q18, Q20 (Algebra) | R&W: Q3, Q10, Q11, Q15, Q16 (Ideas)",
        "At 3": "Math: Q4, Q15, Q19, Q20 (Algebra/Additional) | R&W: Q3, Q9, Q11, Q14, Q15 (Ideas)",
        "At 4": "Math: Q1, Q10, Q13, Q14 (Algebra/Problem Solving) | R&W: Q1, Q3, Q4, Q7, Q11, Q14 (Craft)",
        "At 5": "Math: Q1, Q9, Q10, Q13 (Algebra/Problem Solving) | R&W: Q1, Q14, Q19, Q21 (Std. Eng)",
        "At 6": "Math: Q14, Q18, Q20 (Adv. Math) | R&W: Q1, Q3, Q4, Q11, Q15 (Craft)",
        "At 7": "Math: Q3, Q9, Q13, Q17 (Adv. Math/Algebra) | R&W: Q1, Q3, Q11, Q13, Q15 (Ideas)",
        "At 8": "Math: Q7, Q14, Q18, Q20 (Adv. Math/Problem Solving) | R&W: Q1, Q3, Q4, Q11, Q15 (Craft/Ideas)"
    },
    "Pharin Chantapakul": {
        "At 1": "Math: Q1, Q7, Q13, Q20, Q22 (Algebra/Additional) | R&W: Q4, Q6, Q13, Q15, Q17 (Ideas)",
        "At 2": "Math: Q3, Q4, Q10, Q13 (Advanced Math/Problem Solving) | R&W: Q2, Q11, Q13, Q17, Q20 (Std. Eng)",
        "At 3": "Math: Q4, Q7, Q10, Q13, Q17 (Algebra) | R&W: Q1, Q3, Q7, Q10, Q14 (Craft)",
        "At 4": "Math: Q1, Q10, Q14, Q15 (Problem Solving/Adv. Math) | R&W: Q1, Q4, Q9, Q12, Q16 (Ideas)",
        "At 5": "Math: Q15, Q16, Q18, Q22 (Algebra) | R&W: Q3, Q5, Q9, Q14, Q17 (Craft)",
        "At 6": "Math: Q18, Q20, Q21 (Algebra/Additional) | R&W: Q4, Q9, Q13, Q18, Q20 (Std. Eng)",
        "At 7": "Math: Q9, Q11, Q19, Q20 (Algebra/Additional) | R&W: Q1, Q3, Q11, Q13, Q20 (Std. Eng)",
        "At 8": "Math: Q5, Q14, Q17, Q21 (Adv. Math/Additional) | R&W: Q1, Q4, Q5, Q11, Q16 (Ideas)"
    }
}

# --- 3. การตั้งค่าหน้าตาแอป & CSS (Luxury Theme) ---
st.set_page_config(page_title="aims SAT Premium Report", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;900&display=swap');
    
    .main { background-color: #fcfdfe; }
    
    /* Center Header Branding */
    .header-branding {
        text-align: center;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 30px;
        margin-bottom: 40px;
    }
    .header-branding p {
        margin: 0;
        font-size: 16px;
        color: #002d56;
        font-weight: 600;
        line-height: 1.6;
    }
    
    /* Target Score Styling */
    .target-container { text-align: center; margin: 20px 0; }
    .target-label { font-size: 26px; color: #64748b; font-weight: 600; letter-spacing: 5px; font-family: 'Poppins'; }
    .target-huge { font-size: 150px; font-weight: 900; color: #002d56; line-height: 1; margin: 0; font-family: 'Poppins'; }
    
    .stMetric { background-color: white; padding: 20px; border-radius: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    .attempt-card { background-color: white; padding: 30px; border-radius: 25px; border: 1px solid #f1f5f9; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05); }
    .topic-box { background-color: #ffffff; padding: 14px 20px; border-radius: 16px; border: 1px solid #f1f5f9; margin-bottom: 12px; display: flex; justify-content: space-between; }
    .insight-card { background-color: #f0f9ff; padding: 30px; border-radius: 25px; border: 1px solid #e0f2fe; margin-top: 25px; }
    .error-tag { background-color: #fff1f2; color: #e11d48; border: 1px solid #fecdd3; padding: 12px 18px; border-radius: 14px; font-size: 14px; font-weight: 600; line-height: 1.6; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. แสดงผล Header Branding (Centered Letterhead) ---
st.markdown("<div class='header-branding'>", unsafe_allow_html=True)
# ตรวจสอบไฟล์โลโก้
logo_filename = "aims_logo_2014_01_crop_blue_200x50px.png"
if os.path.exists(logo_filename):
    st.image(logo_filename, width=280)
else:
    st.image("https://aims.co.th/wp-content/uploads/2019/12/Logo-aims.png", width=280)

st.markdown("""
    <p>Siam Square: 02-254-9300-2</p>
    <p><a href='https://www.aims.co.th' style='color: #002d56;'>www.aims.co.th</a> | Line ID: @aims2</p>
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
        target_val = 1500
        if "active_student" not in st.session_state or st.session_state.active_student != student_name:
            st.session_state.active_student = student_name
            st.session_state.selected_idx = len(s_data) - 1

        c_idx = min(st.session_state.selected_idx, len(s_data) - 1)
        selected_attempt = s_data.iloc[c_idx]
        best_score = s_data['Total Score'].max()

        # ส่วนเป้าหมายหลัก
        st.markdown(f"""
            <div class="target-container">
                <div style="font-size: 32px; font-weight: 600; color: #002d56; margin-bottom: 10px;">{student_name}</div>
                <div class="target-label">TARGET SCORE</div>
                <div class="target-huge">{target_val}</div>
            </div>
        """, unsafe_allow_html=True)

        # KPI Metrics
        m1, m2, m3 = st.columns(3)
        with m1: st.metric("Current Attempt Score", int(selected_attempt['Total Score']), f"At {c_idx+1}")
        with m2: st.metric("Personal Best Score", int(best_score))
        with m3:
            prog = int((best_score / target_val) * 100)
            st.metric("Progress to Goal", f"{prog}%", f"Gap: {target_val - int(best_score)}")
            st.progress(prog/100)

        st.divider()

        # --- 6. กราฟพรีเมียม (Blue & Hollow White) ---
        left, right = st.columns([1.7, 1.3])

        with left:
            st.subheader("📊 Performance Trend (At 1 - At 8)")
            fig = go.Figure()
            labels = [f"At {i+1}" for i in range(len(s_data))]
            
            # Math: สีฟ้าเข้มพรีเมียม
            fig.add_trace(go.Bar(
                x=labels, y=s_data['Math Score'], name='Math', 
                marker=dict(color='#002d56', line=dict(width=0))
            ))
            # R&W: แท่งโปร่งขอบน้ำเงิน (Hollow)
            fig.add_trace(go.Bar(
                x=labels, y=s_data['R&W Score'], name='Reading & Writing', 
                marker=dict(
                    color='rgba(255, 255, 255, 0)', 
                    line=dict(color='#002d56', width=3) 
                )
            ))
            
            fig.update_layout(
                barmode='group',
                xaxis=dict(title="Attempts", showgrid=False),
                yaxis=dict(title="Score", range=[200, 800], tickvals=[200, 400, 600, 800], gridcolor='#f1f5f9'),
                height=500, plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True, theme=None)
            
            # Selector Buttons
            st.write("🔍 เจาะลึกข้อมูลครั้งที่สอบ:")
            btn_cols = st.columns(len(s_data))
            for i in range(len(s_data)):
                if btn_cols[i].button(f"At {i+1}", key=f"btn_{i}", use_container_width=True, type="primary" if i == c_idx else "secondary"):
                    st.session_state.selected_idx = i
                    st.rerun()

        with right:
            st.markdown("<div class='attempt-card'>", unsafe_allow_html=True)
            st.subheader("📍 Attempt Details")
            st.markdown(f"🗓️ **Date Taken:** {selected_attempt['Date']} | **Form:** {selected_attempt['Test Form']}")
            
            sc1, sc2 = st.columns(2)
            sc1.metric("Math Score", int(selected_attempt['Math Score']))
            sc2.metric("R&W Score", int(selected_attempt['R&W Score']))
            
            t_math, t_rw = st.tabs(["Math Topic Mastery", "R&W Topic Mastery"])
            with t_math:
                for k, v in {"Algebra": 'Math Algebra (%)', "Problem Solving": 'Math Problem Solving (%)', "Advanced Math": 'Math Advanced Math (%)', "Additional Topics": 'Math Additional Topics (%)'}.items():
                    if v in selected_attempt:
                        st.markdown(f"<div class='topic-box'><span>{k}</span><b>{int(selected_attempt[v])}%</b></div>", unsafe_allow_html=True)
            with t_rw:
                for k, v in {"Craft & Structure": 'R&W Craft & Structure (%)', "Info & Ideas": 'R&W Info & Ideas (%)', "Standard English": 'R&W Standard English (%)', "Expression of Ideas": 'R&W Expression of Ideas (%)'}.items():
                    if v in selected_attempt:
                        st.markdown(f"<div class='topic-box'><span>{k}</span><b>{int(selected_attempt[v])}%</b></div>", unsafe_allow_html=True)

            # --- 7. Smart Insight Card ---
            st.markdown("<div class='insight-card'>", unsafe_allow_html=True)
            st.markdown("<b style='color: #002d56; font-size: 19px;'>📝 Insight & Advice</b>", unsafe_allow_html=True)
            
            all_t = {}
            for k, v in {**{"Algebra": 'Math Algebra (%)', "Problem Solving": 'Math Problem Solving (%)', "Advanced Math": 'Math Advanced Math (%)', "Additional Topics": 'Math Additional Topics (%)'}, **{"Craft & Structure": 'R&W Craft & Structure (%)', "Info & Ideas": 'R&W Info & Ideas (%)', "Standard English": 'R&W Standard English (%)', "Expression of Ideas": 'R&W Expression of Ideas (%)'}}.items():
                if v in selected_attempt: all_t[k] = selected_attempt[v]
            
            if all_t:
                weak = min(all_t, key=all_t.get)
                st.markdown(f"""
                    <div style='font-size: 15px; color: #1e293b; line-height: 1.7; margin: 15px 0;'>
                        หนูวิเคราะห์แล้วนะคะ จุดที่ต้องเร่งเสริมเพื่อให้ถึง 1500 คือหัวข้อ <b>{weak}</b> ค่ะ 
                        ซึ่งได้เพียง <b>{int(all_t[weak])}%</b> ในรอบนี้ หนูแนะนำให้พี่เน้นให้น้องทำโจทย์หัวข้อนี้เพิ่มขึ้น 
                        พร้อมทั้งเก็บความแม่นยำในส่วนที่ทำได้ดีอยู่แล้วนะคะ หนูเป็นกำลังใจให้ค่ะ!
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<b style='color: #002d56;'>Incorrect Questions Analysis:</b>", unsafe_allow_html=True)
            at_key = f"At {c_idx+1}"
            inc_info = incorrect_mapping.get(student_name, {}).get(at_key, "หนูกำลังอัปเดตข้อมูล PDF ให้อยู่นะคะ")
            st.markdown(f"<div class='error-tag'>{inc_info}</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

elif role == "Admin":
    st.title("⚙️ Admin Console")
    st.dataframe(df, use_container_width=True)

st.markdown("<br><center style='color: #94a3b8; font-size: 11px;'>aims SAT Professional Dashboard • Data Insights powered by aims school</center>", unsafe_allow_html=True)
