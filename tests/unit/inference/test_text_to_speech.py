from src.opennotebookllm.inference.text_to_speech import text_to_speech

from src.opennotebookllm.podcast_maker.config import PodcastConfig
from src.opennotebookllm.podcast_maker.script_to_audio import save_waveform_as_file


def test_text_to_speech_parler(tts_prompt: str, podcast_config: PodcastConfig):
    waveform = text_to_speech(
        input_text=tts_prompt, tts_config=list(podcast_config.speakers.values())[0]
    )

    save_waveform_as_file(
        waveform=waveform,
        sampling_rate=podcast_config.sampling_rate,
        filename="test_parler_tts.wav",
    )
