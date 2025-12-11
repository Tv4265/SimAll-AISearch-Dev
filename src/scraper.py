import requests
from bs4 import BeautifulSoup
import json

def scrape_article_data(url: str) -> dict:
    """ดึงข้อมูลบทความและสร้างเป็นโครงสร้างสำหรับ AI"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 1. หัวข้อหลัก
        title = soup.find('h1').text.strip()
        
        # 2. เนื้อหาสรุป (สำหรับ AI Overview)
        # (สมมติว่าเนื้อหาสรุปอยู่ใน div ที่มี class 'summarize-post')
        summary_div = soup.find('div', class_='summarize-post')
        summary = summary_div.text.strip() if summary_div else "N/A"
        
        # 3. ข้อมูล Metadata/E-E-A-T
        author_element = soup.find('span', class_='author-name')
        author = author_element.text.strip() if author_element else "Sim-All Team"
        
        return {
            'title': title,
            'summary': summary,
            'author': author,
            'url': url,
            'raw_content_length': len(response.text)
        }
    except requests.exceptions.RequestException as e:
        return {'error': f"Request Failed: {e}"}

# ตัวอย่างการใช้งานและบันทึกผล
# article_url = "https://sim-all.com/check-horoscope-2569-fire-horse/"
# data_result = scrape_article_data(article_url)
# with open('data/raw/horoscope_2569_raw.json', 'w', encoding='utf-8') as f:
#     json.dump(data_result, f, indent=4, ensure_ascii=False)
