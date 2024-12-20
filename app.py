"""
This script sets up a Gradio interface to process audio files by separating them into stems using the Demucs model
and converting the "other" stem to MIDI using the Basic Pitch model.

Summary:
- The main function `gradio_pipeline` takes an input audio file, separates it into stems, and converts the "other" stem to MIDI.
- The separated audio files and the generated MIDI file are returned as outputs.

Usage:
- Run this script to launch the Gradio interface.
- Upload an audio file and specify the Demucs model to use for separation.
"""

import warnings
import logging
import os

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, message="Coremltools is not installed.")
warnings.filterwarnings("ignore", category=UserWarning, message="tflite-runtime is not installed.")
warnings.filterwarnings("ignore", category=DeprecationWarning, message="The name tf.losses.sparse_softmax_cross_entropy is deprecated.")

# Suppress specific logging warnings
logging.getLogger("root").setLevel(logging.ERROR)
logging.getLogger("tensorflow").setLevel(logging.ERROR)

# Set TensorFlow logging level to suppress informational messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# ══════════════════════════
# Imports
# ══════════════════════════

# Standard Library Imports
from pathlib import Path

# Third-party imports
import gradio as gr

# Local imports
from utilities import separate_audio, audio_to_midi, print_line, extract_lyrics

# ══════════════════════════
# Gradio Pipeline
# ══════════════════════════

def seperate_files(
    input_file,
    # Parameters for `separate_audio`
    model="htdemucs_ft",
    mp3=True,
    mp3_rate=320,
    float32=False,
    int24=False,
):
    """
    
    """
    print("*"*50)
    print(f"Input File: {input_file}")
    print(f"Model: {model}")
    print(f"MP3: {mp3}")
    print(f"MP3 Rate: {mp3_rate}")
    print(f"Float32: {float32}")
    print(f"Int24: {int24}")
    print("*"*50)

    # Output path for audio stems
    output_path_stems = "./audio_processing/output_stems"

    # ══════════════════════════
    # Step 1: Separate Audio Stems using Demucs Model
    # ══════════════════════════
    results = separate_audio(
        input_file,
        output_path=output_path_stems,
        model=model,
        mp3=mp3,
        mp3_rate=mp3_rate,
        float32=float32,
        int24=int24,
    )

    # Check if results are returned
    if results is None:
        return print_line("[ERROR] \n\tNo results returned from `separate_audio`.", text_color="red")

    # Unpack audio stems paths from results
    other_stem_path, voice_stem_path, bass_stem_path, drums_stem_path = results

    # Return the "other" stem path for Gradio output
    return str(other_stem_path), str(voice_stem_path), str(bass_stem_path), str(drums_stem_path)



def output_midi(
    input_file,

    # Parameters for `separate_audio`
    model="htdemucs_ft",
    mp3=True,
    mp3_rate=320,
    float32=False,
    int24=False,

    # Parameters for `audio_to_midi`
    save_midi=True,
    sonify_midi=False,
    save_model_outputs=False,
    onset_threshold=0.5,
    frame_threshold=0.3,
    minimum_note_length=127.70,
    minimum_frequency=None,
    maximum_frequency=None,
    multiple_pitch_bends=False,
    melodia_trick=True,
    sonification_samplerate=44100,
    midi_tempo=120,
):
    """
    Full pipeline function to process audio files by separating them into stems and converting the "other" stem to MIDI.
    """

    # Validate frequency values
    def validate_frequency(value):
        return None if value == 0 else value
    
    minimum_frequency = validate_frequency(minimum_frequency)
    maximum_frequency = validate_frequency(maximum_frequency)

    # Input Song Name
    song_name = Path(input_file).stem

    # Output path for audio stems
    output_path_midi = "./audio_processing/output_midi"
        
    # ══════════════════════════
    # Step 2: Convert "other" stem to MIDI
    # ══════════════════════════
    midi_file_path = audio_to_midi(
        audio_path=input_file,
        output_directory=output_path_midi,
        save_midi=save_midi,
        sonify_midi=sonify_midi,
        save_model_outputs=save_model_outputs,
        save_notes=True,
        onset_threshold=onset_threshold,
        frame_threshold=frame_threshold,
        minimum_note_length=minimum_note_length,
        minimum_frequency=minimum_frequency,
        maximum_frequency=maximum_frequency,
        multiple_pitch_bends=multiple_pitch_bends,
        melodia_trick=melodia_trick,
        sonification_samplerate=sonification_samplerate,
        midi_tempo=midi_tempo,
    )

    # Return both files for Gradio output
    return str(midi_file_path)


def extract_audio(input_file):
    """
    
    """
    print("*"*50)
    print(f"Input File: {input_file}")
    print("*"*50)

    # ══════════════════════════
    # Step 1: Separate Audio Stems using Demucs Model
    lyrics = extract_lyrics.extract_audio_lyrics(input_file)
    # take the list of strings and join them into one string
    lyrics = "\n".join(lyrics)
    # Return the "other" stem path for Gradio output
    return str(lyrics)


def translate_lyrics(lyrics, language):
    """
    
    """
    print("*"*50)
    print(f"Lyrics: {lyrics}")
    print("*"*50)

    # ══════════════════════════
    # Step 1: Separate Audio Stems using Demucs Model
    t = " ".join(extract_lyrics.translate_lyrics(lyrics.split("\n"), language))
    # Return the "other" stem path for Gradio output
    return str(t)


