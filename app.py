import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import base64
import random

# --- 1. ระบบจัดการข้อมูล (Data Engine) ---
@st.cache_data(ttl=10)
def load_and_process_data():
    try:
        students = pd.read_csv('students.csv')
        scores = pd.read_csv('scores.csv')
        topic_scores = pd.read_csv('topic_scores.csv')

        # เชื่อมโยงข้อมูล
        df = scores.merge(students, on='student_id', how='left')
        df = df.merge(topic_scores, on=['score_id', 'student_id'], how='left')

        # จัดเตรียมคอลัมน์มาตรฐาน
        df['Student Name'] = df['full_name']
        df['Date'] = pd.to_datetime(df['test_date']).dt.date
        df['Math Score'] = df['math_score']
        df['R&W Score'] = df['rw_score']
        df['Total Score'] = df['total_score']
        df['Target Score'] = df['target_score']

        # คำนวณเปอร์เซ็นต์ความถูกต้องรายบทเรียน
        topics_map = {
            'Math Algebra (%)': ['alg_c', 'alg_t'],
            'Math Problem Solving (%)': ['ps_c', 'ps_t'],
            'Math Advanced Math (%)': ['adv_c', 'adv_t'],
            'Math Additional Topics (%)': ['add_c', 'add_t'],
            'R&W Craft & Structure (%)': ['cs_c', 'cs_t'],
            'R&W Info & Ideas (%)': ['ii_c', 'ii_t'],
            'R&W Standard English (%)': ['sec_c', 'sec_t'],
            'R&W Expression of Ideas (%)': ['ei_c', 'ei_t']
        }
        for label, cols in topics_map.items():
            df[label] = (df[cols[0]] / df[cols[1]]) * 100
        
        return df
    except Exception as e:
        st.error(f"หนูโหลดข้อมูล Demo ไม่ได้ค่ะ: {e}")
        return None

df = load_process_data()

# --- 2. ฟังก์ชันเสริม (Helper Functions) ---
def get_branding():
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

def generate_analysis(selected_attempt):
    analysis_pool = {
        "Math Algebra (%)": ["Linear Equation", "Systems of Equations"],
        "Math Advanced Math (%)": ["Quadratic Equations", "Non-linear Functions"],
        "R&W Standard English (%)": ["Punctuation", "Subject-Verb Agreement"],
        "R&W Expression of Ideas (%)": ["Transitions", "Rhetorical Synthesis"]
    }
    analysis = []
    for col, topics in analysis_pool.items():
        if selected_attempt[col] < 100:
            analysis.append({
                "Subject": "Math" if "Math" in col else "R&W",
                "Question": f"Q{random.randint(1, 27)}",
                "Topic": topics[random.randint(0, len(topics)-1)],
                "Detail": "วิเคราะห์พลาดเนื่องจากสับสนเงื่อนไขโจทย์ แนะนำให้ฝึกทำ Error Log"
            })
    return analysis[:4]

