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
import os
import subprocess
import sys

def install_chrome_on_railway():
    """Install Chrome and ChromeDriver on Railway"""
    try:
        # Update package list
        subprocess.run(["apt-get", "update", "-y"], check=True, capture_output=True)
        
        # Install dependencies
        subprocess.run(["apt-get", "install", "-y", "wget", "gnupg", "curl"], check=True, capture_output=True)
        
        # Add Google Chrome repository
        subprocess.run(["wget", "-q", "-O", "-", "https://dl.google.com/linux/linux_signing_key.pub"], 
                      check=True, capture_output=True, stdout=subprocess.PIPE)
        
        # Add Chrome repository
        with open("/etc/apt/sources.list.d/google-chrome.list", "w") as f:
            f.write("deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main\n")
        
        # Update and install Chrome
        subprocess.run(["apt-get", "update", "-y"], check=True, capture_output=True)
        subprocess.run(["apt-get", "install", "-y", "google-chrome-stable"], check=True, capture_output=True)
        
        # Install ChromeDriver
        subprocess.run(["apt-get", "install", "-y", "chromium-chromedriver"], check=True, capture_output=True)
        
        print("Chrome and ChromeDriver installed successfully")
        return True
    except Exception as e:
        print(f"Failed to install Chrome: {e}")
        return False

