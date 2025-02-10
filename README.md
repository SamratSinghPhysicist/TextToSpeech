---
title: TextToSpeechYourTTS
emoji: 🏆
colorFrom: green
colorTo: gray
sdk: gradio
sdk_version: 5.15.0
app_file: app.py
pinned: false
short_description: Have my own clone voice in it
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference



# TTS with Voice Cloning – UI & API

This repository provides a text-to-speech (TTS) application built with Coqui TTS’s voice cloning model. It offers both:

- **A Web UI:** Built with [Gradio](https://gradio.app/) for interactive synthesis.
- **An API:** Built with [FastAPI](https://fastapi.tiangolo.com/) for programmatic access.

If no speaker reference file is provided, the application will use your default recorded voice (`my_voice.wav`) for voice cloning.

---

## Features

- **Voice Cloning TTS:** Synthesize speech using Coqui TTS’s multilingual voice cloning model.
- **Multiple Language Support:** (Supported languages: `en`, `fr-fr`, `pt-br`)
- **Web UI:** Interactively enter text, choose language, and optionally upload a speaker reference.
- **API Endpoint:** POST requests to synthesize speech from your applications.
- **Deployment Ready:** Easily deployable to Hugging Face Spaces via your GitHub repository.

---

## Files in This Repository

- **app.py**  
  Contains the FastAPI application with:
  - An API endpoint at `/api/synthesize/`
  - A mounted Gradio UI at `/ui`
- **requirements.txt**  
  Lists the required Python packages.
- **my_voice.wav**  
  Your recorded voice file (used as the default speaker reference if no file is uploaded).

---

## How It Works

### API Endpoint

- **URL:** `/api/synthesize/`  
- **Method:** `POST`  
- **Form Data Parameters:**
  - `text` (string, required): The text to synthesize.
  - `language` (string, required): The language code (e.g., `en`, `fr-fr`, or `pt-br`).
  - `speaker_file` (file, optional): A WAV file of a speaker reference. If not provided, the default `my_voice.wav` will be used if available.

- **Response:**  
  Returns the synthesized speech as a WAV file.

### Web UI

- **URL:** `/ui`  
- Use the interactive Gradio interface to enter text, select language, and (optionally) upload a speaker file. Click the button to synthesize and play back the audio.

---

## Running Locally

1. **Clone the repository:**

   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt

3. **Run the application**

   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000


4. **Access the UI and API**

   ```bash
    UI: Open your browser and navigate to http://localhost:8000/ui
    API: The API endpoint is available at http://localhost:8000/api/synthesize/

5. **Sample Python Client for the API**
    Below is a sample Python script that demonstrates how to call the TTS API endpoint using the "requests" library:

    ```python
    import requests
    # Replace with your deployed Hugging Face Spaces URL (or localhost for testing)
    API_URL = "http://localhost:8000/api/synthesize/"

    # Prepare the form data
    data = {
        "text": "Hello, this is a test of the TTS API.",
        "language": "en"
    }

    # (Optional) Include a speaker reference file if you want:
    # files = {"speaker_file": open("path/to/your/speaker.wav", "rb")}
    files = {}  # No file provided; the default my_voice.wav will be used

    response = requests.post(API_URL, data=data, files=files)

    if response.status_code == 200:
        # Save the returned WAV file
        with open("output.wav", "wb") as f:
            f.write(response.content)
        print("Synthesized audio saved as output.wav")
    else:
        print("Error:", response.json())