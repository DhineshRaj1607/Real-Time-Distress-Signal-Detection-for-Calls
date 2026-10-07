"""SpeakSafe: an audio-based distress phrase detection prototype."""

from __future__ import annotations

import io
from pathlib import Path

import streamlit as st

from speaksafe.detector import detect_alerts, parse_phrases
from speaksafe.transcriber import TranscriptionError, transcribe_audio


st.set_page_config(
    page_title="SpeakSafe | Distress phrase detection",
    page_icon="🛟",
    layout="centered",
)

st.markdown(
    """
    <style>
    .block-container {max-width: 920px; padding-top: 2.2rem;}
    .hero {padding: 1.6rem 1.8rem; border-radius: 18px;
           background: linear-gradient(120deg,#101e36,#183c54); color: #f4f8ff;
           margin-bottom: 1rem;}
    .hero h1 {margin: 0 0 .35rem 0; font-size: 2.35rem;}
    .hero p {margin: 0; color: #d2e1f2; font-size: 1.06rem;}
    </style>
    <div class="hero">
      <h1>🛟 SpeakSafe</h1>
      <p>Speech-to-text with a visible alert when configured distress phrases are heard.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Detection settings")
    model_size = st.selectbox(
        "Speech model",
        options=("tiny", "base", "small"),
        index=0,
        help="The model downloads the first time you transcribe. Tiny is fastest; larger models may be more accurate but need more time and memory.",
    )
    language = st.text_input(
        "Language code (optional)",
        value="",
        placeholder="e.g. en, hi, es",
        help="Leave blank to let Whisper detect the language.",
    ).strip() or None
    phrase_text = st.text_area(
        "Phrases to watch for (one per line)",
        value="help me\nI need help\nI am in danger\ncall the police\nplease help",
        height=160,
    )
    st.caption("Choose phrases for your use case. This is a configurable demo list, not a complete threat vocabulary.")

phrases = parse_phrases(phrase_text)
st.subheader("Choose audio")
upload_tab, record_tab = st.tabs(("Upload a recording", "Record a voice sample"))
audio_bytes: bytes | None = None
audio_name = "audio"

with upload_tab:
    uploaded = st.file_uploader(
        "Select an audio file",
        type=("wav", "mp3", "m4a", "ogg", "flac", "webm"),
        help="Audio is processed by the local Whisper model after it has been downloaded.",
    )
    if uploaded is not None:
        audio_bytes = uploaded.getvalue()
        audio_name = uploaded.name

with record_tab:
    recording = st.audio_input("Record a short sample")
    if recording is not None:
        audio_bytes = recording.getvalue()
        audio_name = "microphone-recording.wav"

if audio_bytes:
    st.audio(audio_bytes)
else:
    st.info("Upload an audio file or record a voice sample to begin.")

run = st.button("Transcribe and check for phrases", type="primary", use_container_width=True)
if run:
    if not audio_bytes:
        st.error("Choose an audio file or record a sample first.")
    elif not phrases:
        st.error("Add at least one phrase to check before transcribing.")
    else:
        try:
            with st.spinner("Transcribing audio locally… The first run may download the model. Keep this page open."):
                segments = transcribe_audio(
                    io.BytesIO(audio_bytes),
                    model_size=model_size,
                    language=language,
                )
            transcript = " ".join(segment.text.strip() for segment in segments).strip()
            st.session_state["last_transcript"] = transcript
            st.session_state["last_segments"] = [segment.to_dict() for segment in segments]
            st.session_state["last_audio_name"] = Path(audio_name).name
            st.session_state["last_alerts"] = [
                alert.to_dict() for alert in detect_alerts(segments, phrases)
            ]
        except TranscriptionError as exc:
            st.error(str(exc))

if "last_transcript" in st.session_state:
    st.divider()
    st.subheader("Transcription result")
    st.caption(f"Source: {st.session_state.get('last_audio_name', 'audio')}")
    transcript = st.session_state["last_transcript"]
    if transcript:
        st.text_area("Recognized speech", value=transcript, height=160, disabled=True)
        st.download_button(
            "Download transcript",
            data=transcript,
            file_name="speaksafe-transcript.txt",
            mime="text/plain",
        )
    else:
        st.info("No speech was recognized in this audio. Try a clearer or longer recording.")

    alerts = st.session_state.get("last_alerts", [])
    if alerts:
        st.error(f"⚠️ Possible distress phrase detected ({len(alerts)} match{'es' if len(alerts) != 1 else ''})")
        for alert in alerts:
            timestamp = f"{alert['start']:.1f}s" if alert["start"] is not None else "time unavailable"
            st.warning(f"At {timestamp}: **{alert['phrase']}** — “{alert['text']}”")
        st.caption("Review the audio and context. A match is not confirmation that someone is in danger.")
    else:
        st.success("No configured phrases matched the recognized speech.")
