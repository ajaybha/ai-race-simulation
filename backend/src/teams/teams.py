from dataclasses import dataclass
import logging
import os
import json
import aiofiles
from typing import Any, Awaitable, Callable, Optional

# autogen
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.base import ChatAgent, TaskResult
from autogen_agentchat.messages import TextMessage, UserInputRequestedEvent
from autogen_agentchat.conditions import TextMentionTermination, ExternalTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core import CancellationToken
from autogen_core.models import ChatCompletionClient


# from repo
from agents import get_agent

# set logger for uvicorn
logger = logging.getLogger('uvicorn.info')

async def get_team(
    user_input_func: Callable[[str, Optional[CancellationToken]], Awaitable[str]],
    state_path: str = "team_state.json",
) -> RoundRobinGroupChat:
    """Create a team of agents."""
    # termination conditions.
    text_termination = TextMentionTermination("TERMINATE")
    # Create the team.
    agent = await get_agent("assistant")
    yoda = await get_agent("yoda")
    user_proxy = UserProxyAgent(
        name="user",
        input_func=user_input_func,  # Use the user input function.
    )
    team = RoundRobinGroupChat(
        [agent, yoda, user_proxy],termination_condition=text_termination
    )
    # Load state from file.
    if not os.path.exists(state_path):
        return team
    async with aiofiles.open(state_path, "r") as file:
        state = json.loads(await file.read())
    await team.load_state(state)
    return team

