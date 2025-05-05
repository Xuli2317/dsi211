from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import csv

# ตั้งค่า Chrome ให้เด้งเปิด
options = Options()
options.add_argument('--start-maximized')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

data = []

try:
    # เปิด Lazada แล้ว search โยเกิร์ต
    driver.get("https://www.lazada.co.th/")
    time.sleep(2)
    search = driver.find_element(By.CSS_SELECTOR, 'input[name="q"]')
    search.send_keys("โยเกิร์ต")
    search.submit()
    time.sleep(5)
    print("🔍 ทำการค้นหาคำว่า 'โยเกิร์ต'")

    # Scroll the page to load more results
    for _ in range(5):  # Scroll 5 times to load more products
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)

    # ดึงทุกการ์ดสินค้าจากผลลัพธ์
    cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-qa-locator="product-item"]')
    print(f"พบ {len(cards)} การ์ดสินค้า")

    # Process only the first 10 cards
    for index, card in enumerate(cards[:10], 1):
        try:
            print(f"\n🔑 กำลังดึงข้อมูลจากการ์ดที่ {index} ...")

            # ชื่อสินค้า: tag <a> ใน div.RfADt
            title = card.find_element(By.CSS_SELECTOR, 'div.RfADt a').get_attribute('title').strip()

            # ราคา: span.ooOxS
            price = card.find_element(By.CSS_SELECTOR, 'span.ooOxS').text.strip()

            # จำนวนยอดขาย: span ใน div._6uN7R > span._1cEkb > span
            try:
                sales = card.find_element(By.CSS_SELECTOR, 'div._6uN7R span._1cEkb span').text.strip()
            except:
                sales = "ไม่พบยอดขาย"

            # เพิ่มข้อมูลลงใน list
            data.append([title, price, sales])

            # คลิกที่การ์ดเพื่อเข้าไปดูรายละเอียด (ใช้ลิงค์ใน tag <a>)
            card_link = card.find_element(By.CSS_SELECTOR, 'div.RfADt a')
            card_link.click()
            print(f"🔗 กำลังเข้าไปดูรายละเอียดของสินค้า: {title}")

            # รอโหลดหน้าใหม่
            time.sleep(3)

            # กลับไปยังหน้าผลลัพธ์ (ย้อนกลับไปยังหน้าหลัก)
            driver.back()
            print("⏪ กลับไปยังหน้าผลลัพธ์")

            # รอให้โหลดหน้ากลับมา
            time.sleep(3)

        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการ์ด {index}: {e}")

finally:
    driver.quit()

# บันทึกลง CSV
with open('yogurt_data.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['ชื่อสินค้า', 'ราคา', 'จำนวนยอดขาย'])
    writer.writerows(data)

print(f"✅ บันทึกข้อมูลเรียบร้อย: yogurt_data.csv ({len(data)} รายการ)")
