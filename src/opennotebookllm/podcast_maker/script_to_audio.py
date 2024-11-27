from pathlib import Path

import numpy as np

from src.opennotebookllm.inference.text_to_speech import text_to_speech
from scipy.io.wavfile import write

from src.opennotebookllm.podcast_maker.config import (
    PodcastConfig,
    SpeakerConfig,
    speaker_1_description,
    speaker_2_description,
)


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
    waveform: np.ndarray, sampling_rate: int, filename: Path
) -> None:
    write(filename, rate=sampling_rate, data=waveform)


if __name__ == "__main__":
    filename = Path("test_podcast.wav")
    podcast_script = (
        "Speaker 1: Welcome to our podcast. Speaker 2: It's great to be here!"
    )
    speaker_1 = SpeakerConfig(
        model_id="parler-tts/parler-tts-mini-v1",
        speaker_id="1",
        speaker_description=speaker_1_description,
    )
    speaker_2 = SpeakerConfig(
        model_id="parler-tts/parler-tts-mini-v1",
        speaker_id="2",
        speaker_description=speaker_2_description,
    )
    test_podcast_config = PodcastConfig(
        speakers={s.speaker_id: s for s in [speaker_1, speaker_2]}
    )
    podcast_waveform = parse_script_to_waveform(podcast_script, test_podcast_config)

    save_waveform_as_file(
        podcast_waveform,
        sampling_rate=test_podcast_config.sampling_rate,
        filename=filename,
    )
