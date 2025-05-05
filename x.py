import tweepy
import yake

# ใส่คีย์ API ที่ได้จาก Twitter Developer Portal
BEARER_TOKEN = "YOUR_TWITTER_BEARER_TOKEN"

# สร้าง client สำหรับดึงข้อมูลจาก Twitter/X
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# ค้นหาทวีตที่มีคำว่า "โยเกิร์ต"
query = "โยเกิร์ต -is:retweet lang:th"
try:
    tweets = client.search_recent_tweets(query=query, max_results=50)
    
    if not tweets.data:
        print("ไม่พบทวีตเกี่ยวกับโยเกิร์ตในช่วงนี้")
    else:
        # รวมข้อความทั้งหมด
        all_text = " ".join(tweet.text for tweet in tweets.data)

        # ดึงคีย์เวิร์ดด้วย YAKE
        kw_extractor = yake.KeywordExtractor(lan="th", n=1, top=10)
        keywords = kw_extractor.extract_keywords(all_text)

        # กรองคีย์เวิร์ดที่เกี่ยวข้องกับโยเกิร์ต
        relevant_keywords = [kw for kw, score in keywords if "โยเกิร์ต" in kw or "Yogurt" in kw]

        # แสดงคีย์เวิร์ด
        if relevant_keywords:
            print("คีย์เวิร์ดยอดนิยมเกี่ยวกับโยเกิร์ต:")
            for kw in relevant_keywords:
                print(kw)
        else:
            print("ไม่พบคีย์เวิร์ดที่เกี่ยวข้องกับโยเกิร์ต")
except tweepy.TweepyException as e:
    print(f"เกิดข้อผิดพลาดในการดึงข้อมูลจาก Twitter: {e}")
