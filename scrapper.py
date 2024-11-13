import requests
from bs4 import BeautifulSoup
import json
import time
import re

class WikiGynecologyScraper:
    def __init__(self):
        self.base_url = "https://en.wikipedia.org"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.data = []
        self.scraped_urls = set()  # To avoid duplicates

    def clean_text(self, text):
        # Remove citations [1], [2], etc.
        text = re.sub(r'\[\d+\]', '', text)
        # Remove edit links [edit]
        text = re.sub(r'\[edit\]', '', text)
        # Clean extra whitespace
        text = ' '.join(text.split())
        return text.strip()

    def scrape_page(self, url):
        if url in self.scraped_urls:
            return None
        
        try:
            print(f"Scraping: {url}")
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            self.scraped_urls.add(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Get title
            title = soup.find('h1', {'id': 'firstHeading'}).text.strip()
            
            # Get introduction (before the first heading)
            intro = []
            content_div = soup.find('div', {'id': 'mw-content-text'})
            for p in content_div.find_all('p', recursive=False):
                if p.find_previous('h2') is None:
                    text = self.clean_text(p.get_text())
                    if text and len(text) > 50:
                        intro.append(text)

            # Get sections
            sections = {}
            current_section = None
            for element in content_div.find_all(['h2', 'h3', 'p', 'ul']):
                if element.name in ['h2', 'h3']:
                    section_title = self.clean_text(element.get_text())
                    if 'References' not in section_title and 'See also' not in section_title and 'External links' not in section_title:
                        current_section = section_title
                        sections[current_section] = {'text': [], 'lists': []}
                elif current_section and element.name == 'p':
                    text = self.clean_text(element.get_text())
                    if text and len(text) > 50:
                        sections[current_section]['text'].append(text)
                elif current_section and element.name == 'ul':
                    list_items = []
                    for li in element.find_all('li', recursive=False):
                        item_text = self.clean_text(li.get_text())
                        if item_text:
                            list_items.append(item_text)
                    if list_items:
                        sections[current_section]['lists'].append(list_items)

            # Find related links
            related_links = []
            for link in soup.find_all('a'):
                href = link.get('href', '')
                if href.startswith('/wiki/') and any(term in href.lower() for term in [
                    'gynecologic', 'gynaecologic', 'ovarian', 'uterine', 'vaginal', 
                    'cervical', 'endometri', 'menstrual', 'pcos', 'syndrome'
                ]):
                    full_url = f"https://en.wikipedia.org{href}"
                    if full_url not in self.scraped_urls:
                        related_links.append(full_url)

            return {
                'url': url,
                'title': title,
                'introduction': intro,
                'sections': sections,
                'related_links': related_links
            }
            
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None

    def save_to_json(self, filename='wikipedia_gynecology_data.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        print(f"Data saved to {filename}")

def main():
    # Starting URLs for gynecological conditions
    start_urls = [
        'https://en.wikipedia.org/wiki/Gynaecology',
        'https://en.wikipedia.org/wiki/Gynecologic_disorder',
        'https://en.wikipedia.org/wiki/Benign_gynecological_condition',
        'https://en.wikipedia.org/wiki/Ovarian_disease',
        'https://en.wikipedia.org/wiki/Menstrual_disorder',
        'https://en.wikipedia.org/wiki/Polycystic_ovary_syndrome',
        'https://en.wikipedia.org/wiki/Endometriosis',
        'https://en.wikipedia.org/wiki/Uterine_fibroid',
        'https://en.wikipedia.org/wiki/Cervical_cancer',
        'https://en.wikipedia.org/wiki/Ovarian_cancer',
        'https://en.wikipedia.org/wiki/Vaginal_disease',
        'https://en.wikipedia.org/wiki/Pelvic_inflammatory_disease'
    ]

    scraper = WikiGynecologyScraper()
    urls_to_scrape = start_urls.copy()
    
    while urls_to_scrape:
        url = urls_to_scrape.pop(0)
        data = scraper.scrape_page(url)
        
        if data:
            scraper.data.append(data)
            # Add new related links to scrape
            urls_to_scrape.extend([link for link in data['related_links'][:5] 
                                 if link not in scraper.scraped_urls])
            # Be respectful to Wikipedia's servers
            time.sleep(2)
        
        # Limit the number of pages to scrape (adjust as needed)
        if len(scraper.data) >= 50:
            break
    
    scraper.save_to_json()

if __name__ == "__main__":
    main()