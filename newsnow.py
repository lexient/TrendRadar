import requests
from bs4 import BeautifulSoup
try:
    from crawlers.base import BaseCrawler
except ImportError:
    class BaseCrawler:
        pass

class NewsNow(BaseCrawler):
    def __init__(self):
        # alt https://www.newsnow.co.uk/h/Hot+Topics
        self.url = "https://www.newsnow.co.uk/h/Technology" 

    def crawl(self):
        print(f"Start crawling NewsNow: {self.url}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        try:
            response = requests.get(self.url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"NewsNow connection failed: {response.status_code}")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            news_list = []
            
            # NewsNow uses class 'hl' for headlines in their grid
            items = soup.select('.hl')
            
            for index, item in enumerate(items[:30]):  # Get Top 30
                try:
                    link = item.select_one('a.hll')
                    if not link: continue
                        
                    title = link.get_text().strip()
                    url = link['href']
                    
                    news_list.append({
                        "title": title,
                        "url": url,
                        "hot_value": 1000 - index, # Fake 'popularity' score
                    })
                except:
                    continue

            print(f"NewsNow: Found {len(news_list)} items")
            return news_list
            
        except Exception as e:
            print(f"NewsNow Error: {e}")
            return []
