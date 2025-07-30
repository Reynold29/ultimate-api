from typing import Any

# tab {
#     title: "tab name",
#     artist_name: "",
#     author: "",
#     capo: "" (can be null),
#     Tuning: "" (can be null),
#
#     lines: [
#         {
#          type: "chord" (OR "lyrics", "blank"),
#          chords: [
#             {
#                 note: "G",
#                 pre_spaces: 10
#             },
#             {
#                 note: "Em",
#                 pre_spaces: 8
#             }
#          ]
#         },
#         {
#          type: "lyrics",
#          lyrics: "I found a love for me"
#         },
#         {
#          type: "blank"
#         }
#     ]
# }

class UltimateTabInfo(object):
    '''
    Represents the info of an ultimate guitar tab. Does not contain any lyrics or chords
    '''

    def __init__(self, title: str, artist: str, author: str, difficulty: str = None, key: str = None, capo: str = None, tuning: str = None):
        self.title = title
        self.artist = artist
        self.author = author
        # Optionals:
        self.difficulty = difficulty
        self.key = key
        self.capo = capo
        self.tuning = tuning


class UltimateTab(object):
    '''
    Represents an ultimate guitar tab containing Lyrics and Chords

    A `queue-like` object which will append lines to object
    and can be parsed to formatted json.
    '''

    JSON_CONTAINER_NAME  = 'lines'
    JSON_KEY_CHORD_ARRAY = 'chords'
    JSON_KEY_NOTE        = 'note'
    JSON_KEY_LYRIC       = 'lyric'
    JSON_KEY_BLANK       = 'blank'
    JSON_KEY_TYPE        = 'type'
    JOSN_KEY_LEAD_SPACES = 'pre_spaces'

    def __init__(self):
        self.lines = []


    def _append_new_line(self, type: str, content_tag: str, content: Any) -> None:
        line = {}
        if content_tag is not None:
            line[content_tag] = content

        self.lines.append(line)


    def append_chord_line(self, chords_line: str) -> None:
        '''
        Appends a chord line to the tab.

        Parameters:
            - chords_line: A single-line string containing leading spaces and guitar chords (i.e. G, Em, etc.)
        '''
        chords = [] # Array of dictionary of chords

        # Clean up the line - handle newlines but preserve original spacing
        chords_line = chords_line.replace('\n', ' ').replace('\r', ' ')
        
        # Find all chord positions while preserving spacing
        import re
        # Match chords (letters, numbers, #, /, etc.) separated by spaces
        chord_pattern = r'([A-Za-z0-9#/]+)'
        matches = list(re.finditer(chord_pattern, chords_line))
        
        for i, match in enumerate(matches):
            chord_text = match.group(1)
            # Calculate leading spaces from start of string to this chord
            start_pos = match.start()
            leading_spaces = start_pos
            
            chord = {
                self.JSON_KEY_NOTE: chord_text,
                self.JOSN_KEY_LEAD_SPACES: leading_spaces
            }
            chords.append(chord)

        self._append_new_line(self.JSON_KEY_CHORD_ARRAY, self.JSON_KEY_CHORD_ARRAY, chords)

    def append_lyric_line(self, lyric_line: str) -> None:
        '''
        Appends a lyric line to the tab.

        Parameters:
            - lyric_line: A single-line string containing lyrics (and any leading spaces needed)
        '''
        self._append_new_line(self.JSON_KEY_LYRIC, self.JSON_KEY_LYRIC, lyric_line)

    def append_blank_line(self) -> None:
        '''
        Appends a blank line to the tab.
        '''
        self._append_new_line(self.JSON_KEY_BLANK, None, None)

    def as_json_dictionary(self) -> dict:
        '''
        Returns a dictionary representation of the tab object.
        Properly formatted for use as a json object.
        '''
        return {self.JSON_CONTAINER_NAME: self.lines}
