import wave

import numpy as np

from demo.app import sample_pod_config
from opennotebookllm.inference.text_to_speech import text_to_speech

from opennotebookllm.podcast_maker.config import PodcastConfig


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
    waveform: np.ndarray, sampling_rate: int, filename: str
) -> None:
    with wave.open(filename, "w") as f:
        f.setnchannels(2)  # 2 for Stereo, 1 for Mono
        f.setsampwidth(1)  # bytes per sample
        f.setframerate(sampling_rate)
        f.writeframes(waveform.tobytes())


if __name__ == "__main__":
    test_filename = "test_podcast.wav"
    test_podcast_script = (
        "Speaker 1: Welcome to our podcast. Speaker 2: It's great to be here!"
    )

    test_podcast_waveform = parse_script_to_waveform(
        test_podcast_script, sample_pod_config
    )

    save_waveform_as_file(
        test_podcast_waveform,
        sampling_rate=sample_pod_config.sampling_rate,
        filename=test_filename,
    )
