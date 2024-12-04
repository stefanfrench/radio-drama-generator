import os
from pathlib import Path

import numpy as np

from document_to_podcast.podcast_maker.config import PodcastConfig
from document_to_podcast.podcast_maker.script_to_audio import (
    parse_script_to_waveform,
    save_waveform_as_file,
)


def test_parse_script_waveform(podcast_script: str, podcast_config: PodcastConfig):
    podcast_waveform = parse_script_to_waveform(podcast_script, podcast_config)

    assert isinstance(podcast_waveform, np.ndarray)
    assert podcast_waveform.size > 1


def test_script_to_podcast(
    tmp_path: Path, podcast_script: str, podcast_config: PodcastConfig
):
    filename = str(tmp_path / "test_podcast.wav")
    podcast_waveform = parse_script_to_waveform(podcast_script, podcast_config)

    save_waveform_as_file(
        podcast_waveform, sampling_rate=podcast_config.sampling_rate, filename=filename
    )
    assert os.path.isfile(filename)
