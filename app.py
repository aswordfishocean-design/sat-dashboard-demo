import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- 1. การเชื่อมต่อข้อมูล ---
sheet_id = "1qTeQHY74MxOPx_gxXwrkB4pX8bRrqaG4WTox3vHIPVw" 
sheet_name = "SAT%20Information%20Dashboard%20V2"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

@st.cache_data(ttl=600) # พักข้อมูลไว้ 10 นาทีเพื่อความรวดเร็ว
def load_data():
    df = pd.read_csv(url)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"เชื่อมต่อข้อมูลไม่ได้: {e}")
    st.stop()

st.set_page_config(page_title="aims SAT Dashboard", layout="wide")

# --- 2.Sidebar ---
st.sidebar.title("🔐 Login Portal")
role = st.sidebar.selectbox("บทบาทผู้ใช้งาน:", ["Student", "Teacher", "Admin"])

# --- 3. หน้า Students (ปรับปรุงใหม่) ---
if role == "Student":
    student_list = df['Student Name'].unique()
    student_name = st.sidebar.selectbox("เลือกชื่อนักเรียน:", student_list)
    student_data = df[df['Student Name'] == student_name].sort_values('Date')
    
    st.title(f"✨ ยินดีต้อนรับน้อง {student_name}")
    
    # ส่วนสรุปด้านบน (Key Metrics)
    c1, c2, c3, c4 = st.columns(4)
    latest_score = student_data['Total Score'].iloc[-1]
    target = student_data['Target Score'].iloc[0]
    highest = student_data['Highest Score'].iloc[0]
    
    c1.metric("คะแนนล่าสุด", latest_score, f"{latest_score - target if latest_score < target else 0} จากเป้าหมาย")
    c2.metric("เป้าหมาย", int(target))
    c3.metric("คะแนนสูงสุดที่ทำได้", int(highest))
    c4.metric("คอร์สเรียน", student_data['Course Level'].iloc[0])

    st.divider()

    # กราฟที่ 1: พัฒนาการคะแนนรวม (Interactive Line Chart)
    st.subheader("📈 คะแนนรวมย้อนหลัง (Total Score Trend)")
    fig_line = px.line(student_data, x='Date', y='Total Score', markers=True, 
                       text='Total Score', template="plotly_white")
    fig_line.update_traces(textposition="top center", line_color='#2dd4bf')
    st.plotly_chart(fig_line, use_container_width=True)

    # กราฟที่ 2: วิเคราะห์จุดแข็งรายวิชา (Radar Chart)
    st.subheader("🎯 วิเคราะห์ความเชี่ยวชาญแยกตามหัวข้อ (Skill Analysis)")
    st.info("กราฟนี้แสดงเป็นเปอร์เซ็นต์ (%) ยิ่งกว้างแปลว่ายิ่งเก่งในหัวข้อนั้นค่ะ")
    
    latest_test = student_data.iloc[-1]
    
    # เตรียมข้อมูลสำหรับ Radar Chart
    categories_rw = ['Craft & Structure', 'Info & Ideas', 'Standard English', 'Expression of Ideas']
    values_rw = [latest_test['R&W Craft & Structure (%)'], latest_test['R&W Info & Ideas (%)'], 
                 latest_test['R&W Standard English (%)'], latest_test['R&W Expression of Ideas (%)']]
    
    categories_math = ['Algebra', 'Problem Solving', 'Advanced Math', 'Additional Topics']
    values_math = [latest_test['Math Algebra (%)'], latest_test['Math Problem Solving (%)'], 
                   latest_test['Math Advanced Math (%)'], latest_test['Math Additional Topics (%)']]

    col_a, col_b = st.columns(2)
    
    with col_a:
        fig_rw = go.Figure(data=go.Scatterpolar(r=values_rw, theta=categories_rw, fill='toself', name='R&W'))
        fig_rw.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), title="Reading & Writing Breakdown")
        st.plotly_chart(fig_rw, use_container_width=True)
        
    with col_b:
        fig_math = go.Figure(data=go.Scatterpolar(r=values_math, theta=categories_math, fill='toself', name='Math', fillcolor='rgba(255, 212, 59, 0.5)'))
        fig_math.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), title="Math Breakdown")
        st.plotly_chart(fig_math, use_container_width=True)

    # ตารางสรุปผลสอบ
    with st.expander("📝 ดูประวัติผลสอบทั้งหมด"):
        st.table(student_data[['Date', 'Test Form', 'Total Score', 'Math Score', 'R&W Score']])

# --- 4. หน้า Teacher & Admin ---
else:
    st.title(f"🛠️ ระบบ {role} (Under Construction)")
    st.write("ข้อมูลดิบจาก Google Sheet:")
    st.dataframe(df)
