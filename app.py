import streamlit as st
import sqlite3
import pandas as pd

# ตั้งค่าหน้าตาของเว็บสำหรับสมาร์ทโฟน/แท็บเล็ต
st.set_page_config(page_title="ระบบสืบค้นคู่ผสมพันธุ์โค", layout="centered")

st.title("🐄 ระบบสืบค้นคู่ผสมพันธุ์โค")

# รายชื่อพ่อพันธุ์ทั้งหมดในตาราง
SIRE_LIST = ['TH519', 'TH518', 'TH517', 'TH514', 'TH513', 'TH512', 'TH510', 'TH520', 'TH521', 'TH523']

# ฟังก์ชันดึงข้อมูลจาก SQLite
def search_mating(dam_id, sire_id):
    conn = sqlite3.connect('mating_data.db')
    # ดึงค่า SireId_MinInb (พ่อพันธุ์ที่แนะนำ) และค่าจากคอลัมน์พ่อโคที่เลือก (จุดตัด)
    query = f"SELECT SireId_MinInb, {sire_id} FROM sim_matings WHERE DamId = ?"
    df = pd.read_sql_query(query, conn, params=(dam_id,))
    conn.close()
    return df

# ส่วนรับข้อมูลจากเจ้าหน้าที่
st.subheader("🔎 ระบุข้อมูลการสืบค้น")
dam_input = st.text_input("หมายเลขแม่โค (DamId):", placeholder="เช่น 22570365").strip()
sire_input = st.selectbox("เลือกหมายเลขพ่อโค (SireId):", SIRE_LIST)

if st.button("สืบค้นข้อมูล", type="primary"):
    if not dam_input:
        st.warning("กรุณากรอกหมายเลขแม่โค (DamId)")
    else:
        result = search_mating(dam_input, sire_input)
        
        if not result.empty:
            recommended_sire = result.iloc[0]['SireId_MinInb']
            intersection_val = result.iloc[0][sire_input]
            
            st.divider()
            st.success("พบข้อมูลการสืบค้น")
            
            # แสดงผลลัพธ์ในรูปแบบการ์ดเน้นข้อความ
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    label="พ่อพันธุ์ที่แนะนำ (SireId_MinInb)", 
                    value=str(recommended_sire)
                )
                
            with col2:
                st.metric(
                    label=f"ค่าจุดตัด ({sire_input})", 
                    value=f"{intersection_val:.6f}" if isinstance(intersection_val, (float, int)) else str(intersection_val)
                )
        else:
            st.error(f"ไม่พบข้อมูลหมายเลขแม่โค '{dam_input}' ในระบบ")