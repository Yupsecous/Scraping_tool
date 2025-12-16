"""
Setup script for Google Custom Search API (Optional - Free tier: 100 searches/day)
This is completely optional. The scraper works fine without it using free Google search.
"""

import json
import os

def setup_google_api():
    """Interactive setup for Google Custom Search API."""
    print("=" * 60)
    print("Google Custom Search API Setup (Optional)")
    print("=" * 60)
    print()
    print("This is OPTIONAL. The scraper works fine without it!")
    print("Google Custom Search API provides:")
    print("  - Free tier: 100 searches per day")
    print("  - More reliable results")
    print("  - Official API access")
    print()
    print("To get free API credentials:")
    print("  1. Go to https://developers.google.com/custom-search/v1/overview")
    print("  2. Create a project and enable Custom Search API")
    print("  3. Create a Custom Search Engine at:")
    print("     https://programmablesearchengine.google.com/")
    print("  4. Get your API key and Search Engine ID")
    print()
    
    use_api = input("Do you want to set up Google Custom Search API? (y/n): ").lower().strip()
    
    if use_api != 'y':
        print("Skipping API setup. The scraper will use free Google search scraping.")
        return
    
    print()
    api_key = input("Enter your Google API Key (or press Enter to skip): ").strip()
    search_engine_id = input("Enter your Search Engine ID (or press Enter to skip): ").strip()
    
    if api_key and search_engine_id:
        config = {
            'api_key': api_key,
            'search_engine_id': search_engine_id
        }
        
        with open('google_api_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print()
        print("✓ Google API configuration saved to google_api_config.json")
        print("  The scraper will use the API when you run with --use-api flag")
    else:
        print("API setup skipped. The scraper will use free Google search scraping.")

if __name__ == "__main__":
    setup_google_api()

