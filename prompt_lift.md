# 🚗 LIFT – Shared Mobility Platform

## 📌 แนวคิดหลัก
LIFT เป็นแพลตฟอร์มแชร์การเดินทางในเขตเมือง ที่ช่วยจับคู่ผู้โดยสารที่มีเส้นทางใกล้เคียงกันแบบเรียลไทม์ พร้อมระบบเปรียบเทียบค่าโดยสารจากผู้ให้บริการต่าง ๆ (เช่น Grab, Bolt, Lineman) โดยมีจุดมุ่งหมายเพื่อลดค่าใช้จ่ายในการเดินทาง, แก้ปัญหารถติด และลด PM2.5

---

## 🎯 เป้าหมายหลัก
- แก้ปัญหาค่าโดยสารที่สูงในเมืองใหญ่
- เพิ่มอัตราการใช้รถร่วมกัน (maximized occupancy)
- ลดมลพิษและเวลาเดินทางในช่วงเวลาเร่งด่วน
- สนับสนุนการเปลี่ยนผ่านสู่ระบบขนส่งแบบยั่งยืน

---

## 👥 กลุ่มเป้าหมาย
- พนักงานออฟฟิศในกรุงเทพฯ ที่ทำงานในย่านที่ไม่ติด BTS/MRT
- เดินทางช่วงเช้า (07:00–09:00) และเย็น (17:00–20:00)
- ต้องการทางเลือกที่ปลอดภัยกว่า ถูกกว่า และประหยัดเวลากว่าการใช้ Grab หรือ Taxi แบบเดี่ยว

---

## 🧩 ฟีเจอร์สำคัญ

### 1. Ride Matching & Fare Splitting
- จับคู่ผู้โดยสารที่มีเส้นทางคล้ายกัน (Route Similarity + Time Window ±10 นาที)
- แบ่งค่าโดยสารอัตโนมัติ
- ใช้ข้อมูลตำแหน่ง GPS และ Google Maps API

### 2. Real-time Fare Comparison
- เปรียบเทียบค่าโดยสารจากผู้ให้บริการ (Grab, Bolt, ฯลฯ)
- จองผ่าน API ของ Third Party แบบ on-demand

### 3. Safety & Trust
- ระบบยืนยันตัวตน (OTP, เบอร์โทร, ชื่อ, ทะเบียนรถ)
- ระบบ Tracking & Emergency Alert (SOS)
- รีวิวผู้ร่วมเดินทาง

### 4. Corporate Ride-Sharing
- รองรับการเดินทางแบบกลุ่มองค์กร
- มีการปรับแต่งเส้นทางและช่วงเวลาให้เหมาะสมกับพนักงาน

---

## 📊 Business Model Canvas (สรุป)
- **Value Proposition:** เดินทางสะดวก ปลอดภัย ประหยัด และเป็นมิตรต่อสิ่งแวดล้อม
- **Revenue:** ค่าธรรมเนียมแพลตฟอร์ม, โฆษณา, Carbon Credit
- **Channels:** Mobile App, Partnership, B2B
- **Customer Segments:** พนักงานออฟฟิศในเมือง, บริษัท, ผู้ใช้รายวัน

---

## 💡 Business Strategy
- **Cost Leadership:** เน้นความประหยัดโดยใช้ระบบจับคู่อัตโนมัติและค่ารถถูกลง
- **Marketing Plan:**
  - Offline: Roadshow, billboard, taxi wrap
  - Online: Facebook, YouTube, Targeted Ads (กลุ่ม ≤30 ปี, รายได้ ≤35,000, อยู่ในกรุงเทพ)

---

## 🧠 Data Strategy Framework

### 1. Data Assets:
- User Profile: เบอร์โทร, บัตร, สถานที่โปรด
- Trip Matching: ต้นทาง-ปลายทาง, จำนวนคน
- Driver API: ทะเบียนรถ, เบอร์, ตำแหน่ง
- Location: GPS real-time

### 2. Data Quality:
- ใช้ regex ตรวจสอบอีเมล, เบอร์, ชื่อ, payment
- ตรวจสอบว่าข้อมูลมี timestamp ที่ถูกต้อง
- ป้องกัน duplicate / fake user

### 3. Data Governance:
- มีนโยบายความเป็นส่วนตัว
- รองรับ PDPA
- กำหนด retention, deletion policy
- มี role & responsibility ชัดเจนในทีม

---

## 🏗️ Data Architecture & Workflow

### Data Pipeline:
1. **Ingestion**: ข้อมูลจากแอป, APIs
2. **Validation**: ตรวจสอบความถูกต้อง
3. **Cleaning**: จัดการ missing/ผิดพลาด
4. **Storage**: ลง S3 / RDMS
5. **Transformation & Analytics**: ETL, Aggregation
6. **ML/AI**: คำนวณจับคู่เส้นทาง, ความต้องการ
7. **Visualization**: Dashboard KPI เช่น CO₂, PM2.5

---

## 🔍 Matching Flow (อัลกอริทึมการจับคู่)

- ตรวจจับความใกล้เคียงของเส้นทาง (route overlap %)
- เปรียบเทียบเวลาเดินทาง (±10 นาที)
- ใช้ Haversine / Route vector / DTW
- Matching Score = route + time + history + preference
- หากทั้ง 2 ฝ่ายยอมรับ → จองผ่าน API

---

## 📈 KPI & OKRs

| Objective | Key Results |
|----------|-------------|
| เพิ่มผู้ใช้ | ≥30,000 ภายใน 3 ปี |
| ความสำเร็จในการจับคู่ | ≥60% ของ ride requests |
| ลด CO₂ | ≥300,000 กม. ลดจากรถคันเดียว |
| ลดต้นทุนผู้โดยสาร | ≥30% จาก Grab |

---

## 💰 Financial Projection

### รายได้:
- Platform fee: 18.45 ล้านบาท/ปี
- โฆษณา: 1.8 ล้านบาท/ปี
- ขาย Carbon Credit: 86,760 บาท/ปี

### ต้นทุน:
- **Development:** 3.41 ล้านบาท
- **Operation (3 ปี):** 10.08 ล้านบาท
- **Cloud Infra (3 ปี):** 3.24 ล้านบาท

---

## 🚧 ความเสี่ยงและแผนรับมือ

| ความเสี่ยง | ระดับ | การจัดการ |
|------------|--------|-------------|
| ความปลอดภัย | สูง | ID verify, SOS, rating |
| การเปลี่ยนนโยบาย 3rd-party | ปานกลาง | มีแผนสำรอง |
| ความเชื่อมั่นของผู้ใช้ | สูง | โปรโมชัน, UX ดี, รีวิวดี |

---

## 💸 Data Monetization
- **DaaS:** เปิด API ข้อมูล real-time
- **Map Insights:** วิเคราะห์ heatmap, demand zone
- **Customer Insight:** ขายข้อมูล B2B สำหรับโฆษณา, loyalty

---

## 🧪 MVP ฟังก์ชันเริ่มต้น
- ระบบจับคู่เส้นทาง + จองรถ
- ระบบแบ่งค่าโดยสารอัตโนมัติ
- ความปลอดภัยพื้นฐาน + รีวิวผู้ใช้งาน


# User Prompt
{{ $json.chatInput }}