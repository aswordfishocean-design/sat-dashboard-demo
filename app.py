import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import base64

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

# --- 2. ฐานข้อมูล Incorrect Questions จริง (At 1 - At 8) ---
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

# --- 3. การตั้งค่าหน้าตาแอป & CSS ---
st.set_page_config(page_title="aims SAT Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #fcfdfe; }
    
    /* Target Score & Student Name Section */
    .student-name-title { text-align: center; color: #002d56; font-size: 50px; font-weight: 900; margin-top: 20px; margin-bottom: 5px; }
    .target-container { text-align: center; margin-top: 0px; margin-bottom: 40px; }
    .target-label { font-size: 24px; color: #64748b; font-weight: 700; letter-spacing: 5px; }
    .target-huge { font-size: 150px; font-weight: 900; color: #002d56; line-height: 1; margin: 0; }
    
    .stMetric { background-color: white; padding: 20px; border-radius: 20px; border: 1px solid #e2e8f0; }
    .attempt-card { background-color: white; padding: 30px; border-radius: 25px; border: 1px solid #f1f5f9; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05); }
    .topic-box { background-color: #ffffff; padding: 12px 18px; border-radius: 15px; border: 1px solid #f1f5f9; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .insight-box { background-color: #f0f9ff; padding: 25px; border-radius: 20px; border: 1px solid #e0f2fe; margin-top: 20px; }
    .error-chip { background-color: #fff1f2; color: #e11d48; border: 1px solid #fecdd3; padding: 12px 15px; border-radius: 12px; font-size: 14px; font-weight: 600; margin-top: 10px; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ระบบ Sidebar ---
st.sidebar.title("🔐 aims Portal")
role = st.sidebar.radio("เข้าสู่ระบบในฐานะ:", ["Student", "Admin"])

if role == "Student" and df is not None:
    # ---------------------------------------------------------
    # LAYOUT แถวบนสุด: ซ้าย=เลือกนักเรียน | ขวา=โลโก้ชิดขวา
    # ---------------------------------------------------------
    top_left, top_space, top_right = st.columns([1.2, 1, 1.2])
    
    with top_left:
        student_list = sorted(df['Student Name'].unique())
        def reset_idx(): st.session_state.selected_idx = 0
        student_name = st.selectbox("เลือกนักเรียนที่ต้องการดูข้อมูล:", student_list, on_change=reset_idx)
        
    with top_right:
        # เทคนิคแปลงรูปเป็น Base64 เพื่อให้ล็อกชิดขวาได้ 100% ค่ะ
        logo_path = "aims_logo_2014_01_crop_blue_200x50px.png"
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as img_file:
                logo_b64 = base64.b64encode(img_file.read()).decode()
            img_html = f'<img src="data:image/png;base64,{logo_b64}" width="220">'
        else:
            img_html = '<img src="https://aims.co.th/wp-content/uploads/2019/12/Logo-aims.png" width="220">'
            
        st.markdown(f'''
            <div style='text-align: right;'>
                {img_html}
                <div style='color: #002d56; font-size: 14px; font-weight: bold; line-height: 1.2; margin-top: 5px;'>
                    Siam Square: 02-254-9300-2<br>
                    www.aims.co.th | Line ID: @aims2
                </div>
            </div>
        ''', unsafe_allow_html=True)

    # --- ดึงข้อมูลนักเรียน ---
    s_data = df[df['Student Name'] == student_name].sort_values('Date').reset_index(drop=True)
    
    if not s_data.empty:
        target_val = 1500
        if "active_student" not in st.session_state or st.session_state.active_student != student_name:
            st.session_state.active_student = student_name
            st.session_state.selected_idx = len(s_data) - 1

        c_idx = min(st.session_state.selected_idx, len(s_data) - 1)
        selected_attempt = s_data.iloc[c_idx]
        best_score = s_data['Total Score'].max()

        # ---------------------------------------------------------
        # LAYOUT แถวกลาง: ชื่อนักเรียน และ 1500 อยู่ตรงกลางเป๊ะๆ
        # ---------------------------------------------------------
        st.markdown(f"<div class='student-name-title'>{student_name}</div>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="target-container">
                <div class="target-label">TARGET SCORE</div>
                <div class="target-huge">{target_val}</div>
            </div>
        """, unsafe_allow_html=True)

        # KPI Metrics
        m1, m2, m3 = st.columns(3)
        with m1: st.metric("คะแนนครั้งที่เลือก", int(selected_attempt['Total Score']), f"At {c_idx+1}")
        with m2: st.metric("คะแนนสูงสุด (Best)", int(best_score))
        with m3:
            prog = int((best_score / target_val) * 100)
            st.metric("Progress to 1500", f"{prog}%", f"ขาดอีก {target_val - int(best_score)}")
            st.progress(prog/100)

        st.divider()

        # --- 6. Layout กราฟ (Blue & White) และรายละเอียด ---
        left, right = st.columns([1.7, 1.3])

        with left:
            st.subheader("📊 Performance Trend (At 1 - At 8)")
            fig = go.Figure()
            labels = [f"At {i+1}" for i in range(len(s_data))]
            
            # Math: สีฟ้าทึบ (Solid Blue) #002d56
            fig.add_trace(go.Bar(
                x=labels, y=s_data['Math Score'], name='Math', 
                marker_color='#002d56'
            ))
            # R&W: สีขาวขอบฟ้า (Solid White with Blue Border) #ffffff
            fig.add_trace(go.Bar(
                x=labels, y=s_data['R&W Score'], name='Reading & Writing', 
                marker=dict(
                    color='#ffffff', 
                    line=dict(color='#002d56', width=2) 
                )
            ))
            
            fig.update_layout(
                barmode='group',
                plot_bgcolor='#ffffff', # บังคับพื้นหลังกราฟเป็นสีขาว
                paper_bgcolor='#ffffff',
                xaxis=dict(title="Attempts"),
                yaxis=dict(title="Score", range=[200, 800], tickvals=[200, 400, 600, 800], gridcolor='#f1f5f9'),
                height=500,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            # บังคับ theme=None เด็ดขาด เพื่อไม่ให้ Streamlit ดึงสีมั่วค่ะ!
            st.plotly_chart(fig, use_container_width=True, theme=None)
            
            # ปุ่มเลือกดู Attempt
            st.write("🔍 เลือกครั้งที่ต้องการเจาะลึกข้อมูลด้านข้างค่ะ:")
            btn_cols = st.columns(len(s_data))
            for i in range(len(s_data)):
                if btn_cols[i].button(f"At {i+1}", key=f"btn_{i}", use_container_width=True, type="primary" if i == c_idx else "secondary"):
                    st.session_state.selected_idx = i
                    st.rerun()

        with right:
            st.markdown("<div class='attempt-card'>", unsafe_allow_html=True)
            st.subheader("📍 Attempt Details")
            st.markdown(f"🗓️ **วันที่สอบ:** {selected_attempt['Date']} | **Test Form:** {selected_attempt['Test Form']}")
            
            sc1, sc2 = st.columns(2)
            sc1.metric("Math Score", int(selected_attempt['Math Score']))
            sc2.metric("R&W Score", int(selected_attempt['R&W Score']))
            
            t_math, t_rw = st.tabs(["Math Topics", "R&W Topics"])
            with t_math:
                m_t = {"Algebra": 'Math Algebra (%)', "Problem Solving": 'Math Problem Solving (%)', "Advanced Math": 'Math Advanced Math (%)', "Additional Topics": 'Math Additional Topics (%)'}
                for k, v in m_t.items(): 
                    if v in selected_attempt:
                        st.markdown(f"<div class='topic-box'><span>{k}</span><b>{int(selected_attempt[v])}%</b></div>", unsafe_allow_html=True)
            with t_rw:
                r_t = {"Craft & Structure": 'R&W Craft & Structure (%)', "Info & Ideas": 'R&W Info & Ideas (%)', "Standard English": 'R&W Standard English (%)', "Expression of Ideas": 'R&W Expression of Ideas (%)'}
                for k, v in r_t.items():
                    if v in selected_attempt:
                        st.markdown(f"<div class='topic-box'><span>{k}</span><b>{int(selected_attempt[v])}%</b></div>", unsafe_allow_html=True)

            # --- 7. Smart Insight ---
            st.markdown("<div class='insight-box'>", unsafe_allow_html=True)
            st.markdown("<b style='color: #002d56; font-size: 19px;'>📖 ข้อแนะนำการเรียนเพิ่มเติม</b>", unsafe_allow_html=True)
            
            all_topics = {}
            for k, v in {**m_t, **r_t}.items():
                if v in selected_attempt: all_topics[k] = selected_attempt[v]
            
            if all_topics:
                weak_t = min(all_topics, key=all_topics.get)
                st.markdown(f"""
                    <div style='font-size: 14px; color: #1e293b; line-height: 1.7; margin: 15px 0;'>
                        หนูวิเคราะห์ข้อมูลครั้งนี้ให้แล้วนะคะ จุดที่น้องต้องเร่งเสริมเพื่อให้ถึง 1500 คือหัวข้อ <b>{weak_t}</b> ค่ะ 
                        ซึ่งทำได้เพียง <b>{int(all_topics[weak_t])}%</b> ในรอบนี้ หนูแนะนำให้พี่เน้นให้น้องทำโจทย์หัวข้อนี้เพิ่มขึ้นเป็นพิเศษนะคะ สู้ๆ ค่ะ!
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<b style='color: #002d56;'>📝 Incorrect Questions Analysis</b>", unsafe_allow_html=True)
            at_key = f"At {c_idx+1}"
            incorrect_info = incorrect_mapping.get(student_name, {}).get(at_key, "หนูกำลังอัปเดตข้อมูล PDF ให้อยู่นะคะ")
            st.markdown(f"<div class='error-chip'>{incorrect_info}</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

elif role == "Admin":
    st.title("⚙️ Admin Console")
    st.dataframe(df, use_container_width=True)
