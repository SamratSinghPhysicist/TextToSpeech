import gradio as gr
from TTS.api import TTS
import tempfile
import os

# Load the TTS model when the app starts.
# Using the multilingual YourTTS model that supports voice cloning.
MODEL_NAME = "tts_models/multilingual/multi-dataset/your_tts"
tts = TTS(model_name=MODEL_NAME, progress_bar=False, gpu=False)  # Set gpu=True if available

def synthesize_speech(text: str, language: str, speaker_file):
    """
    Synthesizes speech from the provided text.
    Uses your recorded voice (my_voice.wav) as the default speaker reference if none is uploaded.

    Args:
        text (str): The input text to synthesize.
        language (str): The language code (e.g., "hi" for Hindi, "en" for English).
        speaker_file (str): File path to the uploaded speaker reference WAV file (optional).

    Returns:
        str: Path to the generated audio file (WAV format).
    """
    # If the user did not upload a speaker file, use the default recorded voice.
    if speaker_file is None:
        default_speaker = "my_voice.wav"
        if os.path.exists(default_speaker):
            speaker_path = default_speaker
        else:
            speaker_path = None
    else:
        speaker_path = speaker_file

    # Create a temporary file for the output audio.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        output_path = tmp_file.name

    try:
        # Pass the language parameter to the TTS synthesis call.
        tts.tts_to_file(
            text=text,
            language=language,
            speaker_wav=speaker_path,
            file_path=output_path
        )
    except Exception as e:
        # Raise a Gradio error so that the error is displayed properly.
        raise gr.Error(f"Error during synthesis: {str(e)}")
    
    return output_path

# Define the Gradio interface with three inputs:
# 1. A textbox for the text.
# 2. A dropdown for selecting the language.
# 3. An optional audio upload for a speaker reference.
iface = gr.Interface(
    fn=synthesize_speech,
    inputs=[
        gr.Textbox(
            lines=5,
            placeholder="Enter your text (Hinglish: Hindi + English)...",
            label="Input Text"
        ),
        gr.Dropdown(
            choices=["hi", "en"],
            value="hi",
            label="Language (e.g., hi for Hindi, en for English)"
        ),
        gr.Audio(
            type="filepath",
            label="Upload Speaker Reference (Optional)\n(Leave empty to use your recorded voice)"
        )
    ],
    outputs=gr.Audio(
        type="filepath",
        label="Generated Speech"
    ),
    title="YourTTS Voice Cloning TTS",
    description=(
        "Enter the text you want to synthesize and select the language. "
        "If you don't upload a speaker reference, the app will use your recorded voice "
        "(my_voice.wav) for voice cloning. The app uses Coqui TTS's multilingual YourTTS model."
    )
)

if __name__ == "__main__":
    iface.launch()
