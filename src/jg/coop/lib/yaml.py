from pydantic import BaseModel, ConfigDict

class YAMLConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
