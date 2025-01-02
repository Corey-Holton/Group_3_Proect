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
    process_audio_extract_lyric_timing, 
    load_lyrics_metadata,
    save_modified_lyrics,
    process_audio_merging,
    process_karaoke_creation,
    get_font_list,
    get_available_colors,
)

# ════════════════════════════════════════════════════════════
# Gradio Interface 1: Audio Separation
# ════════════════════════════════════════════════════════════
def create_audio_separation_interface():
    with gr.Blocks() as interface:
        with gr.Row():
            gr.Markdown("## Separate Audio into Stems using AI")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Upload an audio file to separate into `vocals`, `instrumental`, `bass`, and `drums`.")
                audio_input = gr.Audio(type="filepath", label="Upload Audio File", sources="upload")
                process_button = gr.Button("Separate Audio")
                
            with gr.Column(scale=1):
                gr.Markdown("### Parameters for audio separation using the AI model.")
                model = gr.Textbox(value="htdemucs_ft", label="Demucs Model", placeholder="htdemucs_ft")
                save_as_mp3 = gr.Checkbox(label="Save as MP3?", value=True)
                mp3_bitrate = gr.Slider(minimum=60, maximum=600, step=20, value=320, label="MP3 Bitrate (kbps)")
                use_float32 = gr.Checkbox(label="32-bit Float Output?", value=False)
                use_int24 = gr.Checkbox(label="24-bit Integer Output?", value=False)

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Stem audio outputs.")
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
            gr.Markdown("## Convert an Audio File into `MIDI` format using AI")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Upload an audio file to convert to `MIDI`.")
                audio_input = gr.Audio(type="filepath", label="Upload Audio File", sources="upload")
                gr.Markdown("### Name the output `MIDI` parent folder. (Example: `song_name`)")
                song_directory = gr.Textbox(label="`MIDI` Directory Name", placeholder="Enter a song directory name.", value=f"song_{random.randint(1000, 9999)}")
                process_button = gr.Button("Convert to MIDI")
                gr.Markdown("### `MIDI` file output.")
                midi_output = gr.Audio(label="MIDI")

            with gr.Column(scale=1):
                gr.Markdown("### Parameters for audio to `MIDI` conversion for the AI model.")
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
            gr.Markdown("## Modify an Existing `MIDI` File using AI")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Upload a `MIDI` file to modify.")
                midi_input = gr.Audio(type="filepath", label="Upload MIDI File", sources="upload")

            with gr.Column(scale=1):
                gr.Markdown("### Name the output `MIDI` parent folder. (Example: `song_name`)")
                song_dir_name = gr.Textbox(label="`MIDI` Directory Name", placeholder="Enter a song directory name.", value=f"song_{random.randint(1000, 9999)}")
                gr.Markdown("### Prefix name for the modified `MIDI` file. (Example: `rock_and_roll`)")
                song_prefix_name = gr.Textbox(label="`MIDI` Prefix Name", placeholder="Enter a song prefix name.", value=f'{random.randint(1000, 9999)}')

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Text prompt for the AI model.")
                prompt = gr.Textbox(label="Prompt", placeholder="Enter a prompt here.")

        with gr.Row():
            with gr.Column(scale=1):
                process_button = gr.Button("Modify MIDI")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Modified `MIDI` output file.")
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
            gr.Markdown("## Extract Lyrics for Translation")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Upload `vocals` audio file.")
                audio_input = gr.Audio(type="filepath", label="Upload Audio File", sources="upload")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Lyrics extraction output.")
                lyrics_output = gr.Textbox(label="Lyrics")
                extract_button = gr.Button("Extract Lyrics")

            with gr.Column(scale=1):
                gr.Markdown("### Translated lyrics output.")
                language_code = gr.Dropdown(choices=get_available_languages(), label="Select a Language", interactive=True)
                translated_output = gr.Textbox(label="Translated Lyrics")
                translate_button = gr.Button("Translate Lyrics")

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
# Gradio Interface 6 Sub-Interface 1: Extract Lyrics MetaData
# ════════════════════════════════════════════════════════════
def create_lyric_extraction_interface():
    with gr.Blocks() as interface:
        with gr.Row():
            gr.Markdown("## Extract Lyrics for Karaoke")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Upload `vocals` audio file.")
                audio_input = gr.Audio(type="filepath", label="Vocals Audio File", sources="upload")
                gr.Markdown("### Name the output file. (Example: `song_name`)")
                name_file = gr.Textbox(label="Output File Name", placeholder="Enter a name for the file without an extension.")
                extract_button = gr.Button("Extract Lyrics")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Lyric data saved file path.")
                metadata_output = gr.Textbox(label="Raw Metadata File Path", interactive=False)
                gr.Markdown("### Lyric data output.")
                metadata_output_json = gr.JSON(label="Extracted Metadata")

        extract_button.click(
            process_audio_extract_lyric_timing,
            inputs=[audio_input, name_file],
            outputs=[metadata_output, metadata_output_json],
        )

    return interface

