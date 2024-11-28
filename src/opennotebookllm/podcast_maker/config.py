from typing import Dict, Optional

from pydantic import BaseModel


class SpeakerConfig(BaseModel):
    model_id: str
    speaker_id: str
    speaker_description: Optional[str] = (
        None  # This description is used by the ParlerTTS model to configure the speaker profile
    )


class PodcastConfig(BaseModel):
    speakers: Dict[str, SpeakerConfig]
    sampling_rate: int = 44_100
