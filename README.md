# Gradio Audio Processing App

This application provides an intuitive interface built with Gradio for processing audio files. It includes functionalities like audio separation, MIDI conversion, MIDI modification, and lyrics extraction and translation.

---

## Features

1. **Audio Separation**  
   - Separate an audio file into its components (vocals, bass, drums, etc.) using the Demucs model.

2. **Audio to MIDI Conversion**  
   - Convert audio files into MIDI format using the Basic Pitch model with customizable parameters.

3. **Modify MIDI Files**  
   - Upload a MIDI file and apply transformations based on user-defined prompts.

4. **Lyrics Extraction and Translation**  
   - Extract lyrics from an audio file and translate them into different languages.

---

## Requirements

### Software
- Python 3.9 or above  
- Conda for environment management

### Python Libraries
The app utilizes various Python libraries such as:
- Gradio  
- TensorFlow  
- Coremltools (optional)  
- Additional dependencies mentioned in `requirements.txt` (not provided here but recommended to generate)

### Models
- **Demucs**: For audio separation  
- **Basic Pitch**: For MIDI generation  
- **Custom Lyrics Extraction and Translation Models**

---

## Installation Guide

1. **Clone the Repository**
    ```bash
    git clone https://github.com/Corey-Holton/Group_3_Project.git
    cd https://github.com/Corey-Holton/Group_3_Project.git
    ```

2. **Set Up Conda Environment**  
   Create and activate a Conda environment for the project:
    ```bash
    conda create -n audio_processing python=3.10 -y
    conda activate audio_processing
    ```

3. **Install Dependencies**  
   Install all required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application**  
   Launch the Gradio interface:
    ```bash
    python app.py
    ```

---

## How to Use

### Audio Separation
1. Navigate to the “Audio Separation” tab.  
2. Upload an audio file and customize the parameters (e.g., model, output format, bitrate).  
3. Click **Separate Audio** to process the file and download the separated stems.

### Audio to MIDI
1. Switch to the “Audio to MIDI” tab.  
2. Upload an audio file and configure the MIDI generation settings.  
3. Click **Convert to MIDI** to generate the MIDI file.

### Modify MIDI
1. Select the “Modify MIDI” tab.  
2. Upload a MIDI file and provide a prompt for modifications.  
3. Click **Modify MIDI** to generate a new MIDI file.

### Lyrics Extraction
1. Go to the “Lyrics Extraction” tab.  
2. Upload an audio file and click **Extract Lyrics** to display the lyrics.  
3. Optionally, input a language code (e.g., en, es, fr) and click **Translate** to translate the lyrics.

---

## File Structure Overview

```plaintext
audio_processing/
├── output_stems/            # Directory for storing separated audio stems
├── notebooks/               # Jupyter notebooks for development and testing
├── utilities/               # Utility scripts for audio processing and MIDI generation
│   ├── separate_audio.py    # Audio separation logic
│   ├── audio_to_midi.py     # MIDI conversion functionality
│   ├── extract_lyrics.py    # Lyrics extraction and translation functions
├── app.py                   # Main script for the Gradio app
├── requirements.txt         # Python dependencies
```


### Customization Options
-  Audio Separation: Change the model name (default is htdemucs_ft) in the interface.
-  MIDI Conversion: Adjust thresholds, frequency ranges, and samplerate for optimal results.
-  Lyrics Translation: Update translation API or dictionaries as needed.

### Troubleshooting
- Coremltools Warning: If not required, the app will work fine without it.
- TensorFlow Warning: Ensure TensorFlow is installed and compatible with your Python version.
- Missing Outputs: Verify the output_stems/ and output_midi/ directories are writable.

### Future Enhancements
- Integration with cloud storage for saving outputs.
- Support for more languages in lyrics translation.
- Improved MIDI modification capabilities.