# ════════════════════════════════════════════════════════════
# Gradio Interface 6 Sub-Interface 2: Modify Lyrics Metadata
# ════════════════════════════════════════════════════════════
def create_lyric_modification_interface():
    with gr.Blocks() as interface:
        with gr.Row():
            gr.Markdown("## Modify Lyrics for Karaoke")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Upload `.json` lyrics metadata file.")
                metadata_input = gr.File(label="Raw Metadata JSON", file_types=[".json"])
                load_button = gr.Button("Load Metadata")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Edit words or timing of the lyrics in the metadata.")
                words_table = gr.Dataframe(
                    headers=["Verse Number", "Word Number", "Word", "Start Time", "End Time", "Probability"],
                    datatype=["number", "number", "str", "number", "number", "number"],
                    interactive=True
                )
                save_button = gr.Button("Modifiy Lyrics")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Modified lyric data saved file path.")
                modified_metadata_output = gr.Textbox(label="Modified Metadata File Path", interactive=False)
                gr.Markdown("### Modified lyric data output.")
                metadata_output_json = gr.JSON(label="Extracted Metadata")

        # Actions
        def load_and_display_metadata(metadata_file):
            return load_lyrics_metadata(metadata_file)

        load_button.click(
            load_and_display_metadata,
            inputs=[metadata_input],
            outputs=[words_table],
        )

        def save_metadata(metadata_file, modified_words):
            return save_modified_lyrics(metadata_file, modified_words)

        save_button.click(
            save_metadata,
            inputs=[metadata_input, words_table],
            outputs=[modified_metadata_output, metadata_output_json],
        )

    return interface

# ════════════════════════════════════════════════════════════
# Gradio Interface 6 Sub-Interface 3: Process Audio Merging
# ════════════════════════════════════════════════════════════
def create_audio_merging_interface():
    with gr.Blocks() as interface:
        with gr.Row():
            gr.Markdown("## Create Audio for Karaoke")
            
        with gr.Row():
            gr.Markdown("### Merge `bass`, `drums`, and `other` audio stems.")

        with gr.Row():
            with gr.Column(scale=1):
                bass_input = gr.Audio(type="filepath", label="Bass Stem", sources="upload")
            with gr.Column(scale=1):
                drums_input = gr.Audio(type="filepath", label="Drums Stem", sources="upload")
            with gr.Column(scale=1):
                other_input = gr.Audio(type="filepath", label="Other Stem", sources="upload")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Name the output file. (Example: `song_name`)")
                name_file = gr.Textbox(label="Output File Name", placeholder="Enter a name for the file without an extension.")
                fuse_button = gr.Button("Merge Stems")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Merged Audio Output")
                fused_output = gr.Audio(label="Merged Audio")

        fuse_button.click(
            process_audio_merging,
            inputs=[bass_input, drums_input, other_input, name_file],
            outputs=[fused_output],
        )

    return interface

