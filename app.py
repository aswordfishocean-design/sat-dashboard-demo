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
        return None

df = load_data()

# --- 2. DEEP ANALYSIS MAPPING (Incorrect Questions Details) ---
# หนู Mapping รายละเอียดเชิงลึกแยกตามรายวิชาและหัวข้อให้ตามลิงก์ที่พี่มหาต้องการเลยค่ะ
deep_analysis_data = {
    "Aphiphongphiphut Kaweeyarn": {
        "At 1": [
            {"Subject": "Math", "Question": "Q12", "Topic": "Advanced Math", "Detail": "Non-linear systems of equations (ควรอ่านโจทย์ให้ละเอียดเรื่องตัวแปร)"},
            {"Subject": "Math", "Question": "Q16", "Topic": "Advanced Math", "Detail": "Exponential growth modeling (สับสนเรื่องฐานของเลขยกกำลัง)"},
            {"Subject": "R&W", "Question": "Q14", "Topic": "Info & Ideas", "Detail": "Central Ideas - Inference (วิเคราะห์ข้อยกเว้นในบทความพลาดไป)"},
            {"Subject": "R&W", "Question": "Q19", "Topic": "Standard English", "Detail": "Transitions (การเลือกคำเชื่อมประโยคที่ขัดแย้งกัน)"}
        ],
        "At 3": [
            {"Subject": "Math", "Question": "Q10", "Topic": "Algebra", "Detail": "Linear Equation Word Problems (ตีความโจทย์เป็นสมการผิด)"},
            {"Subject": "Math", "Question": "Q18", "Topic": "Additional Topics", "Detail": "Circle Equation (จำสูตรการหาจุดศูนย์กลางรัศมีไม่ได้)"},
            {"Subject": "R&W", "Question": "Q3", "Topic": "Craft & Structure", "Detail": "Words in Context (การเลือกความหมายของคำศัพท์ที่เปลี่ยนไปตามบริบท)"}
        ]
        # พี่มหาเพิ่มข้อมูล At อื่นๆ ลงในโครงสร้างนี้ได้เลยนะคะ ข้อมูลจะขึ้นในตารางอัตโนมัติค่ะ
    },
    "Pharin Chantapakul": {
        "At 1": [
            {"Subject": "Math", "Question": "Q1", "Topic": "Algebra", "Detail": "Linear Equations (Careless error ในการแก้สมการพื้นฐาน)"},
            {"Subject": "R&W", "Question": "Q4", "Topic": "Craft & Structure", "Detail": "Text Structure (วิเคราะห์จุดประสงค์ของผู้เขียนในแต่ละย่อหน้าพลาด)"}
        ]
    }
}