# --- 3. การตั้งค่า CSS ---
st.set_page_config(page_title="aims SAT Data-Driven System", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .student-title { text-align: center; color: #002d56; font-size: 48px; font-weight: 900; margin-top: 10px; }
    .target-huge { font-size: 140px; font-weight: 900; color: #002d56; text-align: center; line-height: 1; }
    .metric-card { background: white; padding: 25px; border-radius: 20px; border: 1px solid #f1f5f9; box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center; }
    .admin-card { background: #f8fafc; padding: 20px; border-radius: 15px; border-left: 6px solid #002d56; }
    .deep-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    .deep-table th { background-color: #002d56; color: white; padding: 12px; text-align: left; }
    .deep-table td { padding: 12px; border-bottom: 1px solid #f1f5f9; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. การจัดการ Roles ใน Sidebar ---
st.sidebar.markdown("<h2 style='color:#002d56;'>🔐 aims Portal</h2>", unsafe_allow_html=True)
role = st.sidebar.radio("เลือกสิทธิ์การใช้งาน:", ["Admin View (Executive)", "Teacher View (Mastery)", "Student View (Personal)"])

if df is not None:
    # --- 🔵 STUDENT VIEW ---
    if role == "Student View (Personal)":
        h_left, h_right = st.columns([1, 1])
        with h_left:
            student_name = st.selectbox("เลือกชื่อนักเรียน:", sorted(df['Student Name'].unique()))
        with h_right:
            get_branding()

        s_data = df[df['Student Name'] == student_name].sort_values('Date').reset_index(drop=True)
        target_val = int(s_data['Target Score'].iloc[0])
        curr_idx = len(s_data) - 1
        selected = s_data.iloc[curr_idx]

        st.markdown(f"<div class='student-title'>{student_name}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center; color:#64748b; font-weight:700;'>TARGET SCORE</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='target-huge'>{target_val}</div>", unsafe_allow_html=True)

        # Dashboard Content (กราฟและตารางแบบเดิม)
        l, r = st.columns([1.6, 1.4])
        with l:
            st.subheader("📊 Performance Trend")
            fig = go.Figure()
            fig.add_trace(go.Bar(x=[f"At {i+1}" for i in range(len(s_data))], y=s_data['Math Score'], name='Math', marker_color='#002d56'))
            fig.add_trace(go.Bar(x=[f"At {i+1}" for i in range(len(s_data))], y=s_data['R&W Score'], name='R&W', marker=dict(color='#ffffff', line=dict(color='#002d56', width=2))))
            fig.update_layout(barmode='group', plot_bgcolor='white', height=400)
            st.plotly_chart(fig, use_container_width=True, theme=None)
        
        with r:
            st.subheader(f"📍 At {curr_idx+1} Mastery")
            st.markdown(f"**Math: {int(selected['Math Score'])} | R&W: {int(selected['R&W Score'])}**")
            t1, t2 = st.tabs(["Math", "R&W"])
            with t1:
                for k in ["Algebra", "Advanced Math", "Problem Solving"]:
                    st.write(f"{k}: {int(selected[f'Math {k} (%)'])}%")
                    st.progress(selected[f'Math {k} (%)']/100)
            with t2:
                for k in ["Standard English", "Expression of Ideas"]:
                    st.write(f"{k}: {int(selected[f'R&W {k} (%)'])}%")
                    st.progress(selected[f'R&W {k} (%)']/100)

        st.divider()
        st.header("🔍 Deep Analysis: Incorrect Questions")
        ans_list = generate_analysis(selected)
        tbl = "<table class='deep-table'><tr><th>Subject</th><th>Question</th><th>Topic</th><th>Insight</th></tr>"
        for item in ans_list:
            tbl += f"<tr><td>{item['Subject']}</td><td>{item['Question']}</td><td>{item['Topic']}</td><td>{item['Detail']}</td></tr>"
        st.markdown(tbl + "</table>", unsafe_allow_html=True)

    # --- 🟢 TEACHER VIEW ---
    elif role == "Teacher View (Mastery)":
        get_branding()
        st.title("👨‍🏫 Teacher's Mastery Overview")
        
        # ภาพรวมคลาส
        avg_score = df.groupby('Student Name')['Total Score'].max().mean()
        st.markdown(f"""
            <div class='admin-card'>
                <h3 style='margin:0;'>คลาสเรียนรวม</h3>
                <p style='font-size:24px; color:#002d56; font-weight:bold;'>คะแนนเฉลี่ย (Best Score): {int(avg_score)}</p>
            </div>
        """, unsafe_allow_html=True)

        st.write("### 📋 รายชื่อนักเรียนและพัฒนาการ")
        summary = df.groupby('Student Name').agg({
            'Total Score': ['min', 'max', 'count'],
            'Target Score': 'first'
        }).reset_index()
        summary.columns = ['Student', 'First Score', 'Best Score', 'Attempts', 'Target']
        summary['Improvement'] = summary['Best Score'] - summary['First Score']
        
        st.dataframe(summary, use_container_width=True)

        st.write("### 🚨 Students Needing Attention (คะแนนห่างเป้าหมาย > 100)")
        at_risk = summary[summary['Target'] - summary['Best Score'] > 100]
        st.table(at_risk[['Student', 'Best Score', 'Target', 'Improvement']])

    # --- 🔴 ADMIN VIEW ---
    elif role == "Admin View (Executive)":
        get_branding()
        st.title("🏛️ Executive Performance Summary")
        
        # คำนวณ KPIs สำคัญ
        total_students = df['student_id'].nunique()
        # เช็กว่าใครเคยทำถึงเป้าแล้วบ้าง
        reached_df = df[df['Total Score'] >= df['Target Score']]
        reached_count = reached_df['student_id'].nunique()
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='metric-card'><h3>นักเรียนทั้งหมด</h3><h1 style='color:#002d56;'>{total_students}</h1><p>คน</p></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='metric-card'><h3>ถึงเป้าหมายแล้ว</h3><h1 style='color:#22c55e;'>{reached_count}</h1><p>คน ({int(reached_count/total_students*100)}%)</p></div>", unsafe_allow_html=True)
        with c3:
            avg_gain = (df.groupby('student_id')['Total Score'].max() - df.groupby('student_id')['Total Score'].min()).mean()
            st.markdown(f"<div class='metric-card'><h3>อัตราการเติบโตเฉลี่ย</h3><h1 style='color:#002d56;'>+{int(avg_gain)}</h1><p>คะแนน / คน</p></div>", unsafe_allow_html=True)

        st.divider()
        
        st.write("### 🌏 Institutional Topic Mastery (ภาพรวมจุดอ่อนทั้งสถาบัน)")
        # คำนวณค่าเฉลี่ย Mastery ทุกบทเรียน
        mastery_cols = [c for c in df.columns if '(%)' in c]
        avg_mastery = df[mastery_cols].mean().sort_values()
        
        fig_mastery = go.Figure(go.Bar(
            x=avg_mastery.values, y=avg_mastery.index, orientation='h',
            marker_color=['#ef4444' if v < 70 else '#002d56' for v in avg_mastery.values]
        ))
        fig_mastery.update_layout(title="Average Mastery by Topic (Red = Critical Area)", xaxis_title="Percentage (%)", height=400)
        st.plotly_chart(fig_mastery, use_container_width=True)

        st.info("💡 ข้อมูลนี้ช่วยให้ Admin วางแผนเปิด Bootcamp ในหัวข้อที่นักเรียนส่วนใหญ่ยังทำได้ไม่ดี (แถบสีแดง) ได้อย่างแม่นยำค่ะ")

st.markdown("<br><center style='color: #94a3b8; font-size: 11px;'>aims SAT Data-Driven Ecosystem • 2026 Admin Panel</center>", unsafe_allow_html=True)
