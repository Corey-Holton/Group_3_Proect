# Local Imports
from .main import _extract_lyrics, _translate_lyrics
from ..print_utilities import print_message


def process_audio_lyric_extraction(
        # ! Parameters here are handled in the Gradio Interface.
        # ! The order of parameters MUST match the Gradio interface to function correctly.
        input_file
    ):
    """
    Extract lyrics from an audio file and return them as a single string.

    Args:
        input_file (str): Path to the audio file.

    Returns:
        str: Extracted lyrics as a single string.
    """

    # Extract lyrics from the audio file
    lyrics = _extract_lyrics(input_file)

    # Print success message
    print_message("[SUCCESS]", text_color="bright_green", include_border=True)

    # Return the extracted lyrics as a single string
    return "\n".join(lyrics)


def process_audio_lyric_translation(
        # ! Parameters here are handled in the Gradio Interface.
        # ! The order of parameters MUST match the Gradio interface to function correctly.
        lyrics, 
        language_code
    ):
    """
    Translate extracted lyrics to the specified language.

    Args:
        lyrics (str): Lyrics to translate.
        language_code (str): Language code to translate to.

    Returns:
        str: Translated lyrics as a single string.
    """

    # Split the lyrics into a list of lines
    lyrics_list = lyrics.split("\n")

    # Translate the lyrics to the specified language
    translated = _translate_lyrics(lyrics_list, language_code)

    # Print success message
    print_message("[SUCCESS]", text_color="bright_green", include_border=True)

    # Return the translated lyrics as a single string
    return "\n".join(translated)

if __name__ == "__main__":
    print("This script is designed to be used as a Gradio interface for audio lyric extraction and translation.")