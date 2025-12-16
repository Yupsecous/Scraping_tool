"""
Discord Invite Link Scraper for X.com
This script searches X.com for Discord invite links related to crypto, blockchain, NFT, game, and agent keywords.
"""

import re
import time
import json
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup

# Keywords to search for
KEYWORDS = ['crypto', 'blockchain', 'nft', 'game', 'agent']
BASE_SEARCH_URL = "https://x.com/search"

# Discord invite link patterns
DISCORD_PATTERNS = [
    r'discord\.gg/[a-zA-Z0-9]+',
    r'discord\.com/invite/[a-zA-Z0-9-]+',
    r'discord\.gg/[a-zA-Z0-9]{7,}',
]

def extract_discord_links(text):
    """Extract Discord invite links from text using regex patterns."""
    links = set()
    for pattern in DISCORD_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if 'discord.gg/' in match:
                links.add(f"https://{match}")
            elif 'discord.com/invite/' in match:
                links.add(f"https://{match}")
    return links

def search_x_com(query, max_results=100):
    """
    Search X.com for Discord invite links.
    Note: This is a basic implementation. For production use, you would need:
    - X.com API access (Twitter API v2)
    - Proper authentication
    - Rate limiting handling
    - Compliance with X.com's Terms of Service
    """
    all_links = set()
    
    # Construct search query
    search_query = f'{query} "discord.gg/" site:x.com'
    encoded_query = quote_plus(search_query)
    
    print(f"Searching for: {search_query}")
    
    # Note: Direct scraping of X.com requires authentication and may violate ToS
    # This is a template that would need to be adapted for actual use
    # Consider using X.com API instead
    
    return all_links

def main():
    """Main function to collect Discord invite links."""
    all_discord_links = set()
    
    # Read existing links from file
    try:
        with open('invite_link.txt', 'r', encoding='utf-8') as f:
            existing_links = set(line.strip() for line in f if line.strip())
            all_discord_links.update(existing_links)
            print(f"Loaded {len(existing_links)} existing links")
    except FileNotFoundError:
        print("No existing invite_link.txt file found. Starting fresh.")
    
    # Search queries based on keywords
    search_queries = [
        'crypto "discord.gg/"',
        'blockchain "discord.gg/"',
        'nft "discord.gg/"',
        'game "discord.gg/"',
        'agent "discord.gg/"',
        'crypto blockchain nft game agent "discord.gg/"',
        'defi "discord.gg/"',
        'web3 "discord.gg/"',
        'metaverse "discord.gg/"',
        'dao "discord.gg/"',
        'token "discord.gg/"',
        'airdrop "discord.gg/"',
        'mint "discord.gg/"',
        'whitelist "discord.gg/"',
        'alpha "discord.gg/"',
        'signals "discord.gg/"',
        'trading "discord.gg/"',
    ]
    
    print(f"\nStarting search for Discord invite links...")
    print(f"Target: 10,000+ links")
    print(f"Current: {len(all_discord_links)} links\n")
    
    # For each search query
    for query in search_queries:
        print(f"Processing query: {query}")
        # In a real implementation, you would call search_x_com here
        # For now, this is a template
        
        # Add delay to respect rate limits
        time.sleep(1)
    
    # Save all unique links to file
    with open('invite_link.txt', 'w', encoding='utf-8') as f:
        sorted_links = sorted(all_discord_links)
        for link in sorted_links:
            f.write(f"{link}\n")
    
    print(f"\nCompleted! Found {len(all_discord_links)} unique Discord invite links.")
    print(f"Links saved to invite_link.txt")

if __name__ == "__main__":
    print("=" * 60)
    print("Discord Invite Link Scraper for X.com")
    print("=" * 60)
    print("\nIMPORTANT NOTES:")
    print("1. This script requires X.com API access or proper scraping setup")
    print("2. You must comply with X.com's Terms of Service")
    print("3. Rate limiting and authentication are required")
    print("4. This is a template - actual implementation needs API keys")
    print("=" * 60)
    print()
    
    # Uncomment the line below when you have proper API setup
    # main()
    
    print("To use this script:")
    print("1. Get X.com API access at https://developer.x.com/")
    print("2. Install required packages: pip install requests beautifulsoup4")
    print("3. Add your API credentials")
    print("4. Uncomment main() call and run the script")

