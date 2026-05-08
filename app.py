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

# --- 2. การตั้งค่าหน้าตาแอป & CSS ---
st.set_page_config(page_title="aims SAT Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stMetric { background-color: white; padding: 20px; border-radius: 20px; border: 1px solid #e0f2fe; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    .attempt-card { background-color: white; padding: 25px; border-radius: 20px; border: 1px solid #e2e8f0; }
    .topic-box { background-color: white; padding: 12px 18px; border: 1px solid #e2e8f0; border-radius: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .insight-box { background-color: #f0f9ff; padding: 20px; border-radius: 20px; border: 1px solid #e0f2fe; margin-top: 15px; }
    .difficulty-tag { padding: 2px 8px; border-radius: 6px; font-size: 11px; font-weight: bold; }
    .easy { background-color: #dcfce7; color: #166534; }
    .medium { background-color: #fef9c3; color: #854d0e; }
    .hard { background-color: #fee2e2; color: #991b1b; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Sidebar ---
st.sidebar.title("🔐 aims Portal")
role = st.sidebar.radio("เข้าสู่ระบบในฐานะ:", ["Student", "Admin"])

if role == "Student" and df is not None:
    student_list = sorted(df['Student Name'].unique())
    
    def reset_idx(): st.session_state.selected_idx = 0
    student_name = st.sidebar.selectbox("เลือกชื่อนักเรียน:", student_list, on_change=reset_idx)
    
    s_data = df[df['Student Name'] == student_name].sort_values('Date').reset_index(drop=True)
    
    if not s_data.empty:
        target = 1500 # เป้าหมาย 1500 คะแนนเท่ากันทุกคน
        
        if "active_student" not in st.session_state or st.session_state.active_student != student_name:
            st.session_state.active_student = student_name
            st.session_state.selected_idx = len(s_data) - 1

        c_idx = min(st.session_state.selected_idx, len(s_data) - 1)
        selected_attempt = s_data.iloc[c_idx]
        best_score = s_data['Total Score'].max()

        # Header
        st.title(f"✨ Student Report: {student_name}")
        st.markdown(f"<p style='color: #64748b;'>เป้าหมายร่วมกัน: <b style='color: #0284c7; font-size: 20px;'>{target}</b> คะแนน</p>", unsafe_allow_html=True)

        # Top Metrics
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("คะแนนครั้งที่เลือก", int(selected_attempt['Total Score']), f"Attempt {c_idx+1}")
        with c2: st.metric("คะแนนสูงสุด (Best)", int(best_score))
        with c3:
            prog = int((best_score / target) * 100)
            gap = target - int(best_score)
            st.metric("Progress to 1500", f"{prog}%", f"ยังขาดอีก {gap} คะแนน")
            st.progress(prog/100)

        st.divider()

        # --- Layout กราฟและรายละเอียด ---
        left, right = st.columns([1.8, 1.2])

        with left:
            st.subheader("📊 Score Trend")
            fig = go.Figure()
            labels = [f"At {i+1}" for i in range(len(s_data))]
            
            # Math Bar
            fig.add_trace(go.Bar(x=labels, y=s_data['Math Score'], name='Math', marker_color='#0284c7'))
            # R&W Bar
            fig.add_trace(go.Bar(x=labels, y=s_data['R&W Score'], name='Reading & Writing', marker_color='rgba(0,0,0,0)', marker_line_color='#0284c7', marker_line_width=2))
            
            # ปรับแกนตามคำขอ: Y = คะแนน (200-800), X = ครั้งที่สอบ
            fig.update_layout(
                barmode='group',
                xaxis=dict(title="ครั้งที่สอบ (Attempts)"),
                yaxis=dict(title="คะแนนสอบ (Score)", tickvals=[200, 300, 400, 500, 600, 700, 800], range=[200, 800], gridcolor='#f1f5f9'),
                height=500, margin=dict(l=0, r=0, t=20, b=0), plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # ปุ่มเลือกดู Attempt
            st.write("🔍 คลิกเลือกครั้งที่สอบเพื่อดูรายละเอียดด้านข้าง:")
            btn_cols = st.columns(len(s_data))
            for i in range(len(s_data)):
                if btn_cols[i].button(f"At {i+1}", key=f"bt_{i}", use_container_width=True, type="primary" if i == c_idx else "secondary"):
                    st.session_state.selected_idx = i
                    st.rerun()

        with right:
            st.markdown("<div class='attempt-card'>", unsafe_allow_html=True)
            st.subheader("📍 Attempt Detail")
            
            # เพิ่ม Math Score และ R&W Score ในหน้ารายละเอียด
            sc1, sc2 = st.columns(2)
            sc1.metric("Math Score", int(selected_attempt['Math Score']))
            sc2.metric("R&W Score", int(selected_attempt['R&W Score']))
            
            st.write(f"**Test Form:** {selected_attempt['Test Form']}")
            st.caption(f"วันที่สอบ: {selected_attempt['Date']}")
            
            t1, t2 = st.tabs(["Math Topics", "R&W Topics"])
            with t1:
                m_topics = {"Algebra": 'Math Algebra (%)', "Problem Solving": 'Math Problem Solving (%)', "Advanced Math": 'Math Advanced Math (%)', "Additional Topics": 'Math Additional Topics (%)'}
                for k, v in m_topics.items(): st.markdown(f"<div class='topic-box'><span>{k}</span><b>{int(selected_attempt[v])}%</b></div>", unsafe_allow_html=True)
            with t2:
                r_topics = {"Craft & Structure": 'R&W Craft & Structure (%)', "Info & Ideas": 'R&W Info & Ideas (%)', "Standard English": 'R&W Standard English (%)', "Expression of Ideas": 'R&W Expression of Ideas (%)'}
                for k, v in r_topics.items(): st.markdown(f"<div class='topic-box'><span>{k}</span><b>{int(selected_attempt[v])}%</b></div>", unsafe_allow_html=True)

            # --- Smart Insight (โดยพี่ใจดี) ---
            st.markdown("<div class='insight-box'>", unsafe_allow_html=True)
            st.markdown("<b style='color: #0369a1; font-size: 16px;'>👩‍🏫 Smart Insight (โดยพี่ใจดี)</b>", unsafe_allow_html=True)
            
            # วิเคราะห์หัวข้อที่อ่อนที่สุด
            all_scores = {**{k: selected_attempt[v] for k, v in m_topics.items()}, **{k: selected_attempt[v] for k, v in r_topics.items()}}
            weakest = min(all_scores, key=all_scores.get)
            
            st.markdown(f"""
                <p style='font-size: 13px; color: #0c4a6e; margin-top: 10px;'>
                พี่คะ ครั้งนี้น้องมีจุดที่ต้องเร่งเสริมด่วนในหัวข้อ <b>{weakest}</b> ค่ะ เพราะได้คะแนนเพียง <b>{int(all_scores[weakest])}%</b> เท่านั้น 
                แนะนำให้พี่เน้นสอนหัวข้อนี้ก่อนนะคะ เพื่อเพิ่มโอกาสพุ่งสู่ 1500 ค่ะ!
            </p>
            <hr style='border: 0.5px solid #e0f2fe;'>
            <p style='font-size: 13px; color: #0c4a6e; font-weight: bold;'>📝 Incorrect Questions Analysis:</p>
            """, unsafe_allow_html=True)
            
            # จำลองข้อมูลข้อที่ผิดแบบ Dynamic (ในอนาคตดึงจากไฟล์ PDF รายข้อได้)
            # ตัวอย่างการจำลองตามโจทย์ที่พี่มหาให้มา
            incorrect_map = {
                "Q12": {"topic": "Algebra", "diff": "Hard", "class": "hard"},
                "Q19": {"topic": "Info & Ideas", "diff": "Medium", "class": "medium"},
                "Q22": {"topic": "Additional Topics", "diff": "Hard", "class": "hard"},
                "Q05": {"topic": "Standard English", "diff": "Easy", "class": "easy"}
            }
            
            for q_num, info in incorrect_map.items():
                st.markdown(f"""
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;'>
                        <span style='font-size: 12px; color: #1e293b;'><b>{q_num}</b> | {info['topic']}</span>
                        <span class='difficulty-tag {info['class']}'>{info['diff']}</span>
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

elif role == "Admin":
    st.title("⚙️ aims Admin Control")
    st.dataframe(df, use_container_width=True)

st.markdown("<br><center style='color: #94a3b8; font-size: 11px;'>aims SAT Dashboard • P' Jaidee & Student Edition</center>", unsafe_allow_html=True)
