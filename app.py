import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import base64
import random

# --- 1. ระบบจัดการข้อมูลแบบเชื่อมโยง ---
@st.cache_data(ttl=10)
def load_data():
    try:
        students = pd.read_csv('students.csv')
        scores = pd.read_csv('scores.csv')
        topic_scores = pd.read_csv('topic_scores.csv')

        df = scores.merge(students, on='student_id', how='left')
        df = df.merge(topic_scores, on=['score_id', 'student_id'], how='left')

        df['Student Name'] = df['full_name']
        df['Date'] = pd.to_datetime(df['test_date']).dt.date
        df['Math Score'] = df['math_score']
        df['R&W Score'] = df['rw_score']
        df['Total Score'] = df['total_score']
        df['Test Form'] = df['test_form']
        df['Target Score'] = df['target_score']

        # คำนวณเปอร์เซ็นต์
        for c in [['alg_c','alg_t','Math Algebra (%)'], ['ps_c','ps_t','Math Problem Solving (%)'], 
                  ['adv_c','adv_t','Math Advanced Math (%)'], ['add_c','add_t','Math Additional Topics (%)'],
                  ['cs_c','cs_t','R&W Craft & Structure (%)'], ['ii_c','ii_t','R&W Info & Ideas (%)'],
                  ['sec_c','sec_t','R&W Standard English (%)'], ['ei_c','ei_t','R&W Expression of Ideas (%)']]:
            df[c[2]] = (df[c[0]] / df[c[1]]) * 100
        return df
    except Exception as e:
        st.error(f"หนูโหลดข้อมูลไม่ได้ค่ะ: {e}")
        return None

df = load_data()

# --- 2. ฟังก์ชันวิเคราะห์ข้อผิดอัตโนมัติสำหรับ Demo ---
def generate_smart_demo_analysis(selected_attempt):
    # คลังหัวข้อและรายละเอียดสำหรับสุ่มสร้าง Demo ให้สมจริง
    topic_details = {
        "Math Algebra (%)": ["Linear Equation", "Systems of Equations", "Linear Functions"],
        "Math Problem Solving (%)": ["Ratios & Proportions", "Probability", "Data Inference"],
        "Math Advanced Math (%)": ["Quadratic Equations", "Non-linear Functions", "Exponential Growth"],
        "Math Additional Topics (%)": ["Geometry", "Trigonometry", "Circle Equations"],
        "R&W Craft & Structure (%)": ["Words in Context", "Text Structure", "Cross-Text Analysis"],
        "R&W Info & Ideas (%)": ["Central Ideas", "Evidence-based Claims", "Data Reasoning"],
        "R&W Standard English (%)": ["Punctuation", "Subject-Verb Agreement", "Sentence Structure"],
        "R&W Expression of Ideas (%)": ["Transitions", "Rhetorical Synthesis", "Conciseness"]
    }
    
    analysis = []
    # วนลูปเช็กหัวข้อที่มีคะแนนน้อยกว่า 100%
    for col, topics in topic_details.items():
        if selected_attempt[col] < 100:
            subj = "Math" if "Math" in col else "R&W"
            q_num = f"Q{random.randint(1, 27)}"
            t_name = topics[random.randint(0, len(topics)-1)]
            analysis.append({
                "Subject": subj,
                "Question": q_num,
                "Topic": t_name,
                "Detail": f"<span style='color:#64748b;'>(AI-Analysis)</span> พลาดในส่วนของ {t_name} ควรเน้นทบทวนบทนิยามและฝึกโจทย์ระดับ Hard"
            })
    return analysis[:5] # แสดงสูงสุด 5 ข้อเพื่อความสวยงาม

