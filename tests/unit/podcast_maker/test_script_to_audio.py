import os
from src.opennotebookllm.podcast_maker.script_to_audio import script_to_audio


def test_parse_script(podcast_script: str):
    filename = "test_podcast.wav"
    script_to_audio(podcast_script, filename=filename)

    assert os.path.isfile(filename)
