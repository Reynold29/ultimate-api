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

        # Try to find a matching URL from our predefined list
        matching_url = find_song_url(song_name, artist_name)
        
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

def find_song_url(song_name, artist_name=''):
    """
    Find a song URL from a predefined list of popular songs
    """
    # Predefined list of popular songs with their Ultimate Guitar URLs
    popular_songs = {
        'wonderwall': {
            'url': 'https://tabs.ultimate-guitar.com/tab/oasis/wonderwall-190475',
            'artist': 'Oasis',
            'title': 'Wonderwall'
        },
        'what an awesome god': {
            'url': 'https://tabs.ultimate-guitar.com/tab/phil-wickham/what-an-awesome-god-chords-5749718',
            'artist': 'Phil Wickham',
            'title': 'What an Awesome God'
        },
        'shape of you': {
            'url': 'https://tabs.ultimate-guitar.com/tab/ed-sheeran/shape-of-you-1956589',
            'artist': 'Ed Sheeran',
            'title': 'Shape of You'
        },
        'let it be': {
            'url': 'https://tabs.ultimate-guitar.com/tab/beatles/let-it-be-277709',
            'artist': 'The Beatles',
            'title': 'Let It Be'
        },
        'hotel california': {
            'url': 'https://tabs.ultimate-guitar.com/tab/eagles/hotel-california-2355357',
            'artist': 'Eagles',
            'title': 'Hotel California'
        },
        'stairway to heaven': {
            'url': 'https://tabs.ultimate-guitar.com/tab/led-zeppelin/stairway-to-heaven-5434176',
            'artist': 'Led Zeppelin',
            'title': 'Stairway to Heaven'
        }
    }
    
    # Search for matches
    search_terms = [song_name.lower()]
    if artist_name:
        search_terms.append(f"{artist_name.lower()} {song_name.lower()}")
        search_terms.append(f"{song_name.lower()} {artist_name.lower()}")
    
    for term in search_terms:
        for key, song_info in popular_songs.items():
            if term in key or key in term:
                return song_info['url']
    
    return None
