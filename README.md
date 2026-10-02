# SpeakSafe

**Real-Time Distress Signal Detection for Calls**

SpeakSafe is a prototype concept for an ASR-powered tool that listens to audio, converts speech to text, and raises a visible alert when configured distress phrases are detected. Examples might include “help me,” “I’m in danger,” or “call the police.”

> **Project status:** README and project plan. The application source code and tests have not been implemented yet.

## Planned features

- Transcribe microphone or sample audio.
- Match recognized speech against a configurable list of distress phrases.
- Display an alert with the matched phrase and timestamp.
- Adjust phrase matching to catch simple variations while limiting false alarms.
- Include a demo mode so detection can be tried with sample audio.

## Tools and technologies

The proposed stack for the first version is:

- **Python** for application logic.
- **Streamlit** for a simple web interface.
- **faster-whisper** for speech recognition (ASR).
- **sounddevice** for microphone input, if supported by the operating system.
- **pytest** for automated tests of phrase matching and related logic.

These are planned choices; the final stack may change during implementation.

## How it is intended to work

1. The user starts a session and grants microphone access, or selects sample audio.
2. SpeakSafe transcribes the audio.
3. The detector checks the transcript against the configured phrase list.
4. When it finds a match, the interface displays a possible distress alert.

## Planned setup and run instructions

These commands will apply once the application files and `requirements.txt` are added.

1. Install Python 3.10 or newer.
2. Clone the repository and move into its folder:

   ```bash
   git clone <repository-url>
   cd speaksafe
   ```

3. Create and activate a virtual environment:

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

4. Install the project dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Start the app (planned entry point):

   ```bash
   streamlit run app.py
   ```

The exact Python version, install steps, and run command should be updated if the implementation uses a different stack or entry point.

## Testing

Automated tests are planned. Once the test suite is added, run it with:

```bash
python -m pytest
```

Testing should cover phrase matching, variations in capitalization and punctuation, and cases where no alert should be raised.

## Important limitations

SpeakSafe is a prototype and must not be treated as an emergency service, a guarantee of safety, or a replacement for contacting local emergency services. Speech recognition can miss distress phrases or produce false matches because of noise, accents, overlapping speech, language, or poor connectivity. Alerts should be treated as prompts for a person to review, not as proof that someone is in danger.

Use microphone input only with appropriate consent and in accordance with applicable laws and policies. Make recording and listening status clear to users. Avoid storing audio or transcripts unless there is a clear need and users have been informed.

## Contributing

Contributions are welcome. Please describe the change and include tests for detector behavior when submitting a pull request.

## License

No license has been selected yet. Add a `LICENSE` file before redistributing or reusing this project.
