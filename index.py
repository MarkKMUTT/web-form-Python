import os
from flask import Flask, render_template, request, redirect, url_for

# กำหนดพาธไปยังโฟลเดอร์ 'templates' โดยย้อนกลับไปที่ Root Folder
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
app = Flask(__name__)

data_records = [] # เก็บข้อมูลเดิม

@app.route('/', methods=['GET', 'POST'])
def index():
    global data_records
    
    if request.method == 'POST':
        
        # 1: ตรวจสอบการกดปุ่ม delete
        delete_index_str = request.form.get('delete_index')
        if delete_index_str is not None:
            try:
                # แปลง index เป็น integer
                delete_index = int(delete_index_str)
                # ลบรายการออกจาก list ตาม index
                if 0 <= delete_index < len(data_records):
                    data_records.pop(delete_index)
            except ValueError:
                # จัดการถ้าค่าที่ส่งมาไม่ใช่ตัวเลข
                pass
            
            # Redirect หลังการลบ
            return redirect(url_for('index'))
        
        # 2: ตรวจสอบการกดปุ่ม input
        elif 'submit' in request.form:
            # รับข้อมูลจาก Form
            date = request.form.get('date')
            line = request.form.get('line')
            model = request.form.get('model')
            qty_str = request.form.get('qty')
            
            # เพิ่มข้อมูลเข้า List
            if date and line and model and qty_str:
                # ตรวจสอบและแปลง QTY เป็น int เพื่อการคำนวณ
                try:
                    qty = int(qty_str)
                    data_records.append({
                        'date': date,
                        'line': line,
                        'model': model,
                        'qty': qty_str
                    })
                except ValueError:
                    # ถ้า QTY ไม่ใช่ตัวเลข ให้ข้ามไป
                    pass
            
            return redirect(url_for('index'))
            
    # แสดงผลหน้า Form และ Table
    total_qty = 0
    for record in data_records:
        try:
            # ใช้ .get() เพื่อป้องกัน Key Error และแปลงเป็น int/float
            total_qty += float(record.get('qty', 0))
        except ValueError:
            # ถ้าค่า qty ไม่ใช่ตัวเลข ให้ถือว่าเป็น 0
            total_qty += 0
            
    # ส่งค่า total_qty ที่คำนวณเสร็จแล้วไปยัง Template
    return render_template('index.html', records=data_records, total_qty_backend=total_qty)

handler = app