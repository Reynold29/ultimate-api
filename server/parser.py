import json
from bs4 import BeautifulSoup
from .tab import UltimateTab, UltimateTabInfo
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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
    # A line is a chord line if it contains only chord names and spaces
    # This is a naive check; you may want to improve it for your use case
    chord_pattern = re.compile(r'^([A-G][#b]?m?(maj7|sus4|dim|aug|add\d*)?\s*)+$')
    return bool(chord_pattern.match(line.strip()))

def html_tab_to_json_dict(html_body: str, pre_class_tags: [str]) -> json:
    '''
    Returns a json form of a 'pre' tag in an ultimate guitar html tabs body.

    Parameters:
        - html_body: The full html body of an ultimate guitar tab site
        - pre_class_tags: (unused in new version)
    '''
    soup = BeautifulSoup(html_body, "html.parser")

    # Get UltimateTabInfo object from soup html for artist, title, etc.
    tab_info = _tab_info_from_soup(soup)

    # Find the first <pre> tag containing the tab content
    pre_tag = soup.find('pre')
    if pre_tag is None:
        return {'error': 'Could not find <pre> tag with tab content in the page. The page structure may have changed.'}

    tab = UltimateTab()
    tab_text = pre_tag.get_text('\n')  # Get all text, preserving newlines

    for line in tab_text.splitlines():
        if not line.strip():
            tab.append_blank_line()
        elif is_chord_line(line):
            tab.append_chord_line(line)
        else:
            tab.append_lyric_line(line)

    # Construct full json object
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
    return {'tab': json_obj}

def get_rendered_html(url):
    options = Options()
    options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html
