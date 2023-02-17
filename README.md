# ติดตั้งโปรเจ็กต์ djangShopping โดยใช้คำสั่ง git clone https://github.com/phphich/djangShopping.git
# ติดตั้ง Package ต่าง ๆ ของโปรเจ็กต์ โดยใช้คำสั่ง pip install -r requirements.txt
# Log in เข้า mySQL โดยใช้ root 
# สร้างฐานข้อมูลใน mySQL ชื่อ dbtest
# สร้าง user ชื่อ bisdev พร้อมกำหนด รหัสผ่าน 12345 หรือชื่อและรหัสผ่านตามที่ต้องการก็ได้ 
# ให้สิทธิ์การเข้าถึงฐานข้อมูล dbtest แก่ bisdev
# กำหนดค่าในไฟล์ setting.py ในส่วนของ DATABASE โดยระบุค่าชื่อฐานข้อมูล, ชื่อผู้ใช้, รหัสผ่าน ให้ตรงกับที่สร้างไว้ในฐานข้อมูล 
# ใช้คำสั่ง  python manage.py migrate เพื่อสร้างตารางข้อมูลใน mySQL,  และ python manage.py createuperuser เพื่อสร้างบัญชีผู้ดูแลระบบ 
# ใช้คำสั่ง python manage.py runserver 0.0.0.0:80
# เปิด browser ไปที่ localhost
# เพิ่มพนักงานงานในเมนู Employee (เข้าไปครั้งแรก ระบบจะบังคับให้เพิ่ม Employee 1 คน ทันที)
# สมัครสมาชิกที่เมนู Customer Registation
# ทดสอบสั่งซื้อสินค้าและอื่น ๆ
