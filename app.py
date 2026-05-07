import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. ข้อมูลดิบ (อ้างอิงตาม 5 Attempts ในรูปของพี่มหา) ---
attempts_data = [
    {"id": "A1", "label": "Attempt 1", "date": "Apr 20, 2026", "rw": 580, "math": 640, "total": 1220},
    {"id": "A2", "label": "Attempt 2", "date": "Apr 21, 2026", "rw": 610, "math": 600, "total": 1210},
    {"id": "A3", "label": "Attempt 3", "date": "Apr 22, 2026", "rw": 580, "math": 640, "total": 1220},
    {"id": "A4", "label": "Attempt 4", "date": "Apr 23, 2026", "rw": 600, "math": 570, "total": 1170},
    {"id": "A5", "label": "Attempt 5", "date": "Apr 24, 2026", "rw": 620, "math": 720, "total": 1340},
]
# ข้อมูลเจาะลึกของ Attempt 5 (ล่าสุด)
latest_topics = {
    "rw": [
        {"name": "Craft & Structure", "score": "10/12", "pct": 83},
        {"name": "Information & Ideas", "score": "14/16", "pct": 88},
        {"name": "Standard English Conventions", "score": "10/14", "pct": 71},
        {"name": "Expression of Ideas", "score": "9/12", "pct": 75},
    ]
}

# --- 2. ตั้งค่าหน้าตาแอป (Theme Blue/White) ---
st.set_page_config(page_title="aims SAT Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f9ff; }
    .stMetric { background-color: white; padding: 20px; border-radius: 20px; border: 1px solid #e0f2fe; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    .attempt-card { background-color: white; padding: 20px; border-radius: 20px; border: 1px solid #e0f2fe; }
    .topic-row { display: flex; justify-content: space-between; align-items: center; padding: 10px; border: 1px solid #f1f5f9; border-radius: 10px; margin-bottom: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Header & Metrics ---
st.markdown("<div style='display: flex; align-items: center; gap: 10px;'><span style='background-color: #0284c7; color: white; padding: 4px 12px; border-radius: 20px; font-size: 14px; font-weight: bold;'>Digital SAT</span><span style='color: #64748b; font-size: 14px;'>Performance Report</span></div>", unsafe_allow_html=True)
st.title("Aphiphongphiphut Kaweeyarn")
st.markdown("<p style='color: #64748b;'>Target Score: <b>1500</b></p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("✨ Latest Score", "1340", "Attempt 5 • Apr 24, 2026")
with col2:
    st.metric("🏆 Best Score Achieved", "1340", "Attempt 5 • Apr 24, 2026")
with col3:
    gap = 1500 - 1340
    st.metric("🎯 Progress to Target", "89%", f"Gap: {gap}")
    st.progress(0.89)

st.divider()

# --- 4. Main Content Layout ---
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("Score Trend (Click a bar to inspect)")
    st.caption("X-axis: 200–800 scale • Y-axis: attempts")
    
    # สร้างกราฟแท่งแนวนอน (Horizontal Bar Chart)
    fig = go.Figure()
    
    # Math Bar (สีฟ้าเข้ม)
    fig.add_trace(go.Bar(
        y=[a['label'] + f" ({a['date']})" for a in attempts_data],
        x=[a['math'] for a in attempts_data],
        name='Math',
        orientation='h',
        marker=dict(color='#0284c7', line=dict(color='#0284c7', width=1)),
        width=0.4
    ))
    
    # R&W Bar (แท่งโปร่งขอบฟ้า)
    fig.add_trace(go.Bar(
        y=[a['label'] + f" ({a['date']})" for a in attempts_data],
        x=[a['rw'] for a in attempts_data],
        name='Reading & Writing',
        orientation='h',
        marker=dict(color='rgba(0,0,0,0)', line=dict(color='#0284c7', width=2)),
        width=0.4
    ))

    fig.update_layout(
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[200, 800], gridcolor='#f1f5f9', dtick=100),
        yaxis=dict(autorange="reversed"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=30, b=0),
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # ปุ่มเลือก Attempt ด้านล่างกราฟ
    st.write(" ")
    cols = st.columns(len(attempts_data))
    for i, a in enumerate(attempts_data):
        cols[i].button(a['label'], key=a['id'], use_container_width=True)

with right_col:
    with st.container():
        st.markdown("<div class='attempt-card'>", unsafe_allow_html=True)
        st.subheader("Attempt Detail")
        st.caption("Click any bar to switch subject & attempt.")
        
        # ส่วนหัวของ Card
        c_a, c_b = st.columns([2, 1])
        c_a.markdown("**Attempt 5**<br><span style='color: #64748b;'>Apr 24, 2026</span>", unsafe_allow_html=True)
        c_b.markdown("<span style='background-color: #e0f2fe; color: #0369a1; padding: 4px 10px; border-radius: 20px; font-weight: bold;'>Total 1340</span>", unsafe_allow_html=True)
        
        # คะแนนแยกวิชา
        s1, s2 = st.columns(2)
        s1.markdown("<div style='border: 1px solid #e2e8f0; padding: 10px; border-radius: 15px;'> <span style='font-size: 12px; color: #64748b;'>Math</span><br><b style='font-size: 20px;'>720</b><br><span style='font-size: 12px; color: #0284c7;'>Strong</span> </div>", unsafe_allow_html=True)
        s2.markdown("<div style='border: 1px solid #e2e8f0; padding: 10px; border-radius: 15px;'> <span style='font-size: 12px; color: #64748b;'>R&W</span><br><b style='font-size: 20px;'>620</b><br><span style='font-size: 12px; color: #0284c7;'>Developing</span> </div>", unsafe_allow_html=True)
        
        # Tabs สำหรับ Breakdown
        t1, t2 = st.tabs(["Math", "R&W"])
        with t2: # ตัวอย่างแสดง R&W ตามรูป
            st.markdown("<div style='display: flex; justify-content: space-between;'><b>Topic Breakdown</b> <span style='background-color: #0284c7; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px;'>80%</span></div>", unsafe_allow_html=True)
            st.caption("Correct 43/54")
            
            for topic in latest_topics['rw']:
                st.markdown(f"""
                    <div class='topic-row'>
                        <span style='font-size: 13px;'>{topic['name']}</span>
                        <span style='font-size: 13px;'><b>{topic['score']}</b> <span style='color: #64748b; font-weight: bold;'>{topic['pct']}%</span></span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div style='background-color: #f0f9ff; padding: 15px; border-radius: 15px; margin-top: 15px;'><b style='color: #0369a1;'>ℹ️ Smart Insight</b><p style='font-size: 13px; color: #0c4a6e; margin-top: 5px;'>Best total score is <b>1340</b>. To reach target <b>1500</b>, student needs <b>160</b> more points.</p></div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><div style='text-align: center; color: #94a3b8; font-size: 12px;'>Prototype UI • Clean Blue/White Theme • Clickable Interactive Report</div>", unsafe_allow_html=True)
