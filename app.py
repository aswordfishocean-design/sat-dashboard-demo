import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 1. เชื่อมต่อฐานข้อมูลจาก Google Sheet (ข้อมูลจริงของพี่มหา)
# ---------------------------------------------------------
# ข้อมูลจากไฟล์ V2 ที่น้องใจดีสร้างให้ค่ะ [cite: 16]
sheet_id = "1qTeQHY74MxOPx_gxXwrkB4pX8bRrqaG4WTox3vHIPVw" 
sheet_name = "SAT%20Information%20Dashboard%20V2"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# ดึงข้อมูลมาเป็น DataFrame
try:
    df = pd.read_csv(url)
    # แปลงคอลัมน์วันที่ให้เป็นรูปแบบที่ใช้งานง่าย
    df['Date'] = pd.to_datetime(df['Date']).dt.date
except Exception as e:
    st.error(f"ไม่สามารถเชื่อมต่อข้อมูลได้: {e}")
    st.stop()

# ตั้งค่าหน้าจอ Web App
st.set_page_config(page_title="SAT Information Dashboard", layout="wide")

# ---------------------------------------------------------
# 2. ระบบ Log-in (จำลองการเลือกสิทธิ์)
# ---------------------------------------------------------
st.sidebar.title("🔐 Log in")
role = st.sidebar.radio("เข้าสู่ระบบในฐานะ:", ["Student", "Teacher", "Admin"])

# ---------------------------------------------------------
# 3. หน้า Students / Parents
# ---------------------------------------------------------
if role == "Student":
    # ให้นักเรียนเลือกชื่อตัวเอง (จำลองระบบล็อกอินด้วยอีเมล)
    student_list = df['Student Name'].unique()
    student_name = st.sidebar.selectbox("จำลองชื่อนักเรียนที่ล็อกอิน:", student_list)
    
    # กรองข้อมูลเฉพาะของนักเรียนคนนั้น
    student_data = df[df['Student Name'] == student_name].sort_values('Date')
    
    st.title(f"📊 Dashboard ของน้อง {student_name}")
    st.write(f"**คอร์สเรียน:** {student_data['Course Level'].iloc[0]}")
    
    # แสดงเป้าหมายและคะแนนสูงสุด (ดึงจาก Sheet จริง) [cite: 16]
    col1, col2 = st.columns(2)
    col1.metric("🎯 เป้าหมายคะแนน (Target)", f"{int(student_data['Target Score'].iloc[0])}")
    col2.metric("🏆 คะแนนที่ดีที่สุด (Highest)", f"{int(student_data['Highest Score'].iloc[0])}")
    
    st.divider()
    
    # กราฟแท่งแสดงพัฒนาการคะแนนรวม
    st.subheader("📈 พัฒนาการคะแนนรวม (Total SAT Score)")
    st.bar_chart(student_data.set_index('Date')['Total Score'])
    
    # เจาะลึกรายวิชา
    with st.expander("🔍 ดูรายละเอียด Performance in Details (Math vs R&W)"):
        chart_data = student_data[['Date', 'Math Score', 'R&W Score']].set_index('Date')
        st.line_chart(chart_data)
        st.dataframe(student_data[['Date', 'Total Score', 'Math Score', 'R&W Score']], use_container_width=True)

# ---------------------------------------------------------
# 4. หน้า Teachers
# ---------------------------------------------------------
elif role == "Teacher":
    st.title("👩‍🏫 Teacher Dashboard")
    
    # เลือกดูตามคอร์สเรียน
    course_list = df['Course Level'].unique()
    course = st.selectbox("เลือกคอร์สที่ต้องการติดตาม:", course_list)
    
    # กรองข้อมูลนักเรียนในคอร์สนั้น
    course_data = df[df['Course Level'] == course]
    
    if not course_data.empty:
        student_to_view = st.selectbox("เลือกรายชื่อนักเรียน:", course_data['Student Name'].unique())
        st.write(f"**ตารางสรุปผลสอบของน้อง {student_to_view}:**")
        st.dataframe(course_data[course_data['Student Name'] == student_to_view], use_container_width=True)
        
        # ช่องสำหรับพิมพ์คอมเมนต์
        st.subheader("📝 ให้คำแนะนำเพิ่มเติม (Objectives)")
        st.text_area(f"พิมพ์ข้อความถึง {student_to_view}:")
        st.button("ส่งข้อมูล")
    else:
        st.info("ยังไม่มีข้อมูลนักเรียนในระดับนี้")

# ---------------------------------------------------------
# 5. หน้า Admin
# ---------------------------------------------------------
elif role == "Admin":
    st.title("⚙️ Admin Control Panel")
    st.subheader("จัดการฐานข้อมูลผู้ใช้งานและผลสอบ")
    
    # แสดงข้อมูลทั้งหมดในระบบ
    st.write("ข้อมูลภาพรวมทั้งหมดใน Google Sheet:")
    st.dataframe(df, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("➕ เพิ่มข้อมูลนักเรียนใหม่")
        st.button("🔑 จัดการรหัสผ่าน")
    with col2:
        st.button("💾 สำรองข้อมูล (Backup)")
        st.button("🗑️ ลบข้อมูลที่ผิดพลาด")
