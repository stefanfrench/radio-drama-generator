import numpy as np

from src.opennotebookllm.inference.text_to_speech import text_to_speech
from scipy.io.wavfile import write

from src.opennotebookllm.podcast_maker.config import PodcastConfig


def parse_script_to_waveform(script: str, podcast_config: PodcastConfig):
    """
    Given a script with speaker identifiers (such as "Speaker 1") parse it so that each speaker has its own unique
    voice and concatenate all the voices in a sequence to form the complete podcast.
    Args:
        script:
        podcast_config:

    Returns: A 2D numpy array containing the whole podcast in waveform format.

    """
    parts = script.split("Speaker ")
    podcast_waveform = []
    for part in parts:
        if ":" in part:
            speaker_id, speaker_text = part.split(":")
            speaker_waveform = text_to_speech(
                speaker_text, podcast_config.speakers[speaker_id]
            )
            podcast_waveform.append(speaker_waveform)

    return np.concatenate(podcast_waveform)


def save_waveform_as_file(
    waveform: np.ndarray, sampling_rate: int, filename: str = "podcast.wav"
) -> None:
    write(filename, rate=sampling_rate, data=waveform)
