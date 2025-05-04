import json
import os
import logging
import yaml
import aiofiles
from typing import Any, Awaitable, Callable, Optional

# fastapi
from fastapi import FastAPI, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles

# autogen
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import TextMessage, UserInputRequestedEvent
from autogen_agentchat.conditions import TextMentionTermination, ExternalTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core import CancellationToken
from autogen_core.models import ChatCompletionClient

# repo
from utils import EnvVarLoader
from agents import get_agent
from teams import get_team

logger = logging.getLogger('uvicorn.info')
app = FastAPI()
logger.info("Starting FastAPI server...")
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


model_config_path = "./config/model_gemini_config.yaml"
state_path = "team_state.json"
history_path = "team_history.json"
chat_interface_html_path = "app_team.html"


# serve static files
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def root():
    """Serve the chat interface HTML file."""
    return FileResponse(chat_interface_html_path)

@app.get("/api/history")
async def history() -> list[dict[str, Any]]:
    """Get the chat history."""
    try:
        # get the chat history 
        return await get_history()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@app.websocket("/ws/chat")
async def  chat(websocket: WebSocket):
    await websocket.accept()

    # user input function used by the team
    async def _user_input_func(prompt: str, cancel_token: CancellationToken | None) -> str:
        data = await websocket.receive_json()
        message = TextMessage.model_validate(data)
        return message.content
    
    try:
        while True:
            # get user message.
            data = await websocket.receive_json()
            request = TextMessage.model_validate(data)

            try: 
                # get the team and respond to the message
                team = await get_team(_user_input_func, state_path)
                history = await get_history()
                stream = team.run_stream(task = request)
                async for message in stream:
                    if isinstance(message, TaskResult):
                        logger.info(f"Task result: {message.model_dump()}")
                        # send the task result to the client
                        continue
                    await websocket.send_json(message.model_dump())
                    if not isinstance(message, UserInputRequestedEvent):
                        # don't save user input events to history
                        history.append(message.model_dump())
                        logger.info(f"History: {history}")
                
                state = await team.save_state()

                # Save team state to file.
                async with aiofiles.open(state_path, "w") as file:                    
                    await file.write(json.dumps(state))

                # Save chat history to file.
                async with aiofiles.open(history_path, "w") as file:
                    await file.write(json.dumps(history))
            
            except Exception as e:
                 # Send error message to client
                error_message = {
                    "type": "error",
                    "content": f"Error: {str(e)}",
                    "source": "system"
                }
                await websocket.send_json(error_message)
                # Re-enable input after error
                await websocket.send_json({
                    "type": "UserInputRequestedEvent",
                    "content": "An error occurred. Please try again.",
                    "source": "system"
                })

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        try:
            await websocket.send_json({
                "type": "error",
                "content": f"Unexpected error: {str(e)}",
                "source": "system"
            })
        except:
            pass



# helper methods
async def get_history() -> list[dict[str, Any]]:
    """Get chat history from file."""
    if not os.path.exists(history_path):
        return []
    async with aiofiles.open(history_path, "r") as file:
        return json.loads(await file.read())
    

