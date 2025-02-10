import gradio as gr
from TTS.api import TTS
import tempfile

# Load the TTS model once when the app starts.
# Using the YourTTS multilingual model which supports voice cloning.
MODEL_NAME = "tts_models/multilingual/multi-dataset/your_tts"
tts = TTS(model_name=MODEL_NAME, progress_bar=False, gpu=False)  # Set gpu=True if GPU is available

def synthesize_speech(text: str, speaker_file):
    """
    Synthesizes speech from the provided text.
    If a speaker reference file is provided, it uses that for voice cloning.
    
    Args:
        text (str): The input text to synthesize.
        speaker_file (file-like): Optional WAV file for the reference speaker.
    
    Returns:
        str: Path to the generated audio file (WAV format).
    """
    # Determine if a speaker reference was provided.
    speaker_path = speaker_file.name if speaker_file is not None else None

    # Create a temporary file to store the output audio.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        output_path = tmp_file.name

    # Generate the speech and save to the temporary file.
    try:
        tts.tts_to_file(text=text, speaker_wav=speaker_path, file_path=output_path)
    except Exception as e:
        return f"Error during synthesis: {str(e)}"
    
    return output_path

# Define the Gradio interface.
# Two inputs: a textbox for text and an optional audio upload for the speaker reference.
# One output: an audio player that plays the generated speech.
iface = gr.Interface(
    fn=synthesize_speech,
    inputs=[
        gr.components.Textbox(
            lines=5,
            placeholder="Enter your text (Hinglish: Hindi + English)...",
            label="Input Text"
        ),
        gr.components.Audio(
            source="upload",
            type="file",
            label="Speaker Reference (Optional)"
        )
    ],
    outputs=gr.components.Audio(
        type="file",
        label="Generated Speech"
    ),
    title="YourTTS Voice Cloning TTS",
    description=(
        "Enter the text you want to synthesize. Optionally, upload a short WAV file of a reference "
        "speaker to clone their voice. The app uses Coqui TTS's multilingual YourTTS model."
    )
)

# Launch the Gradio interface.
if __name__ == "__main__":
    iface.launch()