def get_chrome_driver():
    """Get a working Chrome driver with multiple fallback strategies"""
    
    # Strategy 1: Try system Chrome
    try:
        if os.path.exists("/usr/bin/google-chrome-stable"):
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-infobars")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--blink-settings=imagesEnabled=false")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-renderer-backgrounding")
            options.add_argument("--disable-features=TranslateUI")
            options.add_argument("--disable-ipc-flooding-protection")
            
            service = Service("/usr/bin/google-chrome-stable")
            driver = webdriver.Chrome(service=service, options=options)
            print("Using system Chrome")
            return driver
    except Exception as e:
        print(f"System Chrome failed: {e}")
    
    # Strategy 2: Try system ChromeDriver
    try:
        if os.path.exists("/usr/bin/chromedriver"):
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-infobars")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--blink-settings=imagesEnabled=false")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-renderer-backgrounding")
            options.add_argument("--disable-features=TranslateUI")
            options.add_argument("--disable-ipc-flooding-protection")
            
            service = Service("/usr/bin/chromedriver")
            driver = webdriver.Chrome(service=service, options=options)
            print("Using system ChromeDriver")
            return driver
    except Exception as e:
        print(f"System ChromeDriver failed: {e}")
    
    # Strategy 3: Try webdriver-manager with manual path resolution
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        driver_path = ChromeDriverManager().install()
        
        # Find the actual chromedriver executable
        if os.path.exists(driver_path):
            driver_dir = os.path.dirname(driver_path)
            actual_driver_path = None
            
            # Look for the actual chromedriver executable
            for file in os.listdir(driver_dir):
                if file.startswith('chromedriver') and not file.endswith(('.txt', '.md', '.notice')):
                    actual_driver_path = os.path.join(driver_dir, file)
                    break
            
            if actual_driver_path and os.path.isfile(actual_driver_path):
                # Make it executable
                os.chmod(actual_driver_path, 0o755)
                
                options = Options()
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-infobars")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_argument("--blink-settings=imagesEnabled=false")
                options.add_argument("--disable-features=VizDisplayCompositor")
                options.add_argument("--disable-web-security")
                options.add_argument("--allow-running-insecure-content")
                options.add_argument("--disable-features=VizDisplayCompositor")
                options.add_argument("--disable-background-timer-throttling")
                options.add_argument("--disable-backgrounding-occluded-windows")
                options.add_argument("--disable-renderer-backgrounding")
                options.add_argument("--disable-features=TranslateUI")
                options.add_argument("--disable-ipc-flooding-protection")
                
                service = Service(actual_driver_path)
                driver = webdriver.Chrome(service=service, options=options)
                print("Using webdriver-manager ChromeDriver")
                return driver
    except Exception as e:
        print(f"WebDriver Manager failed: {e}")
    
    # Strategy 4: Manual installation and setup
    try:
        install_chrome_on_railway()
        
        # Try again with system Chrome
        if os.path.exists("/usr/bin/google-chrome-stable"):
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-infobars")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--blink-settings=imagesEnabled=false")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-renderer-backgrounding")
            options.add_argument("--disable-features=TranslateUI")
            options.add_argument("--disable-ipc-flooding-protection")
            
            service = Service("/usr/bin/google-chrome-stable")
            driver = webdriver.Chrome(service=service, options=options)
            print("Using manually installed Chrome")
            return driver
    except Exception as e:
        print(f"Manual installation failed: {e}")
    
    raise Exception("All Chrome driver strategies failed")

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
    
    # Try multiple selectors for tab content
    tab_content = None
    selectors_to_try = [
        'pre',  # Original format
        '.js-tab-content',  # Modern UG format
        '.tab-content',  # Alternative modern format
        '[data-content="tab"]',  # Data attribute format
        '.chord-content',  # Chord-specific content
        '.tab-text',  # Tab text format
        '#tab-content',  # ID-based format
        '.js-tab',  # JavaScript tab format
        '.tab-body',  # Tab body format
        '.content-body',  # Generic content body
        '.tab',  # Generic tab class
        '.chords',  # Chords class
        '.lyrics',  # Lyrics class
    ]
    
    for selector in selectors_to_try:
        tab_content = soup.select_one(selector)
        if tab_content:
            print(f"Found tab content using selector: {selector}")
            break
    
    # If no specific selector worked, try to find any content that looks like a tab
    if tab_content is None:
        # Look for any element containing tab-like content
        for element in soup.find_all(['div', 'pre', 'span', 'p']):
            text = element.get_text()
            if text and len(text) > 50:
                # Check if it contains chord-like patterns
                chord_pattern = re.compile(r'[A-G][#b]?(m|maj|min|dim|aug|sus[24]?|add\d*|maj7|m7|7|6|9|11|13)?')
                if chord_pattern.search(text):
                    tab_content = element
                    print(f"Found tab content in element: {element.name}")
                    break
    
    if tab_content is None:
        # Last resort: try to extract any text content that might be a tab
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
        if main_content:
            tab_content = main_content
            print("Using main content as fallback")
        else:
            return {'error': 'Could not find tab content in the page. The page structure may have changed or the content is not accessible.'}
    
    tab = UltimateTab()
    tab_text = tab_content.get_text('\n')  # Get all text, preserving newlines
    lines = tab_text.splitlines()
    
    # Filter out empty lines and clean up
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line and len(line) > 0:
            # Filter out metadata lines that interfere with alignment
            # Skip lines that are just metadata (brackets, capo info, etc.)
            if (line.startswith('[') and line.endswith(']')) or \
               line.lower().startswith('capo') or \
               line.lower().startswith('tuning') or \
               line.lower().startswith('key:') or \
               line.lower().startswith('difficulty:') or \
               line.lower().startswith('author:') or \
               line.lower().startswith('transpose:') or \
               line.lower().startswith('chords:') or \
               line.lower().startswith('intro') or \
               line.lower().startswith('verse') or \
               line.lower().startswith('chorus') or \
               line.lower().startswith('bridge') or \
               line.lower().startswith('outro'):
                continue
            cleaned_lines.append(line)
    
    # More sophisticated parsing: look for patterns
    i = 0
    while i < len(cleaned_lines):
        line = cleaned_lines[i]
        
        if not line:
            tab.append_blank_line()
            i += 1
            continue
        
        # Check if this line looks like a chord line
        if is_chord_line(line):
            # Look ahead to see if there's a lyric line following this chord line
            if i + 1 < len(cleaned_lines) and not is_chord_line(cleaned_lines[i + 1]):
                # We have a chord line followed by a lyric line
                chord_line = line
                lyric_line = cleaned_lines[i + 1]
                
                # Calculate chord positions relative to the lyric line
                chords = []
                import re
                chord_pattern = r'([A-Za-z0-9#/]+)'
                chord_matches = list(re.finditer(chord_pattern, chord_line))
                
                for match in chord_matches:
                    chord_text = match.group(1)
                    # Calculate position relative to the lyric line
                    chord_pos = match.start()
                    leading_spaces = chord_pos
                    
                    chord = {
                        'note': chord_text,
                        'pre_spaces': leading_spaces
                    }
                    chords.append(chord)
                
                # Create a combined line with both chords and lyrics
                combined_line = {
                    'chords': chords,
                    'lyric': lyric_line
                }
                tab.lines.append(combined_line)
                
                i += 2  # Skip both chord and lyric lines
            else:
                # Just a chord line without following lyric
                tab.append_chord_line(line)
                i += 1
        else:
            # This is a lyric line without preceding chord line
            tab.append_lyric_line(line)
            i += 1
            
            # Add blank line after each paragraph/verse for better readability
            # Check if next line is a chord line (indicating new verse/section)
            if i < len(cleaned_lines) and is_chord_line(cleaned_lines[i]):
                tab.append_blank_line()
    
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
    """Get rendered HTML with robust error handling"""
    driver = None
    try:
        driver = get_chrome_driver()
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)
        
        # Configure Chrome for better performance
        driver.execute_cdp_cmd("Network.enable", {})
        driver.execute_cdp_cmd("Network.setBlockedURLs", {
            "urls": ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.css", "*.woff", "*.ttf", "*.svg"]
        })
        
        start = time.time()
        driver.get(url)
        
        # Wait for content to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Wait for tab content to appear (try multiple selectors)
        tab_selectors = [
            'pre',
            '.js-tab-content',
            '.tab-content',
            '[data-content="tab"]',
            '.chord-content',
            '.tab-text',
            '#tab-content',
            '.js-tab',
            '.tab-body',
            '.content-body',
            '.tab',
            '.chords',
            '.lyrics'
        ]
        
        tab_found = False
        for selector in tab_selectors:
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                print(f"Found tab content with selector: {selector}")
                tab_found = True
                break
            except:
                continue
        
        # If no specific selector found, wait a bit more for dynamic content
        if not tab_found:
            print("No specific tab selector found, waiting for dynamic content...")
            time.sleep(5)
        
        # Additional wait for any JavaScript content
        time.sleep(3)
        
        html = driver.page_source
        print(f"[Timing] Selenium fetch time: {time.time() - start:.2f}s")
        
        if not html or len(html.strip()) < 100:
            raise Exception("Empty or too short HTML response")
        
        return html
        
    except Exception as e:
        print(f"[Error] Selenium page load failed: {e}")
        return ""
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

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
        resp = session.get(url, timeout=15)  # Increased timeout
        resp.raise_for_status()
        print(f"[Timing] requests fetch time: {time.time() - start:.2f}s")
        return resp.text
    except Exception as e:
        print(f"[Error] requests fetch failed: {e}")
        return ""
