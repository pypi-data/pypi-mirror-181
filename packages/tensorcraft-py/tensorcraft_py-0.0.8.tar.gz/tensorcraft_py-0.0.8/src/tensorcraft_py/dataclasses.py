import typing
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from random import randint

from dataclasses_json import DataClassJsonMixin


class JobType(str, Enum):
  TEXT_2_IMAGE = "text2image"
  IMAGE_2_IMAGE = "image2image"

class JobState(str, Enum):
  UNKNOWN = "unknown"
  SUBMITTED = "submitted"
  ACCEPTED = "accepted"
  WORKING = "working"
  FINISHED = "finished"
  ERROR = "error"



@dataclass
class Text2ImageParams(DataClassJsonMixin):
  seed: int = randint(0, 1000000)


@dataclass
class ImageSize(DataClassJsonMixin):
  width: int
  height: int


@dataclass
class ImageData(DataClassJsonMixin):
  id: str
  user_secret_id: str
  prompt: str
  seed: int
  size: ImageSize
  source_image_id: typing.Optional[str]

  job_id: str
  uri: typing.Optional[str] = None
  image_bytes: typing.Optional[bytearray] = None
  creation_time: datetime = datetime.now()


@dataclass
class JobStatus(DataClassJsonMixin):
  job_id: str
  job_state: JobState
  progress_pct: float
  images: list[ImageData] = field(default_factory=list)
  image_uris: list[str] = field(default_factory=list)
  error: bool = False


@dataclass
class Image2ImageParams(DataClassJsonMixin):
  source_image_id: str
  strength: float = 0.5
  seeds: typing.Optional[list[int]] = None


@dataclass
class Job(DataClassJsonMixin):
  id: str
  user_secret_id: str
  job_type: JobType
  prompt: str
  batch_size: int = 5
  size: ImageSize = ImageSize(512, 512)

  ddim_steps: int = 50
  scale: float = 7.5

  text2image_params: typing.Optional[Text2ImageParams] = None
  image2image_params: typing.Optional[Image2ImageParams] = None

  creation_time: datetime = datetime.now()
  status: typing.Optional[JobStatus] = None


@dataclass
class Filter(DataClassJsonMixin):
  id: str
  name: str
  description: str
  user_secret_id: str
  prompt: str
  
  ddim_steps: int
  scale: float 
  strength: float
  
  creation_time: datetime = datetime.now()
