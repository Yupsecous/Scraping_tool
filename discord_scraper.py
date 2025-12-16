"""
Automated Discord Invite Link Scraper
Searches x.com and articles for Discord invite links related to crypto, blockchain, NFT, game, and agent keywords.
"""

import re
import time
import json
import requests
from urllib.parse import quote_plus, urlparse
from bs4 import BeautifulSoup
from datetime import datetime
import sys

class DiscordLinkScraper:
    def __init__(self, output_file='invite_link.txt', use_google_api=False, api_key=None, search_engine_id=None):
        self.output_file = output_file
        self.discord_links = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Optional: Google Custom Search API (free tier: 100 searches/day)
        self.use_google_api = use_google_api
        if use_google_api and api_key and search_engine_id:
            try:
                from google_search_api import GoogleCustomSearchAPI
                self.google_api = GoogleCustomSearchAPI(api_key, search_engine_id)
                print("Google Custom Search API enabled (100 free searches/day)")
            except:
                self.google_api = None
                print("Google Custom Search API not available, using free scraping method")
        else:
            self.google_api = None
        
        # Discord invite link patterns
        self.discord_patterns = [
            r'https?://discord\.gg/[a-zA-Z0-9-]+',
            r'https?://discord\.com/invite/[a-zA-Z0-9-]+',
            r'discord\.gg/[a-zA-Z0-9-]+',
            r'discord\.com/invite/[a-zA-Z0-9-]+',
        ]
        
        # Keywords to search for
        self.keywords = ['crypto', 'blockchain', 'nft', 'game', 'agent', 'defi', 'web3', 'metaverse', 'dao']
        
        # Load existing links
        self.load_existing_links()
    
    def load_existing_links(self):
        """Load existing links from file to avoid duplicates."""
        try:
            with open(self.output_file, 'r', encoding='utf-8') as f:
                for line in f:
                    link = line.strip()
                    if link and link.startswith('http'):
                        self.discord_links.add(link)
            print(f"Loaded {len(self.discord_links)} existing links from {self.output_file}")
        except FileNotFoundError:
            print(f"No existing file found. Starting fresh.")
    
    def normalize_link(self, link):
        """Normalize Discord invite links to full URLs."""
        if not link.startswith('http'):
            link = 'https://' + link
        # Normalize discord.com/invite to discord.gg
        link = link.replace('discord.com/invite/', 'discord.gg/')
        return link
    
    def extract_discord_links(self, text):
        """Extract Discord invite links from text using regex patterns."""
        links = set()
        for pattern in self.discord_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                normalized = self.normalize_link(match)
                if 'discord.gg/' in normalized:
                    links.add(normalized)
        return links
    
    def search_google(self, query, max_results=100):
        """Search Google for pages containing Discord invite links."""
        print(f"\nSearching Google for: {query}")
        links_found = set()
        
        # Try Google Custom Search API first if available
        if self.google_api and self.google_api.is_available():
            try:
                results = self.google_api.search(query, num_results=10)
                for result in results:
                    # Extract from title, link, and snippet
                    text = f"{result['title']} {result['link']} {result['snippet']}"
                    discord_links = self.extract_discord_links(text)
                    links_found.update(discord_links)
                
                if links_found:
                    print(f"Found {len(links_found)} Discord links via Google API")
                    return links_found
            except Exception as e:
                print(f"Google API error, falling back to scraping: {str(e)}")
        
        # Fallback to free Google search scraping
        try:
            # Google search URL with proper parameters
            search_url = f"https://www.google.com/search?q={quote_plus(query)}&num={min(max_results, 100)}&hl=en"
            
            # Add headers to mimic a real browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Referer': 'https://www.google.com/',
            }
            
            response = self.session.get(search_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Method 1: Extract from search result snippets and URLs
                # Google search results are in divs with class 'g' or similar
                for result in soup.find_all(['div', 'a'], class_=lambda x: x and ('g' in str(x).lower() or 'result' in str(x).lower())):
                    # Extract text content
                    text = result.get_text()
                    discord_links = self.extract_discord_links(text)
                    links_found.update(discord_links)
                    
                    # Extract from href attributes
                    if result.name == 'a' and result.get('href'):
                        href = result.get('href')
                        # Google search result links start with /url?q=
                        if '/url?q=' in href:
                            # Extract actual URL
                            try:
                                actual_url = href.split('/url?q=')[1].split('&')[0]
                                discord_links = self.extract_discord_links(actual_url)
                                links_found.update(discord_links)
                            except:
                                pass
                        else:
                            discord_links = self.extract_discord_links(href)
                            links_found.update(discord_links)
                
                # Method 2: Extract from all links
                for link in soup.find_all('a', href=True):
                    href = link.get('href', '')
                    # Handle Google's URL redirect format
                    if '/url?q=' in href:
                        try:
                            actual_url = href.split('/url?q=')[1].split('&')[0]
                            # Extract Discord links from the actual URL
                            discord_links = self.extract_discord_links(actual_url)
                            links_found.update(discord_links)
                        except:
                            pass
                    else:
                        discord_links = self.extract_discord_links(href)
                        links_found.update(discord_links)
                    
                    # Extract from link text
                    text = link.get_text()
                    discord_links = self.extract_discord_links(text)
                    links_found.update(discord_links)
                
                # Method 3: Extract from entire page text (snippets, descriptions)
                page_text = soup.get_text()
                discord_links = self.extract_discord_links(page_text)
                links_found.update(discord_links)
                
                # Method 4: Look for specific Google result patterns
                # Google often shows snippets with URLs
                for snippet in soup.find_all(['span', 'div'], class_=lambda x: x and ('snippet' in str(x).lower() or 'st' in str(x).lower())):
                    text = snippet.get_text()
                    discord_links = self.extract_discord_links(text)
                    links_found.update(discord_links)
                
                print(f"Found {len(links_found)} Discord links from Google search")
            else:
                print(f"Google search returned status code: {response.status_code}")
                if response.status_code == 429:
                    print("Rate limited by Google. Waiting 60 seconds...")
                    time.sleep(60)
        
        except requests.exceptions.Timeout:
            print("Request timed out. Retrying...")
            time.sleep(5)
        except Exception as e:
            print(f"Error searching Google: {str(e)}")
            import traceback
            traceback.print_exc()
        
        return links_found
    
    def scrape_web_page(self, url):
        """Scrape a web page for Discord invite links."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
            response = self.session.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract from all text content
                text = soup.get_text()
                links = self.extract_discord_links(text)
                
                # Extract from all links
                for link_tag in soup.find_all('a', href=True):
                    href = link_tag.get('href', '')
                    # Handle relative URLs
                    if href.startswith('/'):
                        href = urlparse(url).scheme + '://' + urlparse(url).netloc + href
                    links.update(self.extract_discord_links(href))
                
                # Extract from meta tags
                for meta in soup.find_all('meta', content=True):
                    content = meta.get('content', '')
                    links.update(self.extract_discord_links(content))
                
                return links
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
        
        return set()
    
    def search_x_com_via_google(self, query):
        """Search x.com via Google search."""
        # Remove duplicate site:x.com if already present
        if 'site:x.com' in query:
            x_query = query
        else:
            x_query = f'site:x.com {query}'
        return self.search_google(x_query)
    
    def search_articles(self, query):
        """Search articles and blog posts for Discord links."""
        article_sites = [
            'site:medium.com',
            'site:mirror.xyz',
            'site:substack.com',
            'site:hackernoon.com',
            'site:coindesk.com',
            'site:cointelegraph.com',
        ]
        
        all_links = set()
        
        for site in article_sites:
            search_query = f'{site} {query}'
            print(f"\nSearching {site} for: {query}")
            links = self.search_google(search_query)
            all_links.update(links)
            time.sleep(2)  # Rate limiting
        
        return all_links
    
    def generate_search_queries(self):
        """Generate various search queries."""
        queries = []
        
        # Base queries
        base_queries = [
            '"discord.gg/" crypto',
            '"discord.gg/" blockchain',
            '"discord.gg/" nft',
            '"discord.gg/" game',
            '"discord.gg/" agent',
            '"discord.gg/" defi',
            '"discord.gg/" web3',
            '"discord.gg/" metaverse',
            '"discord.gg/" dao',
            '"discord.gg/" crypto blockchain nft',
            '"discord.gg/" crypto game agent',
        ]
        
        # X.com specific queries
        for query in base_queries:
            queries.append(('x.com', f'site:x.com {query}'))
        
        # Article queries
        for query in base_queries:
            queries.append(('articles', query))
        
        # Combined keyword queries
        combined_keywords = [
            'crypto blockchain nft game agent "discord.gg/"',
            'crypto trading "discord.gg/"',
            'crypto community "discord.gg/"',
            'crypto alpha "discord.gg/"',
            'crypto signals "discord.gg/"',
            'nft collection "discord.gg/"',
            'crypto gaming "discord.gg/"',
            'defi protocol "discord.gg/"',
            'web3 project "discord.gg/"',
        ]
        
        for query in combined_keywords:
            queries.append(('x.com', f'site:x.com {query}'))
            queries.append(('articles', query))
        
        return queries
    
    def run(self, max_searches=50):
        """Run the scraper."""
        print("=" * 60)
        print("Discord Invite Link Scraper")
        print("=" * 60)
        print(f"Starting with {len(self.discord_links)} existing links")
        print(f"Will perform up to {max_searches} searches")
        print("=" * 60)
        
        queries = self.generate_search_queries()
        total_searches = min(len(queries), max_searches)
        
        for i, (source_type, query) in enumerate(queries[:total_searches], 1):
            print(f"\n[{i}/{total_searches}] Searching {source_type}: {query}")
            
            try:
                if source_type == 'x.com':
                    links = self.search_x_com_via_google(query)
                else:
                    links = self.search_articles(query)
                
                new_links = links - self.discord_links
                self.discord_links.update(links)
                
                if new_links:
                    print(f"Found {len(new_links)} new links!")
                    for link in new_links:
                        print(f"  - {link}")
                else:
                    print("No new links found")
                
                # Save periodically
                if i % 10 == 0:
                    self.save_links()
                    print(f"\nProgress saved: {len(self.discord_links)} total links")
                
                # Rate limiting - random delay to avoid detection
                import random
                delay = random.uniform(2, 5)
                time.sleep(delay)
                
            except Exception as e:
                print(f"Error processing query: {str(e)}")
                continue
        
        # Final save
        self.save_links()
        
        print("\n" + "=" * 60)
        print(f"Scraping completed!")
        print(f"Total unique Discord invite links: {len(self.discord_links)}")
        print(f"Links saved to: {self.output_file}")
        print("=" * 60)
    
    def save_links(self):
        """Save all collected links to file."""
        sorted_links = sorted(self.discord_links)
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for link in sorted_links:
                f.write(f"{link}\n")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape Discord invite links from x.com and articles')
    parser.add_argument('-o', '--output', default='invite_link.txt', help='Output file (default: invite_link.txt)')
    parser.add_argument('-n', '--max-searches', type=int, default=50, help='Maximum number of searches (default: 50)')
    parser.add_argument('--use-api', action='store_true', help='Use Google Custom Search API (requires API key)')
    parser.add_argument('--api-key', default=None, help='Google Custom Search API key')
    parser.add_argument('--search-engine-id', default=None, help='Google Custom Search Engine ID')
    
    args = parser.parse_args()
    
    # Check for API credentials in config file
    api_key = args.api_key
    search_engine_id = args.search_engine_id
    
    try:
        with open('google_api_config.json', 'r') as f:
            config = json.load(f)
            if not api_key:
                api_key = config.get('api_key')
            if not search_engine_id:
                search_engine_id = config.get('search_engine_id')
    except FileNotFoundError:
        pass
    
    scraper = DiscordLinkScraper(
        output_file=args.output,
        use_google_api=args.use_api,
        api_key=api_key,
        search_engine_id=search_engine_id
    )
    scraper.run(max_searches=args.max_searches)

if __name__ == "__main__":
    main()

