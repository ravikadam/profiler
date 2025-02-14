import requests
from bs4 import BeautifulSoup
from typing import Dict, Any
import logging

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape_website(self, url: str) -> Dict[str, Any]:
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text content
            text_content = []
            for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']):
                if tag.text.strip():
                    text_content.append(tag.text.strip())
            
            # Extract meta information
            meta_description = ""
            meta_keywords = ""
            
            meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
            if meta_desc_tag:
                meta_description = meta_desc_tag.get('content', '')
                
            meta_keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
            if meta_keywords_tag:
                meta_keywords = meta_keywords_tag.get('content', '')
            
            # Extract social media links
            social_links = {}
            social_patterns = ['facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com']
            for link in soup.find_all('a', href=True):
                href = link['href'].lower()
                for pattern in social_patterns:
                    if pattern in href:
                        social_links[pattern.split('.')[0]] = href
            
            return {
                'text_content': ' '.join(text_content),
                'meta_description': meta_description,
                'meta_keywords': meta_keywords,
                'social_links': social_links,
                'title': soup.title.string if soup.title else '',
                'url': url
            }
            
        except Exception as e:
            logging.error(f"Error scraping website {url}: {str(e)}")
            raise