import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# --- 1. การเชื่อมต่อข้อมูล (V3) ---
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

# --- 2. ฐานข้อมูล Incorrect Questions (At 1 - At 8) สกัดจาก PDF จริงค่ะ ---
incorrect_mapping = {
    "Aphiphongphiphut Kaweeyarn": {
        "At 1": "Math: Q12, Q16, Q17, Q21 (Adv. Math/Add.) | R&W: Q14, Q19, Q20, Q21, Q27 (Ideas/Std. Eng)",
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

# --- 3. การตั้งค่าหน้าตาแอป & CSS (Professional Luxury Theme) ---
st.set_page_config(page_title="aims SAT Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #fcfdfe; }
    
    /* Target Score Section */
    .target-container { text-align: center; margin-top: -20px; }
    .target-label { font-size: 24px; color: #64748b; font-weight: 700; letter-spacing: 5px; }
    .target-huge { font-size: 150px; font-weight: 900; color: #002d56; line-height: 1; margin: 0; }
    
    .stMetric { background-color: white; padding: 20px; border-radius: 20px; border: 1px solid #e2e8f0; }
    .attempt-card { background-color: white; padding: 30px; border-radius: 25px; border: 1px solid #f1f5f9; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05); }
    .topic-box { background-color: #ffffff; padding: 12px 18px; border-radius: 15px; border: 1px solid #f1f5f9; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .insight-box { background-color: #f0f9ff; padding: 25px; border-radius: 20px; border: 1px solid #e0f2fe; margin-top: 20px; }
    .error-chip { background-color: #fff1f2; color: #e11d48; border: 1px solid #fecdd3; padding: 12px 15px; border-radius: 12px; font-size: 14px; font-weight: 600; margin-top: 10px; display: block; }
    
    /* Contact Styling (Tight line spacing) */
    .contact-info {
        text-align: right; 
        color: #002d56; 
        font-size: 15px; 
        font-weight: bold; 
        line-height: 1.1; /* บรรทัดชิดกันตามสั่งค่ะ */
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. Top Section: Student Name & Branding (Logo on Right) ---
top_left, top_right = st.columns([2, 1])

with top_left:
    # ชื่อนักเรียนอยู่ฝั่งซ้ายของโลโก้ค่ะ
    if df is not None:
        student_list = sorted(df['Student Name'].unique())
        def reset_idx(): st.session_state.selected_idx = 0
        student_name = st.selectbox("เลือกนักเรียนที่ต้องการดูข้อมูล:", student_list, on_change=reset_idx)
        st.markdown(f"<h1 style='color: #002d56; font-size: 42px; margin-top: 10px;'>{student_name}</h1>", unsafe_allow_html=True)

with top_right:
    # โลโก้และข้อมูลติดต่อชิดกันมุมขวาบนค่ะ
    logo_filename = "aims_logo_2014_01_crop_blue_200x50px.png"
    if os.path.exists(logo_filename):
        st.image(logo_filename, width=240)
    else:
        st.image("https://aims.co.th/wp-content/uploads/2019/12/Logo-aims.png", width=240)
    
    st.markdown(f"""
        <div class="contact-info">
            Siam Square: 02-254-9300-2<br>
            www.aims.co.th | Line ID: @aims2
        </div>
    """, unsafe_allow_html=True)

# --- 5. ระบบ Dashboard ---
if df is not None:
    s_data = df[df['Student Name'] == student_name].sort_values('Date').reset_index(drop=True)
    
    if not s_data.empty:
        target_val = 1500
        if "active_student" not in st.session_state or st.session_state.active_student != student_name:
            st.session_state.active_student = student_name
            st.session_state.selected_idx = len(s_data) - 1

        c_idx = min(st.session_state.selected_idx, len(s_data) - 1)
        selected_attempt = s_data.iloc[c_idx]
        best_score = s_data['Total Score'].max()

        # ส่วนเป้าหมายตัวใหญ่ยักษ์
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
            
            # Math: สีฟ้าทึบ (Solid Blue)
            fig.add_trace(go.Bar(
                x=labels, y=s_data['Math Score'], name='Math', 
                marker=dict(color='#002d56')
            ))
            # R&W: สีขาวขอบฟ้า (Hollow White)
            fig.add_trace(go.Bar(
                x=labels, y=s_data['R&W Score'], name='Reading & Writing', 
                marker=dict(
                    color='rgba(255, 255, 255, 1)', # พื้นขาวทึบ
                    line=dict(color='#002d56', width=3) # ขอบสีฟ้าทึบ
                )
            ))
            
            fig.update_layout(
                barmode='group',
                xaxis=dict(title="Attempts"),
                yaxis=dict(title="Score", range=[200, 800], tickvals=[200, 400, 600, 800], gridcolor='#f1f5f9'),
                height=500, plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            # บังคับ theme=None เพื่อให้สีกราฟไม่เพี้ยนค่ะ
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

            # --- 7. ข้อแนะนำ (Smart Insight) ---
            st.markdown("<div class='insight-box'>", unsafe_allow_html=True)
            st.markdown("<b style='color: #002d56; font-size: 19px;'>📖 ข้อแนะนำการเรียนเพิ่มเติม</b>", unsafe_allow_html=True)
            
            all_topics = {}
            for k, v in {**m_t, **r_t}.items():
                if v in selected_attempt: all_topics[k] = selected_attempt[v]
            
            if all_topics:
                weak_t = min(all_topics, key=all_topics.get)
                st.markdown(f"""
                    <div style='font-size: 15px; color: #1e293b; line-height: 1.7; margin: 15px 0;'>
                        หนูวิเคราะห์ข้อมูลครั้งนี้ให้แล้วนะคะ จุดที่น้องต้องเร่งเสริมเพื่อให้ถึง 1500 คือหัวข้อ <b>{weak_t}</b> ค่ะ 
                        ซึ่งได้เพียง <b>{int(all_topics[weak_t])}%</b> ในรอบนี้ หนูแนะนำให้พี่เน้นให้น้องทำโจทย์หัวข้อนี้เพิ่มขึ้นเป็นพิเศษนะคะ สู้ๆ ค่ะ!
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<b style='color: #002d56;'>📝 Incorrect Questions Analysis</b>", unsafe_allow_html=True)
            at_key = f"At {c_idx+1}"
            incorrect_info = incorrect_mapping.get(student_name, {}).get(at_key, "หนูกำลังอัปเดตข้อมูลข้อที่ผิดให้ตามไฟล์ PDF ค่ะ")
            st.markdown(f"<div class='error-chip'>{incorrect_info}</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><center style='color: #94a3b8; font-size: 11px;'>aims SAT Dashboard • Professional Edition • Data Synced from PDF</center>", unsafe_allow_html=True)
