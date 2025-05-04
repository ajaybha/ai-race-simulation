from typing import Any, Literal, NotRequired
from pydantic import BaseModel, Field, SerializeAsAny
from typing_extensions import TypedDict

from schema.models import AllModelEnum


class AgentInfo(BaseModel):
    """ information about an available agent """

    key:str = Field(
        description="Agent key",
        examples=["corporate", "country"]
    )
    description:str = Field(
        description="Description of the agent",
        examples=["A corporate agent representing an AI company", "A country agent representing a country"]
    )

class ServiceMetadata(BaseModel):
    """ Metadata about the service including available agents and models. """   

    agents: list[AgentInfo] = Field(
        description="List of available agents.",
    )
    models: list[AllModelEnum] = Field(
        description="List of available LLMs.",
    )
    default_agent: str = Field(
        description="Default agent used when none is specified.",
        examples=["research-assistant"],
    )
    default_model: AllModelEnum = Field(
        description="Default model used when none is specified.",
    )

