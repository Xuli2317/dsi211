import qrcode

# ลิงก์ที่ต้องการสร้าง QR Code
url = "https://docs.google.com/forms/d/1yAVMUg2YXxNbI4Yg7IWY5lgyaoTyBH3dlUoEr7CSEfU/previewResponse"

# สร้าง QR Code
qr = qrcode.QRCode(
    version=1,  # ขนาดของ QR Code (1-40), หรือใช้ None ให้ปรับอัตโนมัติ
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # ความสามารถในการแก้ไขข้อผิดพลาด
    box_size=10,  # ขนาดของแต่ละกล่อง (พิกเซล)
    border=4,  # ความหนาของขอบ
)
qr.add_data(url)
qr.make(fit=True)

# สร้างภาพจาก QR Code
img = qr.make_image(fill_color="black", back_color="white")

# บันทึกเป็นไฟล์รูปภาพ
img.save("qrcode.png")
