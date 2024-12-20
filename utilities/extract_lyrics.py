from faster_whisper import WhisperModel
import torch

from deep_translator import GoogleTranslator

device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "int8_float16" if device == "cuda" else "int8"
model_size = "large-v3"

# model = WhisperModel(model_size, device=device, compute_type=compute_type)

# audio_file = "../../Resources/audio_files/big_krit.mp3"
# segments, info = model.transcribe(audio_file, beam_size=1)

def extract_audio_lyrics(audio_file):
    model = WhisperModel(model_size, device=device, compute_type=compute_type)
    segments, info = model.transcribe(audio_file, beam_size=1)
    
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    print(segments)

    lyrics = []
    for segment in segments:
        lyrics.append(str(segment.text))
        print(f'added text to lyrics')
        
    return lyrics

def translate_lyrics(lyrics, target_language):
    """
    Translates a list of lyrics (strings) to the target language.
    
    :param lyrics: List of strings (lines of lyrics) in the original language.
    :param target_language: The target language code (e.g. 'en' for English, 'es' for Spanish).
    :return: List of strings with translated lyrics.
    """
    return [GoogleTranslator(target=target_language).translate(line) for line in lyrics]

# Example usage:
# original_lyrics = ["Bonjour, comment ça va?", "J'aime la musique"]
# translated_to_english = translate_lyrics(original_lyrics, 'en')
# print(translated_to_english)

    
    
