from server import app
from flask import request, jsonify
from urllib.parse import urlparse
from .tab_parser import dict_from_ultimate_tab, grouped_blocks_from_ultimate_tab
import re


SUPPORTED_UG_URI = 'tabs.ultimate-guitar.com'

@app.route('/')
def index():
    return 'The API Server is running'

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
