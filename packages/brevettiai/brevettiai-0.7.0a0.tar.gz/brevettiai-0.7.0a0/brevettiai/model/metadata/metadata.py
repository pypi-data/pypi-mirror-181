import h5py
from pydantic import BaseModel, Field, parse_obj_as
from typing import Optional, Type, Dict
from brevettiai import Module
from brevettiai import __version__ as brevettiai_version

from brevettiai.io.h5_metadata import extract_metadata, get_metadata as h5_metadata


def _get_environment():
    return {
        "brevettiai": brevettiai_version,
    }


class ModelMetadata(BaseModel):
    id: str = Field(description="unique id of model")
    run_id: str = Field(description="Specifier of which training run created the model")
    model_version: Optional[str] = Field(default="", description="Specifier of model h5 file hash")
    name: str = Field(description="Name of model")
    producer: str = Field(description="Name of producing code")

    environment: Dict[str, str] = Field(default_factory=dict,
                                        description="Environment info at time of serialization,"
                                                    "updated when .json is called if empty")

    host_name: Optional[str] = Field(default=None, description="URI to host where more information may be found")

    class Config:
        json_encoders = {
            Module: lambda x: x.get_config()
        }

    def json(self, *args, **kwargs) -> str:
        if not self.environment:
            self.environment = _get_environment()
        return super().json(*args, **kwargs)


def get_metadata(file: str, metadata_type: Type[ModelMetadata] = ModelMetadata):
    if isinstance(file, h5py.File):
        return parse_obj_as(metadata_type, extract_metadata(file))
    if file.endswith(".h5"): # file is a string specifying the path
        return parse_obj_as(metadata_type, h5_metadata(file))
    else:
        raise NotImplementedError(f"Getting metadata from '{file}' not implemented")