# ════════════════════════════════════════════════════════════
# Gradio Interface 6 Sub-Interface 4: Process Karaoke Creation
# ════════════════════════════════════════════════════════════
def create_karaoke_creation_interface():
    """
    Interface for creating a karaoke video by uploading instrumental audio and lyrics metadata.
    """
    available_fonts = get_font_list()
    available_colors = get_available_colors()

    with gr.Blocks() as interface:
        with gr.Row():
            gr.Markdown("## Create Karaoke Video")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Upload audio file for the karaoke video.")
                instrumental_audio = gr.Audio(type="filepath", label="Instrumental Audio", sources="upload")
                gr.Markdown("### Upload the lyrics metadata file for the karaoke video.")
                lyrics_metadata = gr.File(label="Lyrics Metadata (JSON)", file_types=[".json"])
                gr.Markdown("### Name the output file. (Example: `song_name`)")
                file_name = gr.Textbox(label="Output File Name", placeholder="Enter a name for the file without an extension.")

            with gr.Column(scale=1):
                gr.Markdown("### Select parameters for the karaoke lyrics being displayed.")
                font = gr.Dropdown(choices=available_fonts, value="Arial", label="Font")
                fontsize = gr.Slider(minimum=8, maximum=36, step=1, value=13, label="Font Size")
                primary_color = gr.Dropdown(choices=available_colors, value="White", label="Primary Color (Text)", interactive=True)
                secondary_color = gr.Dropdown(choices=available_colors, value="Yellow", label="Secondary Color (Highlight)", interactive=True)
                title = gr.Textbox(label="Video Title", value="Karaoke Title", placeholder="Title of the video")

                gr.Markdown("### Select parameters for the karaoke video to be created.")
                resolution = gr.Dropdown(
                    choices=["1280x720", "1920x1080", "640x480"],
                    value="1280x720",
                    label="Resolution"
                )
                preset = gr.Dropdown(
                    choices=["ultrafast", "fast", "medium", "slow"],
                    value="fast",
                    label="FFmpeg Preset"
                )
                crf = gr.Slider(minimum=0, maximum=51, step=1, value=23, label="CRF (Video Quality)")
                fps = gr.Slider(minimum=15, maximum=60, step=1, value=24, label="Frames per Second")
                bitrate = gr.Textbox(label="Video Bitrate", value="3000k", placeholder="e.g., 3000k")
                audio_bitrate = gr.Textbox(label="Audio Bitrate", value="192k", placeholder="e.g., 192k")

        with gr.Row():
            with gr.Column(scale=1):
                process_button = gr.Button("Create Karaoke Video")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Output Karaoke Video")
                output_video = gr.Video(label="Karaoke Video", interactive=False)
                
        # Action: Process Karaoke Creation
        process_button.click(
            process_karaoke_creation,
            inputs=[
                instrumental_audio,
                lyrics_metadata,
                file_name,
                font,
                fontsize,
                primary_color,
                secondary_color,
                title,
                resolution,
                preset,
                crf,
                fps,
                bitrate,
                audio_bitrate,
            ],
            outputs=[output_video],
        )

    return interface

# ════════════════════════════════════════════════════════════
# Main Karaoke Sub-Tabbed Interface 6: Karaoke Features
# ════════════════════════════════════════════════════════════
def create_karaoke_subtabs():
    # Sub-tabs for Karaoke features
    lyric_extraction_interface = create_lyric_extraction_interface()
    lyric_modification_interface = create_lyric_modification_interface()
    audio_merging_interface = create_audio_merging_interface()
    karaoke_creation_interface = create_karaoke_creation_interface()

    karaoke_subtabs = gr.TabbedInterface(
        [
            lyric_extraction_interface,
            lyric_modification_interface,
            audio_merging_interface,
            karaoke_creation_interface,
        ],
        tab_names=[
            "Extract Lyrics Metadata",
            "Modify Lyrics Metadata",
            "Merge Audio Files",
            "Create Karaoke Video",
        ],
    )
    return karaoke_subtabs

# ════════════════════════════════════════════════════════════
# Main Interface Setup
# ════════════════════════════════════════════════════════════
audio_separation_interface = create_audio_separation_interface()
audio_to_midi_interface = create_audio_to_midi_interface()
modify_midi_interface = create_modify_midi_interface()
lyrics_interface = create_lyrics_interface()
external_website_interface = create_external_website_interface()
karaoke_subtabs = create_karaoke_subtabs()

tabbed_interface = gr.TabbedInterface(
    [
        audio_separation_interface,
        audio_to_midi_interface,
        modify_midi_interface,
        lyrics_interface,
        external_website_interface,
        karaoke_subtabs,
    ],
    tab_names=[
        "Audio Separation",
        "Audio to MIDI",
        "Modify MIDI",
        "Lyrics Extraction",
        "SpessaSynth Website",
        "Karaoke Tools",
    ],
    theme="shivi/calm_seafoam",
)

tabbed_interface.launch()