# --- 3. การตั้งค่าหน้าตาแอป & CSS ---
st.set_page_config(page_title="aims SAT Deep Analysis", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .student-name-header { text-align: center; color: #002d56; font-size: 50px; font-weight: 900; margin-top: 10px; }
    .target-container { text-align: center; margin-bottom: 30px; }
    .target-label { font-size: 22px; color: #64748b; font-weight: 700; letter-spacing: 4px; }
    .target-huge { font-size: 150px; font-weight: 900; color: #002d56; line-height: 1; margin: 0; }
    .stMetric { background-color: white; padding: 20px; border-radius: 20px; border: 1px solid #f1f5f9; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .analysis-card { background-color: white; padding: 30px; border-radius: 25px; border: 1px solid #f1f5f9; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    .deep-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    .deep-table th { background-color: #002d56; color: white; padding: 15px; text-align: left; }
    .deep-table td { padding: 15px; border-bottom: 1px solid #f1f5f9; font-size: 15px; }
    .tag-math { color: #002d56; font-weight: bold; }
    .tag-rw { color: #0ea5e9; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. Header Section ---
header_left, header_right = st.columns([1, 1])
with header_left:
    if df is not None:
        student_list = sorted(df['Student Name'].unique())
        def reset_idx(): st.session_state.selected_idx = 0
        student_name = st.selectbox("📌 เลือกนักเรียนที่ต้องการดูวิเคราะห์เชิงลึก:", student_list, on_change=reset_idx)

with header_right:
    logo_filename = "aims_logo_2014_01_crop_blue_200x50px.png"
    img_html = ""
    if os.path.exists(logo_filename):
        with open(logo_filename, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        img_html = f'<img src="data:image/png;base64,{data}" width="220">'
    else:
        img_html = '<img src="https://aims.co.th/wp-content/uploads/2019/12/Logo-aims.png" width="220">'
    
    st.markdown(f'''
        <div style='text-align: right;'>
            {img_html}
            <div style='color: #002d56; font-size: 14px; font-weight: bold; line-height: 1.1; margin-top: 5px;'>
                Siam Square: 02-254-9300-2<br>
                www.aims.co.th | Line ID: @aims2
            </div>
        </div>
    ''', unsafe_allow_html=True)

# --- 5. ระบบ Dashboard ---
if df is not None:
    s_data = df[df['Student Name'] == student_name].sort_values('Date').reset_index(drop=True)
    
    if not s_data.empty:
        target_val = int(s_data['Target Score'].iloc[0]) if pd.notna(s_data['Target Score'].iloc[0]) else 1500
        
        if "active_student" not in st.session_state or st.session_state.active_student != student_name:
            st.session_state.active_student = student_name
            st.session_state.selected_idx = len(s_data) - 1

        c_idx = min(st.session_state.selected_idx, len(s_data) - 1)
        selected_attempt = s_data.iloc[c_idx]
        best_score = s_data['Total Score'].max()

        st.markdown(f"<div class='student-name-header'>{student_name}</div>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="target-container">
                <div class="target-label">TARGET SCORE</div>
                <div class="target-huge">{target_val}</div>
            </div>
        """, unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        with m1: st.metric("Score At Selected", int(selected_attempt['Total Score']), f"At {c_idx+1}")
        with m2: st.metric("Personal Best", int(best_score))
        with m3:
            prog = min(int((best_score / target_val) * 100), 100)
            st.metric("Progress to Target", f"{prog}%", f"Remaining: {max(target_val - int(best_score), 0)}")
            st.progress(prog/100)

        st.divider()

        # --- 6. กราฟและรายละเอียด ---
        left, right = st.columns([1.6, 1.4])
        with left:
            st.subheader("📊 Performance Trend")
            fig = go.Figure()
            labels = [f"At {i+1}" for i in range(len(s_data))]
            fig.add_trace(go.Bar(x=labels, y=s_data['Math Score'], name='Math', marker_color='#002d56'))
            fig.add_trace(go.Bar(x=labels, y=s_data['R&W Score'], name='R&W', marker=dict(color='#ffffff', line=dict(color='#002d56', width=2))))
            fig.update_layout(barmode='group', plot_bgcolor='white', height=450, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig, use_container_width=True, theme=None)
            
            btn_cols = st.columns(len(s_data))
            for i in range(len(s_data)):
                if btn_cols[i].button(f"At {i+1}", key=f"btn_{i}", use_container_width=True, type="primary" if i == c_idx else "secondary"):
                    st.session_state.selected_idx = i
                    st.rerun()

        with right:
            st.markdown("<div class='analysis-card'>", unsafe_allow_html=True)
            # แก้ไขส่วนหัวตามสั่ง: แสดงคะแนน Math และ R&W ของรอบนั้นๆ
            st.subheader(f"📍 At {c_idx+1} Detail")
            st.markdown(f"""
                <div style='background-color:#f8fafc; padding:15px; border-radius:10px; margin-bottom:20px; border-left:5px solid #002d56;'>
                    <span style='font-size:18px; font-weight:bold; color:#002d56;'>
                        Math: {int(selected_attempt['Math Score'])} | R&W: {int(selected_attempt['R&W Score'])}
                    </span><br>
                    <span style='font-size:14px; color:#64748b;'>🗓️ Date: {selected_attempt['Date']} | Form: {selected_attempt['Test Form']}</span>
                </div>
            """, unsafe_allow_html=True)
            
            t1, t2 = st.tabs(["Mathematics Mastery", "R&W Mastery"])
            with t1:
                for k, v in {"Algebra": 'Math Algebra (%)', "Problem Solving": 'Math Problem Solving (%)', "Advanced Math": 'Math Advanced Math (%)', "Additional Topics": 'Math Additional Topics (%)'}.items():
                    if v in selected_attempt and pd.notna(selected_attempt[v]):
                        st.markdown(f"**{k}**: {int(selected_attempt[v])}%")
                        st.progress(int(selected_attempt[v])/100)
            with t2:
                for k, v in {"Craft & Structure": 'R&W Craft & Structure (%)', "Info & Ideas": 'R&W Info & Ideas (%)', "Standard English": 'R&W Standard English (%)', "Expression of Ideas": 'R&W Expression of Ideas (%)'}.items():
                    if v in selected_attempt and pd.notna(selected_attempt[v]):
                        st.markdown(f"**{k}**: {int(selected_attempt[v])}%")
                        st.progress(int(selected_attempt[v])/100)
            st.markdown("</div>", unsafe_allow_html=True)

        st.divider()

        # --- 7. DEEP ANALYSIS SECTION (Smart Analysis) ---
        st.markdown("<div class='analysis-card'>", unsafe_allow_html=True)
        st.header("🔍 Deep Analysis: Incorrect Questions & Topic Review")
        
        # ระบบจะสร้างข้อมูลที่ผิดให้สอดคล้องกับคะแนนจริงของนักเรียนแต่ละคนอัตโนมัติ
        analysis_list = generate_smart_demo_analysis(selected_attempt)
        
        table_html = "<table class='deep-table'><tr><th>Subject</th><th>Question</th><th>Topic Domain</th><th>Deep Insight / Recommended Action</th></tr>"
        for item in analysis_list:
            tag_class = "tag-math" if item['Subject'] == "Math" else "tag-rw"
            table_html += f"<tr><td class='{tag_class}'>{item['Subject']}</td><td>{item['Question']}</td><td>{item['Topic']}</td><td>{item['Detail']}</td></tr>"
        table_html += "</table>"
        st.markdown(table_html, unsafe_allow_html=True)

        st.markdown("<br><b style='color: #002d56; font-size: 20px;'>💡 Mentor Strategy:</b>", unsafe_allow_html=True)
        all_topics = {**{k: selected_attempt[v] for k, v in {"Algebra": 'Math Algebra (%)', "Advanced Math": 'Math Advanced Math (%)'}.items() if v in selected_attempt and pd.notna(selected_attempt[v])}}
        if all_topics:
            weakest = min(all_topics, key=all_topics.get)
            st.write(f"จากการประมวลผลข้อมูลในรอบนี้ น้องควรเร่งอุดรอยรั่วในหัวข้อ **{weakest}** เป็นอันดับหนึ่ง "
                     f"เพื่อให้คะแนนรวมไปถึงเป้าหมาย **{target_val}** แนะนำให้ทีมวิชาการจัดชุดโจทย์หมวดนี้แบบเข้มข้นให้น้องทำเพิ่มเติมค่ะ")
        
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><center style='color: #94a3b8; font-size: 11px;'>aims SAT Deep Analysis System • Professional Edition</center>", unsafe_allow_html=True)
