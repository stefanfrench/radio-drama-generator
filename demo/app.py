import re
from pathlib import Path

import numpy as np
import soundfile as sf
import streamlit as st

from document_to_podcast.preprocessing import DATA_LOADERS, DATA_CLEANERS
from document_to_podcast.inference.model_loaders import (
    load_llama_cpp_model,
    load_outetts_model,
)
from document_to_podcast.config import DEFAULT_PROMPT, DEFAULT_SPEAKERS, Speaker
from document_to_podcast.inference.text_to_speech import text_to_speech
from document_to_podcast.inference.text_to_text import text_to_text_stream




@st.cache_resource
def load_text_to_text_model():
    return load_llama_cpp_model(
        model_id="allenai/OLMoE-1B-7B-0924-Instruct-GGUF/olmoe-1b-7b-0924-instruct-q8_0.gguf"
    )


@st.cache_resource
def load_text_to_speech_model():
    return load_outetts_model("OuteAI/OuteTTS-0.2-500M-GGUF/OuteTTS-0.2-500M-FP16.gguf")


script = "script"
audio = "audio"
gen_button = "generate_radio_drama_button"
if script not in st.session_state:
    st.session_state[script] = ""
if audio not in st.session_state:
    st.session_state.audio = []
if gen_button not in st.session_state:
    st.session_state[gen_button] = False


def gen_button_clicked():
    st.session_state[gen_button] = True


st.title("📖 Radio Drama Generator")

st.header("🎭 Upload intro context for your Story")

uploaded_file = st.file_uploader(
    "Choose a file to transform into a radio drama (e.g., `.pdf`, `.html`, `.txt`, `.docx`, `.md`):",
    type=["pdf", "html", "txt", "docx", "md"],
)

if uploaded_file is not None:
    st.divider()

    extension = Path(uploaded_file.name).suffix


    raw_text = DATA_LOADERS[extension](uploaded_file)

    clean_text = DATA_CLEANERS[extension](raw_text)

    st.header("🤖 Loading AI Models")


    text_model = load_text_to_text_model()
    speech_model = load_text_to_speech_model()

    # ~4 characters per token is considered a reasonable default.
    max_characters = text_model.n_ctx() * 4
    if len(clean_text) > max_characters:
        st.warning(
            f"Input text is too large ({len(clean_text)})."
            f" Using only a subset ({max_characters} characters)."
        )
        clean_text = clean_text[:max_characters]

    st.divider()
    st.header("🎙️ Generate Your Radio Drama")
    st.divider()

    st.subheader("🎭 Configure Your Characters")
    for s in DEFAULT_SPEAKERS:
        s.pop("id", None)
    speakers = st.data_editor(DEFAULT_SPEAKERS, num_rows="dynamic")

    if st.button("Generate Radio Drama", on_click=gen_button_clicked):
        for n, speaker in enumerate(speakers):
            speaker["id"] = n + 1
        system_prompt = DEFAULT_PROMPT.replace(
            "{SPEAKERS}",
            "\n".join(str(Speaker.model_validate(speaker)) for speaker in speakers),
        )
        with st.spinner("Generating Dialogue..."):
            text = ""
            for chunk in text_to_text_stream(
                clean_text, text_model, system_prompt=system_prompt.strip()
            ):
                text += chunk
                if text.endswith("\n") and "Speaker" in text:
                    st.session_state.script += text
                    st.write(text)

                    speaker_id = re.search(r"Speaker (\d+)", text).group(1)
                    voice_profile = next(
                        speaker["voice_profile"]
                        for speaker in speakers
                        if speaker["id"] == int(speaker_id)
                    )
                    with st.spinner("Generating Audio..."):
                        speech = text_to_speech(
                            text.split(f'"Speaker {speaker_id}":')[-1],
                            speech_model,
                            voice_profile,
                        )
                    st.audio(speech, sample_rate=speech_model.audio_codec.sr)

                    st.session_state.audio.append(speech)
                    text = ""

    if st.session_state[gen_button]:
        if st.button("🎧 Save Radio Drama as Audio"):
            st.session_state.audio = np.concatenate(st.session_state.audio)
            sf.write(
                "radio_drama.wav",
                st.session_state.audio,
                samplerate=speech_model.audio_codec.sr,
            )
            st.markdown("Radio drama saved as an audio file!")

        if st.button("📜 Save Script as Text File"):
            with open("script.txt", "w") as f:
                st.session_state.script += "}"
                f.write(st.session_state.script)

            st.markdown("Script saved to disk!")