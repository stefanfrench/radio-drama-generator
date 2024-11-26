from src.opennotebookllm.inference.text_to_speech import text_to_speech
from scipy.io.wavfile import write


def test_text_to_speech_parler(tts_prompt, tts_speaker_description):
    waveform = text_to_speech(
        input_text=tts_prompt,
        speaker_description=tts_speaker_description,
        model_id="parler-tts/parler-tts-mini-v1",
    )

    write("test_parler_tts.wav", rate=24_000, data=waveform)
