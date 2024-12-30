import warnings
import logging
import os
import random

# ════════════════════════════════════════════════════════════
# Suppress Warnings and Logging
# ════════════════════════════════════════════════════════════
warnings.filterwarnings("ignore", category=UserWarning, message="Coremltools is not installed.")
warnings.filterwarnings("ignore", category=UserWarning, message="tflite-runtime is not installed.")
warnings.filterwarnings("ignore", category=DeprecationWarning, message="The name tf.losses.sparse_softmax_cross_entropy is deprecated.")

logging.getLogger("root").setLevel(logging.ERROR)
logging.getLogger("tensorflow").setLevel(logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# ════════════════════════════════════════════════════════════
# Imports
# ════════════════════════════════════════════════════════════
# Third-party Imports
import gradio as gr

# Local Imports
from utilities import (
    process_audio_stem_separation,
    process_audio_to_midi_conversion,
    process_audio_lyric_extraction,
    process_audio_lyric_translation,
    get_available_languages,
    process_midi_style_conversion,
)

# ════════════════════════════════════════════════════════════
# Gradio Interface 1: Audio Separation
# ════════════════════════════════════════════════════════════
def create_audio_separation_interface():
    with gr.Blocks() as interface:
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Audio Input")
                audio_input = gr.Audio(type="filepath", label="Upload Audio File", sources="upload")
                process_button = gr.Button("Separate Audio")

            with gr.Column(scale=1):
                gr.Markdown("### Parameters")
                model = gr.Textbox(value="htdemucs_ft", label="Demucs Model", placeholder="htdemucs_ft")
                save_as_mp3 = gr.Checkbox(label="Save as MP3?", value=True)
                mp3_bitrate = gr.Slider(minimum=60, maximum=600, step=20, value=320, label="MP3 Bitrate (kbps)")
                use_float32 = gr.Checkbox(label="32-bit Float Output?", value=False)
                use_int24 = gr.Checkbox(label="24-bit Integer Output?", value=False)

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Audio Outputs")
                instrumental_output = gr.Audio(label="Instrumental")
                vocal_output = gr.Audio(label="Vocals")
                bass_output = gr.Audio(label="Bass")
                drum_output = gr.Audio(label="Drums")

        process_button.click(
            process_audio_stem_separation,
            inputs=[audio_input, model, save_as_mp3, mp3_bitrate, use_float32, use_int24],
            outputs=[instrumental_output, vocal_output, bass_output, drum_output],
        )
    return interface

# ════════════════════════════════════════════════════════════
# Gradio Interface 2: Audio to MIDI Conversion
# ════════════════════════════════════════════════════════════
def create_audio_to_midi_interface():
    with gr.Blocks() as interface:
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Audio Input")
                audio_input = gr.Audio(type="filepath", label="Upload Audio File", sources="upload")
                song_directory = gr.Textbox(label="Song Directory Name", placeholder="Enter a song directory name.", value=f"song_{random.randint(1000, 9999)}")
                process_button = gr.Button("Convert to MIDI")

                gr.Markdown("### MIDI Output")
                midi_output = gr.Audio(label="MIDI")

            with gr.Column(scale=1):
                gr.Markdown("### Parameters")
                save_midi = gr.Checkbox(label="Save MIDI File?", value=True)
                generate_audio_from_midi = gr.Checkbox(label="Sonify MIDI?", value=False)
                save_model_outputs = gr.Checkbox(label="Save Model Outputs?", value=False)
                # save_notes = gr.Checkbox(label="Save Notes?", value=False)
                onset_threshold = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, value=0.5, label="Onset Threshold")
                frame_threshold = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, value=0.3, label="Frame Threshold")
                min_note_length = gr.Slider(minimum=10, maximum=500, step=10, value=127.7, label="Minimum Note Length (ms)")
                min_frequency = gr.Number(label="Minimum Frequency (Hz)", value=None)
                max_frequency = gr.Number(label="Maximum Frequency (Hz)", value=None)
                allow_multiple_pitch_bends = gr.Checkbox(label="Allow Multiple Pitch Bends?", value=False)
                apply_melodia_trick = gr.Checkbox(label="Apply Melodia Trick?", value=True)
                samplerate = gr.Number(label="Samplerate (Hz)", value=44100)
                midi_tempo = gr.Number(label="MIDI Tempo (BPM)", value=120)

        process_button.click(
            process_audio_to_midi_conversion,
            inputs=[
                audio_input, song_directory, save_midi, generate_audio_from_midi, save_model_outputs, onset_threshold,
                frame_threshold, min_note_length, min_frequency, max_frequency, allow_multiple_pitch_bends,
                apply_melodia_trick, samplerate, midi_tempo
            ],
            outputs=[midi_output],
        )
    return interface

