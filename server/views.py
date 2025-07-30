from server import app
from flask import request, jsonify
from urllib.parse import urlparse
from .tab_parser import dict_from_ultimate_tab, grouped_blocks_from_ultimate_tab
import re
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time


SUPPORTED_UG_URI = 'tabs.ultimate-guitar.com'

@app.route('/')
def index():
    return 'The API Server is running'

@app.route('/api/health')
def health():
    return 'API Server is running ✅'

@app.route('/tab/v1')
def tab_v1():
    try:
        ultimate_url = request.args.get('url')

        # Ensure sanitized url
        parsed_url = urlparse(ultimate_url)
        location = parsed_url.netloc
        if location != SUPPORTED_UG_URI:
            raise Exception('unsupported url scheme')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    tab_dict = dict_from_ultimate_tab(ultimate_url)
    return jsonify(tab_dict)

@app.route('/tab')
def tab_v2():
    try:
        ultimate_url = request.args.get('url')

        # Ensure sanitized url
        parsed_url = urlparse(ultimate_url)
        location = parsed_url.netloc
        if location != SUPPORTED_UG_URI:
            raise Exception('unsupported url scheme')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    grouped_blocks = grouped_blocks_from_ultimate_tab(ultimate_url)

    # Post-process for joined text output
    lyrics_lines = []
    tabs_lines = []
    for block in grouped_blocks:
        if 'lyrics' in block:
            lyrics_lines.extend(block['lyrics'])
        if 'tabs' in block:
            tabs_lines.extend(block['tabs'])

    def clean_lines(lines):
        # Remove excessive empty lines (no more than one in a row)
        cleaned = []
        prev_empty = False
        for line in lines:
            is_empty = not line.strip()
            if is_empty and prev_empty:
                continue
            cleaned.append(line)
            prev_empty = is_empty
        # Remove leading/trailing empty lines
        while cleaned and not cleaned[0].strip():
            cleaned.pop(0)
        while cleaned and not cleaned[-1].strip():
            cleaned.pop()
        return cleaned

    lyrics_lines = clean_lines(lyrics_lines)
    tabs_lines = clean_lines(tabs_lines)

    lyrics_text = '\n'.join(lyrics_lines)
    tabs_text = '\n'.join(tabs_lines)

    return jsonify({
        'blocks': grouped_blocks,
        'lyrics_text': lyrics_text,
        'tabs_text': tabs_text
    })

@app.route('/search')
def search_song():
    """
    Search for a song by name and return the Ultimate Guitar URL
    """
    try:
        song_name = request.args.get('song')
        artist_name = request.args.get('artist', '')
        
        if not song_name:
            return jsonify({'error': 'Song name is required'}), 400

        # Search Ultimate Guitar dynamically
        matching_url = search_ultimate_guitar(song_name, artist_name)
        
        if not matching_url:
            return jsonify({'error': f'No tabs found for "{song_name}". Try using the /tab endpoint with a direct Ultimate Guitar URL.'}), 404

        # Return the URL directly without trying to parse it
        return jsonify({
            'song_name': song_name,
            'artist_name': artist_name,
            'url': matching_url,
            'message': 'URL found. Use this URL with your Flutter app to fetch the tab content.'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def search_ultimate_guitar(song_name, artist_name=''):
    """
    Search Ultimate Guitar website for a song and return the best matching URL
    """
    try:
        # Construct search query
        search_query = song_name
        if artist_name:
            search_query = f"{artist_name} {song_name}"
        
        # URL encode the search query
        encoded_query = urllib.parse.quote(search_query)
        
        # Search URL for Ultimate Guitar
        search_url = f"https://www.ultimate-guitar.com/search.php?search_type=title&value={encoded_query}"
        
        print(f"Searching URL: {search_url}")  # Debug log
        
        # Make the request with headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        print(f"Response status: {response.status_code}")  # Debug log
        
        # Parse the HTML response
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for tab links in the search results - try multiple patterns
        tab_links = []
        
        # Pattern 1: Direct tab links
        tab_links.extend(soup.find_all('a', href=re.compile(r'/tab/.*')))
        
        # Pattern 2: Full tabs.ultimate-guitar.com URLs
        tab_links.extend(soup.find_all('a', href=re.compile(r'tabs\.ultimate-guitar\.com.*')))
        
        # Pattern 3: Any link containing 'tab'
        tab_links.extend(soup.find_all('a', href=re.compile(r'.*tab.*')))
        
        # Pattern 4: Look for links in search result containers
        search_results = soup.find_all('div', class_=re.compile(r'search.*result|result.*item'))
        for result in search_results:
            tab_links.extend(result.find_all('a', href=re.compile(r'.*tab.*')))
        
        # Pattern 5: Look for any link that might be a tab
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            href = link.get('href', '')
            if 'tab' in href.lower() or 'ultimate-guitar' in href.lower():
                tab_links.append(link)
        
        print(f"Found {len(tab_links)} potential tab links")  # Debug log
        
        # Filter and rank the results
        valid_urls = []
        for link in tab_links:
            href = link.get('href', '')
            
            # Convert relative URLs to absolute
            if href.startswith('/'):
                href = f"https://tabs.ultimate-guitar.com{href}"
            elif href.startswith('http'):
                # Ensure it's a tabs.ultimate-guitar.com URL
                if 'tabs.ultimate-guitar.com' in href:
                    valid_urls.append(href)
            else:
                continue
            
            # Only add if it's a valid tabs URL
            if 'tabs.ultimate-guitar.com' in href:
                valid_urls.append(href)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_urls = []
        for url in valid_urls:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)
        
        print(f"Valid URLs found: {unique_urls}")  # Debug log
        
        # Return the first valid URL found
        if unique_urls:
            return unique_urls[0]
        
        # If no results found, try alternative search approach
        print("No results found with primary search, trying alternative approach...")
        return search_ultimate_guitar_alternative(song_name, artist_name)
        
    except requests.RequestException as e:
        print(f"Request error during search: {e}")
        return None
    except Exception as e:
        print(f"Error during search: {e}")
        return None

def search_ultimate_guitar_alternative(song_name, artist_name=''):
    """
    Alternative search method using different Ultimate Guitar search endpoints
    """
    try:
        # Construct search query
        search_query = song_name
        if artist_name:
            search_query = f"{artist_name} {song_name}"
        
        # URL encode the search query
        encoded_query = urllib.parse.quote(search_query)
        
        # Try different search URLs
        search_urls = [
            f"https://www.ultimate-guitar.com/search.php?search_type=title&value={encoded_query}",
            f"https://www.ultimate-guitar.com/search.php?search_type=artist&value={encoded_query}",
            f"https://www.ultimate-guitar.com/search.php?value={encoded_query}",
            f"https://tabs.ultimate-guitar.com/search?q={encoded_query}"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        for search_url in search_urls:
            print(f"Trying alternative search URL: {search_url}")
            
            try:
                response = requests.get(search_url, headers=headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for any links that might be tabs
                all_links = soup.find_all('a', href=True)
                tab_urls = []
                
                for link in all_links:
                    href = link.get('href', '')
                    if 'tabs.ultimate-guitar.com' in href or ('/tab/' in href and href.startswith('/')):
                        if href.startswith('/'):
                            href = f"https://tabs.ultimate-guitar.com{href}"
                        tab_urls.append(href)
                
                if tab_urls:
                    print(f"Found {len(tab_urls)} URLs with alternative search")
                    return tab_urls[0]
                    
            except Exception as e:
                print(f"Alternative search failed for {search_url}: {e}")
                continue
        
        return None
        
    except Exception as e:
        print(f"Error during alternative search: {e}")
        return None
