# Discord Scraper GUI - Features

## New Features Added

### ✅ Keyword Selection
- **12 Available Keywords:**
  - crypto
  - AI
  - blockchain
  - chain
  - defi
  - dapp
  - game
  - agent
  - ecosystem
  - nft
  - coin
  - wallet

- **Features:**
  - Select/deselect individual keywords
  - "Select All" button
  - "Deselect All" button
  - All keywords selected by default

### ✅ Site Selection
- **7 Available Sites:**
  - x.com (X/Twitter) - Selected by default
  - medium.com (Medium)
  - mirror.xyz (Mirror)
  - substack.com (Substack)
  - hackernoon.com (HackerNoon)
  - coindesk.com (CoinDesk)
  - cointelegraph.com (CoinTelegraph)

- **Features:**
  - Select/deselect individual sites
  - "Select All Sites" button
  - "Deselect All Sites" button
  - x.com selected by default

### ✅ Smart Query Generation
- Automatically generates search queries based on:
  - Selected keywords
  - Selected sites
  - Keyword combinations (2-3 keywords at a time)

### ✅ Validation
- Checks that at least one keyword is selected
- Checks that at least one site is selected
- Shows error messages if validation fails

## How It Works

1. **Select Keywords**: Choose which keywords to search for
2. **Select Sites**: Choose which websites to search
3. **Set Max Searches**: Limit the number of searches
4. **Start Scraping**: The tool generates queries based on your selections

## Example Usage

### Scenario 1: Search only crypto and NFT on x.com
- Keywords: ✅ crypto, ✅ nft (others unchecked)
- Sites: ✅ x.com (others unchecked)
- Result: Searches x.com for "discord.gg/" crypto and "discord.gg/" nft

### Scenario 2: Search AI and blockchain on all sites
- Keywords: ✅ AI, ✅ blockchain (others unchecked)
- Sites: ✅ All sites selected
- Result: Searches all selected sites for AI and blockchain related Discord links

### Scenario 3: Search multiple keywords on specific sites
- Keywords: ✅ crypto, ✅ defi, ✅ game
- Sites: ✅ x.com, ✅ medium.com
- Result: Generates queries combining keywords and searches both sites

## Benefits

- **Flexible**: Choose exactly what you want to search
- **Efficient**: Don't waste searches on unwanted keywords/sites
- **Customizable**: Mix and match keywords and sites
- **User-Friendly**: Visual checkboxes make it easy to configure