# 1. Seperate audio into stems
# 2. Convert other stem to MIDI

# ══════════════════════════
# Gradio Interface 1
# ══════════════════════════
with gr.Blocks(theme="shivi/calm_seafoam") as interface:
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Audio Input")
            audio_input = gr.Audio(type="filepath", label="Upload Audio File", sources="upload")
            process_button = gr.Button("Process Audio")
        
        with gr.Column(scale=1):
            gr.Markdown("### Audio Parameters")
            model = gr.Textbox(value="htdemucs_ft", label='Select Demucs Model', placeholder="htdemucs_ft", max_lines=1)
            mp3 = gr.Checkbox(label="Save as MP3?", value=True)
            mp3_rate = gr.Slider(minimum=60, maximum=600, step=20, value=320, label="MP3 Bitrate (kbps)")
            float32 = gr.Checkbox(label="Save as 32-bit Float Output?", value=False)
            int24 = gr.Checkbox(label="Save as 24-bit Integer Output?", value=False)
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Audio Outputs")
            output_instrumental_main = gr.Audio(label="Main (Other)")
            output_instrumental_voice = gr.Audio(label="Voice")
            output_instrumental_bass = gr.Audio(label="Bass")
            output_instrumental_drums = gr.Audio(label="Drums")
        

# ══════════════════════════
# Gradio Interface 2
# ══════════════════════════   
with gr.Blocks(theme="shivi/calm_seafoam") as interface_2:
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Audio Input")
            audio_input_2 = gr.Audio(type="filepath", label="Upload Audio File", sources="upload")
            gr.Markdown("### Parameters")
            save_midi = gr.Checkbox(label="Save MIDI File?", value=True)
            sonify_midi = gr.Checkbox(label="Sonify MIDI? (Generate Audio from MIDI)", value=False)
            save_model_outputs = gr.Checkbox(label="Save Model Output?", value=False)
            # save_notes = gr.Checkbox(label="Save Notes?", value=False)
            onset_threshold = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, value=0.5, label="Onset Threshold")
            frame_threshold = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, value=0.3, label="Frame Threshold")
            minimum_note_length = gr.Slider(minimum=10, maximum=500, step=10, value=127.7, label="Minimum Note Length (ms)")
            minimum_frequency = gr.Number(label="Minimum Frequency (Hz)", value=None)
            maximum_frequency = gr.Number(label="Maximum Frequency (Hz)", value=None)
            multiple_pitch_bends = gr.Checkbox(label="Allow Multiple Pitch Bends?", value=False)
            melodia_trick = gr.Checkbox(label="Apply Melodia Trick?", value=True)
            sonification_samplerate = gr.Number(label="Sonification Samplerate (Hz)", value=44100)
            midi_tempo = gr.Number(label="MIDI Tempo (BPM)", value=120)
            button = gr.Button("Process Audio")

        with gr.Column(scale=1):
            gr.Markdown("### Audio Outputs")
            midi = gr.Audio(label="Midi")
            
# ══════════════════════════
# Gradio Interface 3
# ══════════════════════════
with gr.Blocks(theme="shivi/calm_seafoam") as lyrics_interface:
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Audio Input")
            midi_input = gr.Audio(type="filepath", label="Upload Audio File", sources="upload")
            get_lyrics = gr.Button("Extract Lyrics")
        
        with gr.Column(scale=1):
            gr.Markdown("### Audio Outputs")
            lyrics = gr.Textbox(label="Lyrics")
            
            gr.Markdown("### Translated Lyrics")
            do_translate = gr.Button("Translate Lyrics")
            language = gr.Textbox(label="Language Code", placeholder="en")
            translated_lyrics = gr.Textbox(label="Lyrics")
            

    # ══════════════════════════
    # Launch Gradio Interface
    # ══════════════════════════
    get_lyrics.click(
        extract_audio,
        inputs=[
            midi_input,
        ],
        outputs=[lyrics],
    )
    
    do_translate.click(
        translate_lyrics,
        inputs=[
            lyrics,
            language,
        ],
        outputs=[translated_lyrics],
    )
    
    process_button.click(
        seperate_files,
        inputs=[
            audio_input,
            model,
            mp3,
            mp3_rate,
            float32,
            int24,
        ],
        outputs=[output_instrumental_main, output_instrumental_voice, output_instrumental_bass, output_instrumental_drums],
    )
    
    button.click(
        output_midi,
        inputs=[
            audio_input_2,
            model,
            mp3,
            mp3_rate,
            float32,
            int24,
            save_midi,
            sonify_midi,
            save_model_outputs,
            onset_threshold,
            frame_threshold,
            minimum_note_length,
            minimum_frequency,
            maximum_frequency,
            multiple_pitch_bends,
            melodia_trick,
            sonification_samplerate,
            midi_tempo,
        ],
        outputs=[midi],
    )
# Tabbed Interface
tabbed_interface = gr.TabbedInterface([interface, interface_2, lyrics_interface], ["Seperate Audio", "Audio To MIDI", "Extract Lyrics"])

tabbed_interface.launch()


