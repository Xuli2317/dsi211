from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import csv

# ตั้งค่า Chrome
options = Options()
options.add_argument('--start-maximized')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

data = []

try:
    driver.get("https://www.lazada.co.th/")
    time.sleep(2)

    search = driver.find_element(By.CSS_SELECTOR, 'input[name="q"]')
    search.send_keys("โยเกิร์ต")
    search.submit()
    time.sleep(5)
    print("🔍 ค้นหาคำว่า 'โยเกิร์ต'")

    # Scroll เพื่อโหลดสินค้าทั้งหมด
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, 1500);")
        time.sleep(2)

    # ดึงรายการการ์ดสินค้า
    cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-qa-locator="product-item"]')
    print(f"📦 พบสินค้าทั้งหมด {len(cards)} รายการ")

    # เก็บลิงก์สินค้า
    product_links = []
    for card in cards:
        try:
            link = card.find_element(By.CSS_SELECTOR, 'div.RfADt a').get_attribute('href')
            product_links.append(link)
        except:
            continue

    print(f"🔗 เก็บลิงก์สำเร็จ {len(product_links)} รายการ")

    # เข้าแต่ละลิงก์เพื่อดึงข้อมูล
    for index, link in enumerate(product_links, 1):
        try:
            driver.get(link)
            print(f"\n➡️ [{index}] เข้าไปยัง: {link}")
            time.sleep(3)

            title = driver.find_element(By.CSS_SELECTOR, 'h1.pdp-mod-product-badge-title').text.strip()
            price = driver.find_element(By.CSS_SELECTOR, 'span.pdp-price.pdp-price_type_normal').text.strip()

            try:
                sales = driver.find_element(By.CSS_SELECTOR, 'div.pdp-product-highlights span').text.strip()
            except:
                sales = "ไม่พบยอดขาย"

            data.append([title, price, sales])
        except Exception as e:
            print(f"❌ ข้อผิดพลาดในลิงก์ที่ {index}: {e}")

finally:
    driver.quit()

# บันทึกลง CSV
with open('yogurt_data.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['ชื่อสินค้า', 'ราคา', 'จำนวนยอดขาย'])
    writer.writerows(data)

print(f"\n✅ บันทึกข้อมูลเรียบร้อย: yogurt_data.csv ({len(data)} รายการ)")
