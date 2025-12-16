"""
Google Custom Search API Integration (Optional - Free tier: 100 searches/day)
This is an alternative method using Google's official API.
"""

import requests
import json
from urllib.parse import quote_plus

class GoogleCustomSearchAPI:
    def __init__(self, api_key=None, search_engine_id=None):
        """
        Initialize Google Custom Search API.
        
        To get free API credentials:
        1. Go to https://developers.google.com/custom-search/v1/overview
        2. Create a project and enable Custom Search API
        3. Create a Custom Search Engine at https://programmablesearchengine.google.com/
        4. Get your API key and Search Engine ID
        """
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        self.daily_quota = 100  # Free tier limit
        
    def search(self, query, num_results=10):
        """Search using Google Custom Search API."""
        if not self.api_key or not self.search_engine_id:
            print("Google Custom Search API not configured. Using free scraping method instead.")
            return []
        
        try:
            params = {
                'key': self.api_key,
                'cx': self.search_engine_id,
                'q': query,
                'num': min(num_results, 10)  # API limit is 10 per request
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                if 'items' in data:
                    for item in data['items']:
                        results.append({
                            'title': item.get('title', ''),
                            'link': item.get('link', ''),
                            'snippet': item.get('snippet', '')
                        })
                
                return results
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return []
        
        except Exception as e:
            print(f"Error using Google Custom Search API: {str(e)}")
            return []
    
    def is_available(self):
        """Check if API is configured."""
        return self.api_key and self.search_engine_id

