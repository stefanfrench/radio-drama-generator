from typing import Dict, Optional

from pydantic import BaseModel

speaker_1_description = "Laura's voice is exciting and fast in delivery with very clear audio and no background noise."
speaker_2_description = (
    "Jon's voice is calm with very clear audio and no background noise."
)


class SpeakerConfig(BaseModel):
    model_id: str
    speaker_id: str
    speaker_description: Optional[str] = (
        None  # This description is used by the ParlerTTS model to configure the speaker profile
    )


class PodcastConfig(BaseModel):
    speakers: Dict[str, SpeakerConfig]
    sampling_rate: int = 44_100
