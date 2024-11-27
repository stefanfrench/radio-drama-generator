from pathlib import Path

import numpy as np

from opennotebookllm.inference.model_loaders import load_parler_tts_model_and_tokenizer
from opennotebookllm.inference.text_to_speech import text_to_speech
from scipy.io.wavfile import write

from opennotebookllm.podcast_maker.config import (
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
            speaker_model = podcast_config.speakers[speaker_id].model
            speaker_tokenizer = podcast_config.speakers[speaker_id].tokenizer
            speaker_description = podcast_config.speakers[
                speaker_id
            ].speaker_description

            speaker_waveform = text_to_speech(
                speaker_text, speaker_model, speaker_tokenizer, speaker_description
            )
            podcast_waveform.append(speaker_waveform)

    return np.concatenate(podcast_waveform)


def save_waveform_as_file(
    waveform: np.ndarray, sampling_rate: int, filename: Path
) -> None:
    write(filename, rate=sampling_rate, data=waveform)


if __name__ == "__main__":
    test_filename = Path("test_podcast.wav")

    model, tokenizer = load_parler_tts_model_and_tokenizer(
        "parler-tts/parler-tts-mini-v1", "cpu"
    )

    podcast_script = (
        "Speaker 1: Welcome to our podcast. Speaker 2: It's great to be here!"
    )
    speaker_1 = SpeakerConfig(
        model=model,
        speaker_id="1",
        tokenizer=tokenizer,
        speaker_description=speaker_1_description,
    )
    speaker_2 = SpeakerConfig(
        model=model,
        speaker_id="2",
        tokenizer=tokenizer,
        speaker_description=speaker_2_description,
    )
    test_podcast_config = PodcastConfig(
        speakers={s.speaker_id: s for s in [speaker_1, speaker_2]}
    )

    test_podcast_waveform = parse_script_to_waveform(
        podcast_script, test_podcast_config
    )

    save_waveform_as_file(
        test_podcast_waveform,
        sampling_rate=test_podcast_config.sampling_rate,
        filename=test_filename,
    )
