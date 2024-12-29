# Local Imports
from .main import _extract_lyrics, _translate_lyrics
from ..print_utilities import print_message


def process_audio_lyric_extraction(input_file):
    """
    Extract lyrics from an audio file and return them as a single string.
    """
    lyrics = _extract_lyrics(input_file)
    print_message("[SUCCESS]", text_color="bright_green", include_border=True)
    return "\n".join(lyrics)


def process_audio_lyric_translation(lyrics, language_code):
    """
    Translate extracted lyrics to the specified language.
    """
    lyrics_list = lyrics.split("\n")
    translated = _translate_lyrics(lyrics_list, language_code)
    print_message("[SUCCESS]", text_color="bright_green", include_border=True)
    return "\n".join(translated)