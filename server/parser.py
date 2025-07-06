import json
import time
from bs4 import BeautifulSoup
from .tab import UltimateTab, UltimateTabInfo
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def _tab_info_from_soup(soup: BeautifulSoup) -> UltimateTabInfo:
    '''
    Returns a populated UltimateTabInfo object based on the provided soup.
    Parses based on UG site construction as of 9/3/17.

    Parameters:
        - soup: A BeautifulSoup for a Ultimate Guitar tab's html (or html body)
    '''
    # Get song title and artist
    try:
        song_title = soup.find(attrs={'itemprop': 'name'}).text
        song_title = re.compile(re.escape('chords'), re.IGNORECASE).sub(r'', song_title).strip() # Remove the word 'chords'
    except:
        song_title = "UNKNOWN"

    try:
        artist_name = soup.find(attrs={'class': 't_autor'}).text.replace('\n', '')
        artist_name = re.compile(re.escape('by'), re.IGNORECASE).sub(r'', artist_name).strip()# Remove the word 'by'
    except:
        artist_name = "UNKNOWN"

    # Get info - author, capo, tuning, etc.
    author = "UNKNOWN"
    difficulty = None
    key = None
    capo = None
    tuning = None
    try:
        info_header_text = soup.find(attrs={'class': 't_dt'}).text.replace('\n', '')
        info_headers = [x.lower() for x in info_header_text.split(' ') if x] # Split string and make lowercase
        info_header_values = soup.findAll(attrs={'class': 't_dtde'})

        for index, header in enumerate(info_headers):
            try:
                if header == 'author':
                    author = info_header_values[index].a.text
                elif header == 'difficulty':
                    difficulty = info_header_values[index].text.strip()
                elif header == 'key':
                    key = info_header_values[index].text.strip()
                elif header == 'capo':
                    capo = info_header_values[index].text.strip()
                elif header == 'tuning':
                    tuning = info_header_values[index].text.strip()
            except:
                continue
    except:
        pass

    tab_info = UltimateTabInfo(song_title, artist_name, author, difficulty, key, capo, tuning)
    return tab_info

def is_chord_line(line):
    """
    A line is a chord line if it contains primarily chord names and spaces.
    This improved version checks for chord patterns and minimal text content.
    """
    line = line.strip()
    if not line:
        return False
    
    # Common chord patterns (more comprehensive)
    chord_pattern = re.compile(r'[A-G][#b]?(m|maj|min|dim|aug|sus[24]?|add\d*|maj7|m7|7|6|9|11|13)?')
    
    # Split the line into words
    words = line.split()
    if not words:
        return False
    
    # Count how many words are chords
    chord_count = 0
    total_chars = 0
    
    for word in words:
        total_chars += len(word)
        if chord_pattern.match(word):
            chord_count += 1
    
    # If more than 70% of words are chords, it's likely a chord line
    if len(words) > 0 and chord_count / len(words) >= 0.7:
        return True
    
    # Also check if the line is mostly spaces and a few chord-like words
    # This catches lines like "    Cadd9  G  D                  Em7"
    non_space_chars = len(line.replace(' ', ''))
    if non_space_chars > 0 and chord_count / non_space_chars >= 0.6:
        return True
    
    return False

def html_tab_to_json_dict(html_body: str) -> json:
    start_parse = time.time()
    soup = BeautifulSoup(html_body, "html.parser")
    tab_info = _tab_info_from_soup(soup)
    pre_tag = soup.find('pre')
    if pre_tag is None:
        return {'error': 'Could not find <pre> tag with tab content in the page. The page structure may have changed.'}
    
    tab = UltimateTab()
    tab_text = pre_tag.get_text('\n')  # Get all text, preserving newlines
    lines = tab_text.splitlines()
    
    # More sophisticated parsing: look for patterns
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            tab.append_blank_line()
            i += 1
            continue
        
        # Check if this line looks like a chord line
        if is_chord_line(line):
            tab.append_chord_line(line)
            i += 1
        else:
            # This is a lyric line
            tab.append_lyric_line(line)
            i += 1
    
    json_obj = {
        'title': tab_info.title,
        'artist_name': tab_info.artist,
        'author': tab_info.author
    }
    if tab_info.difficulty is not None:
        json_obj['difficulty'] = tab_info.difficulty
    if tab_info.key is not None:
        json_obj['key'] = tab_info.key
    if tab_info.capo is not None:
        json_obj['capo'] = tab_info.capo
    if tab_info.tuning is not None:
        json_obj['tuning'] = tab_info.tuning
    json_obj['lines'] = tab.as_json_dictionary()['lines']
    print(f"[Timing] Tab parsing time: {time.time() - start_parse:.2f}s")
    return {'tab': json_obj}

def get_rendered_html(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-features=VizDisplayCompositor")
    # Block images, CSS, fonts via CDP
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(10)
    try:
        driver.execute_cdp_cmd("Network.enable", {})
        driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.css", "*.woff", "*.ttf", "*.svg"]})
        start = time.time()
        driver.get(url)
        # Wait for <pre> tag to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "pre"))
        )
        html = driver.page_source
        print(f"[Timing] Selenium fetch time: {time.time() - start:.2f}s")
    except Exception as e:
        print(f"[Error] Selenium page load failed: {e}")
        html = ""
    finally:
        driver.quit()
    return html

# Optionally, you could add a fallback to requests+BeautifulSoup for static pages:
def get_html_requests(url):
    import requests
    start = time.time()
    try:
        # Use a session with optimized headers for faster requests
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        resp = session.get(url, timeout=10)  # Reduced timeout for faster failure
        resp.raise_for_status()
        print(f"[Timing] requests fetch time: {time.time() - start:.2f}s")
        return resp.text
    except Exception as e:
        print(f"[Error] requests fetch failed: {e}")
        return ""