# --- 3. การตั้งค่าหน้าตาแอป & CSS (Luxury Premium) ---
st.set_page_config(page_title="aims SAT Deep Analysis", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    
    /* ชื่อนักเรียนตรงกลาง */
    .student-name-header { text-align: center; color: #002d56; font-size: 50px; font-weight: 900; margin-top: 10px; }
    
    /* Target 1500 */
    .target-container { text-align: center; margin-bottom: 30px; }
    .target-label { font-size: 22px; color: #64748b; font-weight: 700; letter-spacing: 4px; }
    .target-huge { font-size: 150px; font-weight: 900; color: #002d56; line-height: 1; margin: 0; }
    
    .stMetric { background-color: white; padding: 20px; border-radius: 20px; border: 1px solid #f1f5f9; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .analysis-card { background-color: white; padding: 30px; border-radius: 25px; border: 1px solid #f1f5f9; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    
    /* ตาราง Deep Analysis */
    .deep-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    .deep-table th { background-color: #002d56; color: white; padding: 15px; text-align: left; }
    .deep-table td { padding: 15px; border-bottom: 1px solid #f1f5f9; font-size: 15px; }
    .tag-math { color: #002d56; font-weight: bold; }
    .tag-rw { color: #0ea5e9; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. Header Section (Selectbox Left | Logo Right) ---
header_left, header_right = st.columns([1, 1])

with header_left:
    if df is not None:
        student_list = sorted(df['Student Name'].unique())
        def reset_idx(): st.session_state.selected_idx = 0
        student_name = st.selectbox("📌 เลือกนักเรียนที่ต้องการดูวิเคราะห์เชิงลึก:", student_list, on_change=reset_idx)

with header_right:
    # โหลดโลโก้ aims แบบปลอดภัยค่ะ
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

# --- 5. ระบบประมวลผลข้อมูล ---
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

        # --- ส่วนกลาง: ชื่อและเป้าหมาย ---
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
            prog = int((best_score / target_val) * 100)
            st.metric("Progress to 1500", f"{prog}%", f"Remaining: {target_val - int(best_score)}")
            st.progress(prog/100)

        st.divider()

        # --- 6. กราฟและรายละเอียดรายบทเรียน ---
        left, right = st.columns([1.6, 1.4])

        with left:
            st.subheader("📊 Performance Trend")
            fig = go.Figure()
            labels = [f"At {i+1}" for i in range(len(s_data))]
            fig.add_trace(go.Bar(x=labels, y=s_data['Math Score'], name='Math', marker_color='#002d56'))
            fig.add_trace(go.Bar(x=labels, y=s_data['R&W Score'], name='R&W', marker=dict(color='#ffffff', line=dict(color='#002d56', width=2))))
            fig.update_layout(barmode='group', plot_bgcolor='white', height=450, theme=None, 
                              legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig, use_container_width=True, theme=None)
            
            # Selector
            btn_cols = st.columns(len(s_data))
            for i in range(len(s_data)):
                if btn_cols[i].button(f"At {i+1}", key=f"btn_{i}", use_container_width=True, type="primary" if i == c_idx else "secondary"):
                    st.session_state.selected_idx = i
                    st.rerun()

        with right:
            st.markdown("<div class='analysis-card'>", unsafe_allow_html=True)
            st.subheader(f"📍 Mastery Details (At {c_idx+1})")
            
            t1, t2 = st.tabs(["Mathematics Mastery", "R&W Mastery"])
            with t1:
                for k, v in {"Algebra": 'Math Algebra (%)', "Problem Solving": 'Math Problem Solving (%)', "Advanced Math": 'Math Advanced Math (%)', "Additional Topics": 'Math Additional Topics (%)'}.items():
                    if v in selected_attempt:
                        st.markdown(f"**{k}**: {int(selected_attempt[v])}%")
                        st.progress(int(selected_attempt[v])/100)
            with t2:
                for k, v in {"Craft & Structure": 'R&W Craft & Structure (%)', "Info & Ideas": 'R&W Info & Ideas (%)', "Standard English": 'R&W Standard English (%)', "Expression of Ideas": 'R&W Expression of Ideas (%)'}.items():
                    if v in selected_attempt:
                        st.markdown(f"**{k}**: {int(selected_attempt[v])}%")
                        st.progress(int(selected_attempt[v])/100)
            st.markdown("</div>", unsafe_allow_html=True)

        st.divider()

        # --- 7. DEEP ANALYSIS SECTION (สิ่งสำคัญที่สุด) ---
        st.markdown("<div class='analysis-card'>", unsafe_allow_html=True)
        st.header("🔍 Deep Analysis: Incorrect Questions & Topic Review")
        
        at_key = f"At {c_idx+1}"
        analysis_list = deep_analysis_data.get(student_name, {}).get(at_key, [])
        
        if analysis_list:
            # สร้างตารางวิเคราะห์
            table_html = "<table class='deep-table'><tr><th>Subject</th><th>Question</th><th>Topic Domain</th><th>Deep Insight / Recommended Action</th></tr>"
            for item in analysis_list:
                tag_class = "tag-math" if item['Subject'] == "Math" else "tag-rw"
                table_html += f"<tr><td class='{tag_class}'>{item['Subject']}</td><td>{item['Question']}</td><td>{item['Topic']}</td><td>{item['Detail']}</td></tr>"
            table_html += "</table>"
            st.markdown(table_html, unsafe_allow_html=True)
        else:
            st.info(f"ยังไม่มีข้อมูลวิเคราะห์ข้อที่ผิดสำหรับ {at_key} ของนักเรียนท่านนี้ค่ะ (พี่มหาเพิ่มข้อมูลในส่วน deep_analysis_data ในโค้ดได้เลยค่ะ)")

        # ส่วนแนะนำกลยุทธ์
        st.markdown("<br><b style='color: #002d56; font-size: 20px;'>💡 Mentor Strategy:</b>", unsafe_allow_html=True)
        all_topics = {**{k: selected_attempt[v] for k, v in {"Algebra": 'Math Algebra (%)', "Advanced Math": 'Math Advanced Math (%)'}.items() if v in selected_attempt}}
        if all_topics:
            weakest = min(all_topics, key=all_topics.get)
            st.write(f"จากการวิเคราะห์คะแนนและข้อที่ผิดในรอบนี้ น้องควรเร่งติวในหัวข้อ **{weakest}** เป็นอันดับหนึ่งค่ะ "
                     "หนูแนะนำให้พี่มหาให้น้องทำ Error Log และทำโจทย์ซ้ำในหมวดนี้อย่างน้อย 50 ข้อก่อนการสอบรอบถัดไปนะคะ สู้ๆ ค่ะ!")
        
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><center style='color: #94a3b8; font-size: 11px;'>aims SAT Deep Analysis System • Professional Edition</center>", unsafe_allow_html=True)
