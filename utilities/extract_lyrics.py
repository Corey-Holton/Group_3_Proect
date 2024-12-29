from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator
from pathlib import Path
import torch
from .print_utilities import print_title, print_message

# Determine device and compute type based on availability.
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
COMPUTE_TYPE = "int8_float16" if DEVICE == "cuda" else "int8"
MODEL_SIZE = "large-v3"

# Initialize Whisper model globally to avoid reloading it multiple times.
MODEL = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)


def extract_lyrics(audio_file):
    """
    Extract lyrics from an audio file using the Whisper model.

    :param audio_file: Path to the audio file.
    :return: List of lyrics strings.
    """
    audio_file = Path(audio_file)

    print_title("Extracting Lyrics from Audio", text_color="bright_white")

    print_message("[INFO] Model Configuration", text_color="bright_blue")
    print_message(f"Device: \t{DEVICE}", text_color="bright_blue", indent_level=1)
    print_message(f"Compute Type: \t{COMPUTE_TYPE}", text_color="bright_blue", indent_level=1)
    print_message(f"Model Size: \t{MODEL_SIZE}", text_color="bright_blue", indent_level=1, include_border=True)

    print_message("[INFO] Processing Audio File", text_color="bright_blue")
    print_message(f"`{audio_file.name}`", text_color="bright_blue", indent_level=1, include_border=True)

    # Transcribe audio file.
    segments, info = MODEL.transcribe(audio_file, beam_size=1)

    print_message("[TRANSCRIPTION DETAILS]", text_color="bright_cyan")
    print_message(f"Detected Language: \t{info.language}", text_color="bright_cyan", indent_level=1)
    print_message(f"Language Probability: \t{info.language_probability:.2f}", text_color="bright_cyan", indent_level=1, include_border=True)

    # Collect and return lyrics.
    lyrics = [segment.text for segment in segments]
    return lyrics


def translate_lyrics(lyrics, target_language):
    """
    Translate extracted lyrics into the target language.

    :param lyrics: List of strings representing lyrics.
    :param target_language: Target language code (e.g., 'en' for English).
    :return: List of translated lyrics strings.
    """
    print_title("Translating Lyrics", text_color="bright_white")
    translator = GoogleTranslator(target=target_language)

    return [translator.translate(line) for line in lyrics]


def get_available_languages():
    """
    Retrieve available language codes and names for translation.
    
    :return: dictionary of language names and codes.
    """
    # Get languages as a dictionary from GoogleTranslator
    g_translator = GoogleTranslator()
    language_dict = g_translator.get_supported_languages(as_dict=True)
    return language_dict