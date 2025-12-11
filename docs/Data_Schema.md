# โครงสร้างข้อมูลหลัก: Numerology Meaning Dataset (NM-01)

ไฟล์: `data/processed/numerology_meaning.csv`

| Field Name | Description | Data Type | Required | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **id** | Primary Key สำหรับการ Join | Integer | Yes | Unique ID |
| **number_pair** | คู่เลข 2 หลัก (00-99) | String | Yes | ต้องเป็นตัวเลข 2 หลักเสมอ |
| **meaning_th** | ความหมายหลักของเลขคู่นั้น | String | Yes | สรุปความหมายสั้นๆ |
| **career_fit\_th** | อาชีพที่เหมาะสมที่สุด | String | No | สำหรับการวิเคราะห์อาชีพ |
| **positive\_traits** | ลักษณะด้านบวก (สำหรับ AI Overview) | String | No | |
| **negative\_risks** | ข้อควรระวัง/ความเสี่ยง | String | No | สำหรับข้อจำกัดของเบอร์ |
| **last\_updated** | วันที่อัปเดตข้อมูลล่าสุด | Date | Yes | สำหรับ E-E-A-T Signal |