# ════════════════════════════════════════════════════════════
# Gradio Interface 3: Modify MIDI File
# ════════════════════════════════════════════════════════════
def create_modify_midi_interface():
    with gr.Blocks() as interface:
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### MIDI Input")
                midi_input = gr.Audio(type="filepath", label="Upload MIDI File", sources="upload")
                song_dir_name = gr.Textbox(label="Song Directory Name", placeholder="Enter a song directory name.", value=f"song_{random.randint(1000, 9999)}")
                song_prefix_name = gr.Textbox(label="Song Prefix Name", placeholder="Enter a song prefix name.", value=f'{random.randint(1000, 9999)}')
                process_button = gr.Button("Modify MIDI")

            with gr.Column(scale=1):
                gr.Markdown("### Parameters")
                prompt = gr.Textbox(label="Prompt", placeholder="Enter a prompt here.")

                gr.Markdown("### MIDI Output")
                modified_midi_output = gr.Audio(label="Modified MIDI")

        process_button.click(
            process_midi_style_conversion,
            inputs=[midi_input, song_dir_name, song_prefix_name, prompt],
            outputs=[modified_midi_output],
        )
    return interface


# ════════════════════════════════════════════════════════════
# Gradio Interface 4: Extract and Translate Lyrics
# ════════════════════════════════════════════════════════════
def create_lyrics_interface():
    with gr.Blocks() as interface:
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Audio Input")
                audio_input = gr.Audio(type="filepath", label="Upload Audio File", sources="upload")
                extract_button = gr.Button("Extract Lyrics")

            with gr.Column(scale=1):
                gr.Markdown("### Lyrics Output")
                lyrics_output = gr.Textbox(label="Lyrics")

                gr.Markdown("### Translate Lyrics")
                language_code = gr.Dropdown(choices=get_available_languages(), label="Language", interactive=True)
                translated_output = gr.Textbox(label="Translated Lyrics")
                translate_button = gr.Button("Translate")

        extract_button.click(
            process_audio_lyric_extraction,
            inputs=[audio_input],
            outputs=[lyrics_output],
        )

        translate_button.click(
            process_audio_lyric_translation,
            inputs=[lyrics_output, language_code],
            outputs=[translated_output],
        )
    return interface


# ════════════════════════════════════════════════════════════
# Gradio Interface 5: External Website Tab
# ════════════════════════════════════════════════════════════
def create_external_website_interface():
    with gr.Blocks() as interface:
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown(
                    "### Visit [SpessaSynth](https://spessasus.github.io/SpessaSynth/), [Midiano](https://app.midiano.com/), [html-midi-player](https://cifkao.github.io/html-midi-player/)",
                    elem_id="spessasynth-header",
                )

                gr.HTML(
                    """
                    <iframe 
                        src="https://spessasus.github.io/SpessaSynth/" 
                        width="100%" 
                        height="800px");">
                    </iframe>
                    """
                )

    return interface


# ════════════════════════════════════════════════════════════
# Main Interface Setup
# ════════════════════════════════════════════════════════════
audio_separation_interface = create_audio_separation_interface()
audio_to_midi_interface = create_audio_to_midi_interface()
modify_midi_interface = create_modify_midi_interface()
lyrics_interface = create_lyrics_interface()
external_website_interface = create_external_website_interface()

tabbed_interface = gr.TabbedInterface(
    [
        audio_separation_interface,
        audio_to_midi_interface,
        modify_midi_interface,
        lyrics_interface,
        external_website_interface,
    ],
    tab_names=[
        "Audio Separation",
        "Audio to MIDI",
        "Modify MIDI",
        "Lyrics Extraction",
        "SpessaSynth Website",
    ],
    theme="shivi/calm_seafoam",
)

tabbed_interface.launch()