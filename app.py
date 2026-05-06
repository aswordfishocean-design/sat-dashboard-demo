import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 1. จำลองฐานข้อมูล (ดึงมาจาก Google Sheet ที่เราออกแบบไว้)
# ---------------------------------------------------------
data = {
    'Date': ['2026-04-20', '2026-04-21', '2026-04-20', '2026-04-21'],
    'Student Name': ['Aphiphongphiphut', 'Aphiphongphiphut', 'Pharin', 'Pharin'],
    'Course Level': ['SAT Camp', 'SAT Camp', 'Builder', 'Builder'],
    'Target Score': [1400, 1400, 1200, 1200],
    'Highest Score': [1220, 1220, 1070, 1070],
    'Total Score': [1220, 1210, 900, 1070],
    'R&W Score': [580, 610, 480, 580],
    'Math Score': [640, 600, 420, 490]
}
df = pd.DataFrame(data)

# ตั้งค่าหน้าจอ Web App
st.set_page_config(page_title="SAT Information Dashboard", layout="wide")

# ---------------------------------------------------------
# 2. หน้า Log in (จำลองการเลือกสิทธิ์การเข้าใช้งาน)
# ---------------------------------------------------------
st.sidebar.title("Log in")
role = st.sidebar.radio("เข้าสู่ระบบในฐานะ:", ["Student", "Teacher", "Admin"])

# ---------------------------------------------------------
# 3. หน้า Students / Parents
# ---------------------------------------------------------
if role == "Student":
    # สมมติว่าระบบรู้ว่านักเรียนที่ล็อกอินคือใคร
    student_name = st.sidebar.selectbox("จำลองอีเมลที่ล็อกอิน:", df['Student Name'].unique())
    student_data = df[df['Student Name'] == student_name]
    
    st.title(f"📊 Dashboard ของน้อง {student_name}")
    st.write(f"**คอร์สที่กำลังเรียน:** {student_data['Course Level'].iloc[0]}")
    
    # แสดงเป้าหมายและคะแนนสูงสุด
    col1, col2 = st.columns(2)
    col1.metric("🎯 เป้าหมายคะแนน (Target)", f"{student_data['Target Score'].iloc[0]}")
    col2.metric("🏆 คะแนนที่ดีที่สุด (Highest)", f"{student_data['Highest Score'].iloc[0]}")
    
    st.divider()
    
    # กราฟแท่งแสดงคะแนนรวมแต่ละครั้ง
    st.subheader("📈 พัฒนาการคะแนน (Total Score)")
    st.bar_chart(student_data.set_index('Date')['Total Score'])
    
    # แสดงรายละเอียด Performance in Details (เมื่ออยากดูเจาะลึก)
    with st.expander("🔍 ดูรายละเอียด Performance in Details แยกรายวิชา"):
        st.dataframe(student_data[['Date', 'Total Score', 'R&W Score', 'Math Score']], use_container_width=True)

# ---------------------------------------------------------
# 4. หน้า Teachers
# ---------------------------------------------------------
elif role == "Teacher":
    st.title("👩‍🏫 Teacher Dashboard")
    
    # เลือกคอร์สและนักเรียน
    course = st.selectbox("เลือกคอร์สที่สอน (Courses):", ["Builder", "Mastery", "SAT Camp", "Final Boost", "SAT Blue Print Workshop"])
    
    # กรองเฉพาะนักเรียนในคอร์สนั้น
    course_data = df[df['Course Level'] == course]
    
    if not course_data.empty:
        student_to_view = st.selectbox("เลือกนักเรียนเพื่อดูข้อมูล:", course_data['Student Name'].unique())
        st.write("ข้อมูลคะแนนล่าสุด:")
        st.dataframe(course_data[course_data['Student Name'] == student_to_view], use_container_width=True)
        
        # ช่องพิมพ์ Comment สั่งการบ้านหรือข้อแนะนำ
        st.subheader("📝 Teacher's Comments & Objectives")
        comment = st.text_area(f"พิมพ์ข้อเสนอแนะสำหรับ {student_to_view}:")
        if st.button("ส่ง Comment"):
            st.success("บันทึก Comment ลงฐานข้อมูลเรียบร้อยแล้ว!")
    else:
        st.info("ยังไม่มีข้อมูลนักเรียนในคอร์สนี้")

# ---------------------------------------------------------
# 5. หน้า Admin
# ---------------------------------------------------------
elif role == "Admin":
    st.title("⚙️ Admin Panel")
    st.subheader("ระบบจัดการผู้ใช้งาน (User Management)")
    
    # ตารางจำลองข้อมูล User
    st.dataframe(df[['Student Name', 'Course Level', 'Target Score']].drop_duplicates(), use_container_width=True)
    
    # ปุ่มจัดการ
    col1, col2, col3 = st.columns(3)
    col1.button("➕ เพิ่มนักเรียน/ครู (Add User)")
    col2.button("🔑 รีเซ็ตรหัสผ่าน (Reset Password)")
    col3.button("🗑️ ลบผู้ใช้งาน (Delete User)")
