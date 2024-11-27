from pathlib import Path

import pytest

from opennotebookllm.podcast_maker.config import (
    PodcastConfig,
    SpeakerConfig,
    speaker_1_description,
    speaker_2_description,
)


@pytest.fixture(scope="session")
def example_data():
    return Path(__file__).parent.parent / "example_data"


@pytest.fixture()
def tts_prompt():
    return "Wow what a great unit test this is!"


@pytest.fixture()
def podcast_script():
    return "Speaker 1: Welcome to our podcast. Speaker 2: It's great to be here!"


@pytest.fixture()
def podcast_config():
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
    speakers = {s.speaker_id: s for s in [speaker_1, speaker_2]}
    return PodcastConfig(speakers=speakers)
