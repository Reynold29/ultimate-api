import sys
import json
import requests
from .parser import html_tab_to_json_dict, get_rendered_html, get_html_requests

def dict_from_ultimate_tab(url: str) -> json:
    '''
    Given a Ultimate Guitar tab url, will return a dictionary representing the
    song along with the song info. Uses requests first, then Selenium as fallback.
    '''
    # Try requests first (faster for static pages)
    html = get_html_requests(url)
    if not html or len(html.strip()) < 100:
        # Fallback to Selenium
        try:
            html = get_rendered_html(url)
            if not html or len(html.strip()) < 100:
                return {'error': 'Failed to fetch tab content from both requests and Selenium methods'}
        except Exception as e:
            return {'error': f'Selenium failed: {str(e)}'}
    
    tab_dict = html_tab_to_json_dict(html)
    return tab_dict


def json_from_ultimate_tab(url: str) -> json:
    '''
    Given a Ultimate Guitar tab url, will return a json object representing the
    song along with the song info
    '''
    tab_dict = dict_from_ultimate_tab(url)
    data = json.dumps(tab_dict, ensure_ascii=False)
    return data


def grouped_blocks_from_ultimate_tab(url: str, max_retries: int = 5) -> list:
    '''
    Tries to fetch and parse the tab using requests first (faster for static pages).
    Only tries Selenium if requests fails to get a valid tab. Returns a list of blocks (lyrics/tabs) or a single error block if all fail.
    '''
    errors = []

    # Try requests first
    html = get_html_requests(url)
    if html and len(html.strip()) >= 100:
        # Check if the HTML contains any tab-related content
        tab_indicators = ['<pre', '.js-tab-content', '.tab-content', 'chord', 'tab', 'lyric']
        has_tab_content = any(indicator in html for indicator in tab_indicators)
        
        if has_tab_content:
            tab_dict = html_tab_to_json_dict(html)
            lines = tab_dict.get('tab', {}).get('lines', [])
            if lines:
                # Create a combined structure that preserves alignment
                combined_lines = []
                for line in lines:
                    if 'lyric' in line and 'chords' in line:
                        # Line has both lyrics and chords - preserve alignment
                        lyric_text = line['lyric']
                        chord_text = ''
                        for chord in line['chords']:
                            chord_text += ' ' * chord.get('pre_spaces', 0) + chord.get('note', '')
                        combined_lines.append({
                            'lyric': lyric_text,
                            'chords': chord_text
                        })
                    elif 'lyric' in line:
                        # Line has only lyrics
                        combined_lines.append({
                            'lyric': line['lyric'],
                            'chords': ''
                        })
                    elif 'chords' in line:
                        # Line has only chords - preserve original spacing
                        chord_text = ''
                        for chord in line['chords']:
                            # Add the exact number of spaces from the original tab
                            chord_text += ' ' * chord.get('pre_spaces', 0) + chord.get('note', '')
                        combined_lines.append({
                            'lyric': '',
                            'chords': chord_text
                        })
                    else:
                        # Empty line
                        combined_lines.append({
                            'lyric': '',
                            'chords': ''
                        })
                
                # Remove trailing empty lines
                while combined_lines and not combined_lines[-1]['lyric'].strip() and not combined_lines[-1]['chords'].strip():
                    combined_lines.pop()
                
                return [{'combined': combined_lines}]
            else:
                errors.append("requests returned no tab lines")
        else:
            errors.append("requests returned HTML without tab content (likely dynamic content)")
    else:
        if not html:
            errors.append("requests returned empty HTML")
        elif len(html.strip()) < 100:
            errors.append("requests returned too short HTML")
        else:
            errors.append("requests returned HTML without tab content (likely dynamic content)")

    # Only try Selenium if requests failed
    for attempt in range(max_retries):
        try:
            html = get_rendered_html(url)
            if not html or len(html.strip()) < 100:
                errors.append(f"Selenium returned empty/invalid HTML (attempt {attempt+1})")
                continue
            tab_dict = html_tab_to_json_dict(html)
            lines = tab_dict.get('tab', {}).get('lines', [])
            if lines:
                # Create a combined structure that preserves alignment
                combined_lines = []
                for line in lines:
                    if 'lyric' in line and 'chords' in line:
                        # Line has both lyrics and chords - preserve alignment
                        lyric_text = line['lyric']
                        chord_text = ''
                        for chord in line['chords']:
                            chord_text += ' ' * chord.get('pre_spaces', 0) + chord.get('note', '')
                        combined_lines.append({
                            'lyric': lyric_text,
                            'chords': chord_text
                        })
                    elif 'lyric' in line:
                        # Line has only lyrics
                        combined_lines.append({
                            'lyric': line['lyric'],
                            'chords': ''
                        })
                    elif 'chords' in line:
                        # Line has only chords - preserve original spacing
                        chord_text = ''
                        for chord in line['chords']:
                            # Add the exact number of spaces from the original tab
                            chord_text += ' ' * chord.get('pre_spaces', 0) + chord.get('note', '')
                        combined_lines.append({
                            'lyric': '',
                            'chords': chord_text
                        })
                    else:
                        # Empty line
                        combined_lines.append({
                            'lyric': '',
                            'chords': ''
                        })
                
                # Remove trailing empty lines
                while combined_lines and not combined_lines[-1]['lyric'].strip() and not combined_lines[-1]['chords'].strip():
                    combined_lines.pop()
                
                return [{'combined': combined_lines}]
            else:
                errors.append(f"Selenium returned no tab lines (attempt {attempt+1})")
        except Exception as e:
            errors.append(f"Selenium failed (attempt {attempt+1}): {str(e)}")
            continue

    # If all attempts failed, return detailed error
    return [{'error': f"Failed to fetch and parse tab after requests and {max_retries} Selenium attempts. Errors: {'; '.join(errors)}"}]


if __name__ == '__main__':
    try:
        url = sys.argv[1]
    except:
        print('INCORRECT USAGE\n')
        print('  Usage:')
        print('    python %s {url}' % sys.argv[0])
        sys.exit()

    # json_data = json_from_ultimate_tab(url)
    # pretty_format_json = json.dumps(json.loads(json_data), indent=4, sort_keys=True)
    # print(pretty_format_json)

    # For demo: print grouped blocks
    blocks = grouped_blocks_from_ultimate_tab(url)
    print(json.dumps(blocks, indent=2, ensure_ascii=False))
