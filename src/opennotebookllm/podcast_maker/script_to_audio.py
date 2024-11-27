import numpy as np

from src.opennotebookllm.inference.text_to_speech import (
    text_to_speech,
    default_speaker_1_description,
    default_speaker_2_description,
)
from scipy.io.wavfile import write


def script_to_audio(
    script: str,
    model_id: str = "parler-tts/parler-tts-mini-v1",
    filename: str = "podcast.wav",
    sampling_rate: int = 44_100,
):
    parts = script.split("Speaker")
    podcast_waveform = []
    for part in parts:
        if ":" in part:
            speaker_id, speaker_text = part.split(":")
            if int(speaker_id) == 1:
                speaker_1 = text_to_speech(
                    speaker_text, model_id, default_speaker_1_description
                )
                podcast_waveform.append(speaker_1)
            elif int(speaker_id) == 2:
                speaker_2 = text_to_speech(
                    speaker_text, model_id, default_speaker_2_description
                )
                podcast_waveform.append(speaker_2)

    podcast_waveform = np.concatenate(podcast_waveform)
    write(filename, rate=sampling_rate, data=podcast_waveform)
