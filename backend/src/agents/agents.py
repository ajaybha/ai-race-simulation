from dataclasses import dataclass
import os
import logging
import yaml
import aiofiles


# autogen
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.base import ChatAgent, TaskResult
from autogen_agentchat.messages import TextMessage, UserInputRequestedEvent
from autogen_agentchat.conditions import TextMentionTermination, ExternalTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core import CancellationToken
from autogen_core.models import ChatCompletionClient


# from repo
from schema import AgentInfo
from utils import EnvVarLoader

# set logger for uvicorn
logger = logging.getLogger('uvicorn.info')


@dataclass
class SimAgent:
    """ Simulated agent for the AI Race simulation. """
    agent_id: str
    description: str
    #agent: ChatAgent

sim_agents: dict[str, SimAgent] = {
    "assistant": SimAgent(
        agent_id="assistant",
        description="Assistant agent",
    ),
    "yoda": SimAgent(
        agent_id="yoda",
        description="Yoda agent",
    )
}


async def create_agent(
        agent_id: str
) -> ChatAgent:
    """Create a simulated agent based on the agent_id."""
    model_config_path = "./{path}/{config_file}".format(path="config", config_file="model_gemini_config.yaml")
    # Get model client from config.
    async with aiofiles.open(model_config_path, "r") as file:
        model_config = yaml.load(await file.read(), Loader=EnvVarLoader)
    logger.info(f"Model config: {model_config}")
    model_client = ChatCompletionClient.load_component(model_config)
    
    match agent_id: 
        case "assistant":
            return AssistantAgent(
                name="assistant",
                model_client=model_client,
                system_message="You are a helpful assistant.",
            )
        case "yoda":
            return AssistantAgent(
                name="yoda",
                model_client=model_client,
                system_message="Repeat the same message in the tone of Yoda.",
            )
        case _:
            raise ValueError(f"Unknown agent id: {agent_id}")


async def get_agent(agent_id: str) -> ChatAgent:
    return await create_agent(agent_id)


async def get_all_agent_info() -> list[AgentInfo]:
    return [
        AgentInfo(key=agent_id, description=agent.description) for agent_id, agent in sim_agents.items()
    ]


