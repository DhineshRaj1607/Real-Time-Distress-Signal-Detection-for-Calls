# SpeakSafe

**Real-Time Distress Signal Detection for Calls**

SpeakSafe is a local speech-to-text prototype that checks recorded or uploaded audio for user-configured distress phrases. When it finds a possible match, it shows the recognized phrase and its timestamp. It is designed as an educational ASR project and a demonstration of phrase-based alerting.

> **Important:** SpeakSafe does not connect to or monitor phone calls. It analyzes audio that a user explicitly records or uploads. It is not an emergency service and cannot guarantee that distress will be detected.

## Features

- Record a voice sample in the browser or upload an audio file.
- Transcribe locally with the Faster-Whisper speech recognition model.
- Configure phrases to look for, such as “help me” or “call the police.”
- Show possible matches with the transcript segment and timestamp.
- Download the transcript as a text file.
- Run phrase-matching tests without downloading an ASR model.

## Tools and technologies

- **Python 3.10+** — application logic.
- **Streamlit** — web interface, audio upload, and browser recording.
- **faster-whisper** — local automatic speech recognition using CTranslate2.
- **unittest** — tests for phrase parsing, normalization, and detection.

## Requirements

- Python 3.10 or newer.
- Internet connection for installing packages and downloading the selected Whisper model the first time. After the model is cached, transcription runs locally.
- A modern browser and microphone for recording; audio upload can be used instead.

The first model download can be large. The default **tiny** model is selected to make the first run lighter and faster. You can choose **base** or **small** in the sidebar for potentially better recognition at the cost of speed and memory.

## Run locally

1. Clone the repository and enter the project folder:

   ```bash
   git clone <repository-url>
   cd speaksafe
   ```

2. Create and activate a virtual environment.

   **macOS/Linux**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   **Windows PowerShell**

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

4. Start SpeakSafe:

   ```bash
   streamlit run app.py
   ```

5. Open the local URL printed in the terminal. Upload a recording or use the **Record a voice sample** tab. Choose phrases in the sidebar, then select **Transcribe and check for phrases**.

## Deploy to Streamlit Community Cloud

SpeakSafe is configured for Streamlit Community Cloud. Deployment requires a GitHub repository and a Streamlit Community Cloud account linked to GitHub.

1. Push this project to a GitHub repository.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub and connect the account.
3. Choose **Create app**, select the repository and branch, and set `app.py` as the app file.
4. In advanced settings, select Python 3.10 or newer, then deploy.

The app's upload limit is set to 50 MB. Community Cloud has limited CPU and memory, so the **tiny** model is the recommended setting; larger models may be slow or exceed the host's resources. The model downloads on first use and stays cached on that server while the app environment remains available.

When hosted, audio selected or recorded in the page is sent to the Streamlit server for transcription. Choose a hosting account and sharing setting appropriate for the audio that users may provide. Community Cloud's public/private access follows the app and repository settings.

## Run tests

The detector tests use only the Python standard library and do not download a speech model:

```bash
python -m unittest discover -s tests -v
```

## Project structure

```text
app.py                  Streamlit user interface
speaksafe/detector.py   Phrase parsing and alert matching
speaksafe/transcriber.py Local Faster-Whisper wrapper
tests/                  Unit tests for the detector
requirements.txt        Python dependencies
```

## Privacy and limitations

- The ASR model runs on the same machine as the app after its initial download. The app does not call a hosted transcription API. In a cloud deployment, that machine is the hosting provider's server, and submitted audio is sent there for processing.
- SpeakSafe does not save recordings or transcripts to project files. Results live in the current Streamlit session; deployments may have their own infrastructure-level logging or retention, so review hosting settings before using sensitive audio.
- Speech recognition can miss or mishear words due to noise, language, accents, overlapping speakers, or recording quality. Phrase matching can also produce alerts in harmless contexts.
- Use microphone recording only with appropriate consent. Make recording status clear to anyone whose speech may be captured.
- Treat alerts as a prompt for human review, not as proof of danger. Do not rely on SpeakSafe to contact emergency services or as a replacement for them.

## License

No license has been selected yet. Add a `LICENSE` file before redistributing or reusing this project.
