import os
import tempfile
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from TTS.api import TTS
import uvicorn

# Initialize FastAPI
app = FastAPI(
    title="TTS Voice Cloning API",
    description="API endpoint for synthesizing speech using Coqui TTS's voice cloning model.",
    version="1.0"
)

# Load the voice cloning model (YourTTS) for supported languages.
# Supported languages: "en", "fr-fr", "pt-br"
model_your_tts = TTS(
    model_name="tts_models/multilingual/multi-dataset/your_tts",
    progress_bar=False,
    gpu=False  # Change to True if your deployment environment has a GPU
)

@app.post("/synthesize/", summary="Synthesize speech from text")
async def synthesize_speech(
    text: str = Form(..., description="The text to synthesize."),
    language: str = Form(..., description="Language code (e.g., en, fr-fr, pt-br)."),
    speaker_file: UploadFile = File(None, description="Optional speaker reference WAV file")
):
    """
    Synthesize speech from text using the TTS model.  
    If no speaker file is uploaded, the default speaker (`my_voice.wav`) will be used if available.
    """
    # Create a temporary file to store the generated audio.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        output_path = tmp_file.name

    # Process the uploaded speaker file if provided.
    if speaker_file:
        try:
            # Save the uploaded file to a temporary location.
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as spk_file:
                content = await speaker_file.read()
                spk_file.write(content)
                speaker_path = spk_file.name
        except Exception as e:
            return JSONResponse(status_code=400, content={"error": f"Error processing speaker file: {str(e)}"})
    else:
        # Use the default recorded voice if available.
        default_speaker = "my_voice.wav"
        speaker_path = default_speaker if os.path.exists(default_speaker) else None

    # Attempt to synthesize speech.
    try:
        model_your_tts.tts_to_file(
            text=text,
            language=language,
            speaker_wav=speaker_path,
            file_path=output_path
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Error during synthesis: {str(e)}"})

    # Return the synthesized audio as a WAV file.
    return FileResponse(
        output_path,
        media_type="audio/wav",
        filename="output.wav"
    )

# Optional: Run the server locally (useful for testing)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
