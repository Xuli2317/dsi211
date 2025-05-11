import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import json

# Setup Selenium with Chrome (non-headless for login)
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment for headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

# Use webdriver_manager to get compatible ChromeDriver
service = Service(ChromeDriverManager().install())
try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
except Exception as e:
    print(f"Error initializing ChromeDriver: {e}")
    raise

# Navigate to CpMeiji_TH profile
url = "https://x.com/CpMeiji_TH"
try:
    driver.get(url)
    print("Page loaded. Waiting for content...")
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "article[data-testid='tweet']"))
    )
    # Check for login prompt
    try:
        login_button = driver.find_element(By.CSS_SELECTOR, "a[href='/login']")
        if login_button:
            print("Login required. Please log in manually in the browser window.")
            time.sleep(60)  # Give 60 seconds to log in
            WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "article[data-testid='tweet']"))
            )
    except:
        print("No login prompt detected or login completed.")
except Exception as e:
    print(f"Error loading page or waiting for content: {e}")
    driver.quit()
    raise

# Scroll to load more posts
scrolls = 20  # Increased to load more posts
post_count = 0
for i in range(scrolls):
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)  # Increased wait for JS to load more posts
        # Check number of posts after each scroll
        new_posts = len(driver.find_elements(By.CSS_SELECTOR, "article[data-testid='tweet']"))
        print(f"Scroll {i+1}/{scrolls} completed. Found {new_posts} posts so far")
        if new_posts == post_count:
            print("No new posts loaded. Stopping scroll.")
            break
        post_count = new_posts
    except Exception as e:
        print(f"Error scrolling page: {e}")
        break

# Get page source and parse with BeautifulSoup
try:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
except Exception as e:
    print(f"Error parsing page source: {e}")
    driver.quit()
    raise

driver.quit()

# Extract posts
posts = soup.find_all('article', {'data-testid': 'tweet'})
print(f"Found {len(posts)} posts in total")

data = []
for post in posts:
    try:
        # Extract post text
        text_elem = post.find('div', {'data-testid': 'tweetText'})
        text = text_elem.get_text(strip=True) if text_elem else "N/A"
        
        data.append({
            'Post Text': text
        })
        print(f"Processed post: {text[:50]}...")
    except Exception as e:
        print(f"Error processing post: {e}")
        continue

# Save to JSON file
with open('meiji_posts.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# Summary report
print("Data has been saved to meiji_posts.json")
print("\n5 อันดับโพสต์แรก:")
df = pd.DataFrame(data)
print(df['Post Text'].head())
