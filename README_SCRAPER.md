# Discord Invite Link Scraper

Automated tool to scrape Discord invite links from x.com and articles related to crypto, blockchain, NFT, game, and agent keywords.

## Features

- Searches x.com via Google for Discord invite links
- Searches articles from Medium, Mirror, Substack, and crypto news sites
- Extracts unique Discord invite links
- Saves links to `invite_link.txt`
- Avoids duplicates
- Rate limiting to prevent blocking

## Installation

1. Install Python 3.7 or higher
2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python discord_scraper.py
```

### Advanced Usage
```bash
# Specify output file
python discord_scraper.py -o my_links.txt

# Limit number of searches
python discord_scraper.py -n 100

# Combine options
python discord_scraper.py -o invite_link.txt -n 200
```

## How It Works

1. **Loads existing links** from the output file to avoid duplicates
2. **Generates search queries** based on keywords (crypto, blockchain, NFT, game, agent, etc.)
3. **Searches Google for FREE** using:
   - Direct Google search scraping (FREE - unlimited searches)
   - Optional: Google Custom Search API (FREE tier: 100 searches/day)
4. **Searches for**:
   - x.com posts containing Discord links
   - Articles from Medium, Mirror, Substack, etc.
5. **Extracts Discord invite links** using regex patterns
6. **Saves unique links** to the output file

## Google Search - FREE Methods

The scraper uses **FREE Google search** by default:

### Method 1: Direct Google Search Scraping (Default - FREE)
- ✅ **Completely FREE** - No API keys needed
- ✅ **Unlimited searches** - Search as much as you want
- ✅ **Works immediately** - No setup required
- ⚠️ May have rate limits (handled automatically)

### Method 2: Google Custom Search API (Optional - FREE tier)
- ✅ **FREE tier**: 100 searches per day
- ✅ More reliable results
- ⚠️ Requires API setup (optional)

To use the API (optional):
```bash
python setup_google_api.py
python discord_scraper.py --use-api
```

## Search Queries

The scraper automatically generates queries like:
- `site:x.com "discord.gg/" crypto`
- `site:x.com "discord.gg/" blockchain`
- `site:medium.com "discord.gg/" crypto`
- And many more combinations...

## Output

All unique Discord invite links are saved to `invite_link.txt` (or your specified file), one per line.

## Notes

- **Rate Limiting**: The scraper includes delays between requests to avoid being blocked
- **Respect ToS**: Make sure your usage complies with Google's Terms of Service
- **Legal**: Always respect the terms of service of websites you're scraping
- **Time**: Collecting 10,000+ links will take time due to rate limits

## Troubleshooting

- If you get blocked, reduce the number of searches or increase delays
- Some links may be expired or invalid - this is normal
- The scraper saves progress every 10 searches

## Example Output

```
============================================================
Discord Invite Link Scraper
============================================================
Starting with 50 existing links
Will perform up to 50 searches
============================================================

[1/50] Searching x.com: site:x.com "discord.gg/" crypto
Found 5 new links!
  - https://discord.gg/example1
  - https://discord.gg/example2
...

Scraping completed!
Total unique Discord invite links: 150
Links saved to: invite_link.txt
============================================================
```

