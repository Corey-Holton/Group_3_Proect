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

# Guitar Chord Recognition with Audio Feature Extraction and CNN

## 📚 **Project Overview**
This project focuses on recognizing guitar chords using deep learning and audio signal processing techniques. By leveraging **Librosa** for feature extraction and a **Convolutional Neural Network (CNN)** for classification, the system identifies guitar chords from audio recordings.

---

## 🚀 **Key Features**
- **Audio Feature Extraction:** MFCC, Mel Spectrogram, Chroma, and Spectral Contrast.
- **Data Augmentation:** Techniques such as white noise addition, time stretching, time shifting, and pitch shifting.
- **Machine Learning Model:** CNN implemented using TensorFlow/Keras.
- **Dataset Processing:** Handles large datasets of `.wav` files with preprocessing and normalization.
- **Evaluation Metrics:** Accuracy, Confusion Matrix, and Loss Curves.

---

## ⚙️ **Technologies Used**
- **Python Libraries:**
  - Librosa
  - TensorFlow/Keras
  - Scikit-learn
  - Pandas
  - NumPy
  - Matplotlib
  - Seaborn
- **Machine Learning Techniques:**
  - CNN (Convolutional Neural Network)
  - Data Augmentation
  - Feature Normalization
- **Audio Processing Libraries:**
  - Music21
  - Pydub

---

## 📊 **Audio Features Explained**
- **MFCC (Mel-Frequency Cepstral Coefficients):** Captures the spectral envelope of an audio signal.
- **Mel Spectrogram:** Converts frequencies into the Mel scale for better frequency resolution.
- **Chroma Features:** Represents the energy content in each pitch class.
- **Spectral Contrast:** Highlights differences in peaks and valleys of frequency spectra.

---

## 🛠️ **Setup Instructions**
1. **Clone the Repository:**
   ```bash
   git clone <repo_url>
   cd <repo_directory>
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Script:**
   ```bash
   python main.py
   ```
4. **Model Training and Evaluation:**
   - Follow instructions in the notebook or script.

---

## 🧪 **How it Works**
1. **Audio Preprocessing:** Load `.wav` files and apply noise reduction, normalization, and augmentation.
2. **Feature Extraction:** Extract MFCCs, Mel Spectrogram, Chroma, and Spectral Contrast features.
3. **Data Splitting:** Train, validation, and test datasets.
4. **CNN Training:** Train a CNN model to classify audio features.
5. **Model Evaluation:** Evaluate accuracy and generate confusion matrices.
6. **Save Model:** Export trained model and preprocessors (`encoder.pkl`, `scaler.pkl`).

---

## 📈 **Results and Evaluation**
- **Validation Accuracy:** Displayed via confusion matrix.
- **Model Loss Curve:** Graph showing training and validation loss over epochs.

---

## 📦 **Outputs**
- `guitar_chord_recognition_model.keras`: Trained model file.
- `encoder.pkl`: Label encoder.
- `scaler.pkl`: Feature scaler.
- ** guitar_chord_recognition_model.keras is 1.5 gigs and too large to be added to the git repository so it is added to the gitignore file. This will have to be created to use the chord prediciton model.

---

## 🤝 **Contributing**
Contributions are welcome! Please submit a pull request or open an issue for feedback.

---

## 📝 **License**
This project is licensed under the **MIT License**.



# Guitar Chord Recognition and Audio Processing

## Overview

This project focuses on analyzing and predicting guitar chords from audio files using advanced signal processing and machine learning techniques. The workflow integrates audio feature extraction, model-based chord prediction, and MIDI/music sheet generation.

## Features

Audio Processing: Extracts meaningful audio features using FFT (Fast Fourier Transform) and CQT (Constant-Q Transform).

Chord Prediction: Uses a pre-trained Keras deep learning model for chord recognition.

Pitch Estimation: Identifies fundamental frequencies and generates MIDI notes.

Music Visualization: Generates music21 streams and MIDI files for playback and analysis.

Interactive UI for Fine-Tuning: Sliders to adjust CQT parameters.

Music Sheet Generation: Creates sheet music with predicted chords and notes.

## Dependencies

Ensure the following libraries are installed:

numpy

matplotlib

seaborn

joblib

keras

librosa

midiutil

music21

IPython

ipywidgets

Install via pip:

pip install numpy matplotlib seaborn joblib keras librosa midiutil music21 ipywidgets

## Configuration

- Audio Path: path = './audio/music/'

- Sampling Frequency: fs = 44100

- FFT Parameters: nfft = 2048, overlap = 0.5

- CQT Parameters: n_bins = 72, mag_exp = 4, cqt_threshold = -61

## Workflow

1. Model and Audio Loading

- Load a pre-trained Keras model (guitar_chord_recognition_model.keras).

- Load encoder and scaler (encoder.pkl, scaler.pkl).

- Load and preprocess the audio file using Librosa.

2. Signal Processing

- Apply FFT and CQT for frequency analysis.

- Segment audio into smaller chunks for chord prediction.

3. Chord Prediction

- Predict chords using the trained model.

- Decode predicted outputs into chord names.

4. Music Sheet and MIDI Generation

- Estimate pitch and generate sine waves.

- Create MIDI notes and music21 streams.

- Generate and save MIDI files.

## Outputs

- Audio Playback: Listen to processed audio.

- Visual Plots: FFT and CQT spectrograms.

- Music21 Stream: Play and display sheet music.

- MIDI File: Saved as sweet_child_music21_with_chords.mid

## Running the Code

1. Place audio files in the specified path.

2. Run the script in a Jupyter Notebook environment.

3. Use the UI to fine-tune parameters.

## Troubleshooting

- Verify all dependencies are installed.

- Ensure valid audio file paths.

- Check model and encoder files are available.

## Future Improvements

- Expand model to recognize additional instruments.

- Real-time chord prediction.

## Authors

- Group 3 Project Team (Corey Holton, Christian Palacios, Edwin Lovera, Montre Davis)
License

This project is licensed under the MIT License.

