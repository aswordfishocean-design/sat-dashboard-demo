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

# --- 2. ตั้งค่า Layout ---
st.set_page_config(page_title="aims SAT Dashboard", layout="wide")

if df is not None:
    st.markdown("""
        <style>
        .main { background-color: #f8fafc; }
        .stMetric { background-color: white; padding: 20px; border-radius: 20px; border: 1px solid #e0f2fe; }
        .attempt-card { background-color: white; padding: 25px; border-radius: 20px; border: 1px solid #e2e8f0; }
        .topic-box { background-color: white; padding: 12px 18px; border: 1px solid #e2e8f0; border-radius: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; }
        .insight-box { background-color: #f0f9ff; padding: 20px; border-radius: 20px; border: 1px solid #e0f2fe; margin-top: 15px; }
        .error-chip { background-color: #fff1f2; color: #e11d48; border: 1px solid #fecdd3; padding: 4px 10px; border-radius: 8px; font-size: 12px; font-weight: 600; margin-right: 5px; margin-bottom: 5px; display: inline-block; }
        </style>
        """, unsafe_allow_html=True)

    # --- 3. Sidebar ---
    st.sidebar.title("🔐 aims Portal")
    role = st.sidebar.radio("เข้าสู่ระบบในฐานะ:", ["Student", "Admin"])

    if role == "Student":
        student_list = sorted(df['Student Name'].unique())
        
        if "selected_idx" not in st.session_state: st.session_state.selected_idx = 0

        def reset_idx(): st.session_state.selected_idx = 0
        student_name = st.sidebar.selectbox("เลือกชื่อนักเรียน:", student_list, on_change=reset_idx)
        
        s_data = df[df['Student Name'] == student_name].sort_values('Date').reset_index(drop=True)
        
        if not s_data.empty:
            # บังคับเป้าหมาย 1500
            target = 1500
            
            if "current_student" not in st.session_state or st.session_state.current_student != student_name:
                st.session_state.current_student = student_name
                st.session_state.selected_idx = len(s_data) - 1

            c_idx = min(st.session_state.selected_idx, len(s_data) - 1)
            selected_attempt = s_data.iloc[c_idx]
            best_score = s_data['Total Score'].max()

            # Header
            st.title(f"✨ {student_name}")
            st.markdown(f"<p style='color: #64748b;'>Target Score: <b style='color: #0284c7;'>{target}</b> | Best: {int(best_score)}</p>", unsafe_allow_html=True)

            # Metrics
            c1, c2, c3 = st.columns(3)
            with c1: st.metric("Score ครั้งที่เลือก", int(selected_attempt['Total Score']), f"Attempt {c_idx+1}")
            with c2: st.metric("คะแนนสูงสุด", int(best_score))
            with c3:
                prog = int((best_score / target) * 100)
                st.metric("Progress", f"{prog}%", f"Gap: {target - int(best_score)}")
                st.progress(prog/100)

            st.divider()

            # Layout
            left, right = st.columns([2, 1])

            with left:
                st.subheader("Score Trend")
                fig = go.Figure()
                labels = [f"Attempt {i+1}" for i in range(len(s_data))]
                # Math
                fig.add_trace(go.Bar(y=labels, x=s_data['Math Score'], name='Math', orientation='h', marker_color='#0284c7', width=0.4))
                # R&W
                fig.add_trace(go.Bar(y=labels, x=s_data['R&W Score'], name='Reading & Writing', orientation='h', marker_color='rgba(0,0,0,0)', marker_line_color='#0284c7', marker_line_width=2, width=0.4))
                
                # ปรับแกน X (คะแนน) และแกน Y (Attempt)
                fig.update_layout(
                    barmode='group',
                    xaxis=dict(title="คะแนนสอบ", tickvals=[200, 300, 400, 500, 600, 700, 800], range=[200, 800]),
                    yaxis=dict(title="ครั้งที่สอบ (Attempt)", autorange="reversed"),
                    height=500, plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # ปุ่มเลือก Attempt
                st.write("เลือกครั้งที่ต้องการดู:")
                btn_cols = st.columns(len(s_data))
                for i in range(len(s_data)):
                    if btn_cols[i].button(f"At {i+1}", key=f"bt_{i}", type="primary" if i == c_idx else "secondary"):
                        st.session_state.selected_idx = i
                        st.rerun()

            with right:
                st.markdown("<div class='attempt-card'>", unsafe_allow_html=True)
                st.subheader("Attempt Detail")
                st.caption(f"วันที่สอบ: {selected_attempt['Date']}")
                
                # Topics Breakdown
                tab_m, tab_r = st.tabs(["Math Topics", "R&W Topics"])
                with tab_m:
                    m_d = {"Algebra": 'Math Algebra (%)', "Problem Solving": 'Math Problem Solving (%)', "Advanced Math": 'Math Advanced Math (%)', "Additional Topics": 'Math Additional Topics (%)'}
                    for k, v in m_d.items(): st.markdown(f"<div class='topic-box'><span>{k}</span><b>{int(selected_attempt[v])}%</b></div>", unsafe_allow_html=True)
                with tab_r:
                    r_d = {"Craft & Structure": 'R&W Craft & Structure (%)', "Info & Ideas": 'R&W Info & Ideas (%)', "Standard English": 'R&W Standard English (%)', "Expression of Ideas": 'R&W Expression of Ideas (%)'}
                    for k, v in r_d.items(): st.markdown(f"<div class='topic-box'><span>{k}</span><b>{int(selected_attempt[v])}%</b></div>", unsafe_allow_html=True)

                # --- Smart Insight เจาะลึก ---
                st.markdown("<div class='insight-box'>", unsafe_allow_html=True)
                st.markdown("<b style='color: #0369a1;'>💡 Smart Insight โดยพี่สาวใจดี</b>", unsafe_allow_html=True)
                
                # หาหัวข้อที่คะแนนต่ำสุด
                all_topics = {**{k: selected_attempt[v] for k, v in m_d.items()}, **{k: selected_attempt[v] for k, v in r_d.items()}}
                weakest = min(all_topics, key=all_topics.get)
                
                st.markdown(f"""
                <p style='font-size: 13px; color: #0c4a6e; margin-top: 10px;'>
                จากการวิเคราะห์ ครั้งนี้น้องต้องเร่งเสริมหัวข้อ <b>{weakest}</b> เป็นพิเศษนะคะ เพราะคะแนนยังน้อยที่สุดค่ะ
                </p>
                <p style='font-size: 13px; color: #0c4a6e;'><b>ข้อที่ควรทบทวน (Incorrect Analysis):</b></p>
                """, unsafe_allow_html=True)
                
                # ตัวอย่างการจำลองข้อมูลข้อที่ผิด (ในอนาคตดึงจาก Sheet ได้ค่ะ)
                st.markdown("""
                <div class='error-chip'>Q14 (Algebra) - Hard</div>
                <div class='error-chip'>Q19 (Standard English) - Medium</div>
                <div class='error-chip'>Q22 (Advanced Math) - Hard</div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"<p style='font-size: 12px; color: #64748b; margin-top: 10px;'>ขาดอีก {target - int(selected_attempt['Total Score'])} คะแนน จะถึงเป้าหมาย 1500 ค่ะ สู้ๆ นะคะ!</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
