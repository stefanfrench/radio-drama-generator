from src.opennotebookllm.inference.text_to_speech import text_to_speech
from scipy.io.wavfile import write

from src.opennotebookllm.podcast_maker.config import PodcastConfig


def test_text_to_speech_parler(tts_prompt: str, podcast_config: PodcastConfig):
    waveform = text_to_speech(
        input_text=tts_prompt, tts_config=list(podcast_config.speakers.values())[0]
    )

    write("test_parler_tts.wav", rate=podcast_config.sampling_rate, data=waveform)
