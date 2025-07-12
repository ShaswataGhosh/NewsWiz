
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin



class webscrapper:

    def __init__(self, topic,user_agent=None):
        self.topic = topic
        self.content = []
        self.headers = {
            "User-Agent": user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
    
    def fetch_results(self):
        
        url =f"https://www.bbc.com/search?q={self.topic}&edgeauth=eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJrZXkiOiAiZmFzdGx5LXVyaS10b2tlbi0xIiwiZXhwIjogMTc1MjEzMDcxMiwibmJmIjogMTc1MjEzMDM1MiwicmVxdWVzdHVyaSI6ICIlMkZzZWFyY2glM0ZxJTNEdWtyYWluZSJ9.hvNBGpJez1_sBWvvCYvgTLhezdtX2icUPNx4wGVklYs"
        base_url = "https://www.bbc.com"
        result = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(result.text, "html.parser")
        
        #print(soup)
        pages = soup.find_all('div',class_='sc-225578b-0 btdqbl')
        
        for page in pages:
            h = page.find('h2', class_='sc-9d830f2a-3 duBczH')
            ns = page.find('div', class_='sc-cdecfb63-3 pGVVH')
            d = page.find('span', class_='sc-ac6bc755-1 gxJSVz')
            l = page.find('a', herf=True)
            
            h_ = h.get_text(strip=True) if h else 'No headline'
            ns_ = ns.get_text(strip=True) if ns else 'No summary'
            d_ = d.get_text(strip=True) if d else 'No date'
            a_tag = page.find('a', attrs={'data-testid': 'internal-link'})
            l_ = urljoin(base_url, a_tag["href"]) if a_tag and a_tag.get("href") else "No link"
                
               
            self.content.append({
                "headline":h_,
                "date":d_,
                "tagline":ns_,
                "link":l_ })
        return self.content
    def run(self):
        self.fetch_results()

# Entry point
if __name__ == "__main__":
    app = webscrapper()
    app.run()



            




