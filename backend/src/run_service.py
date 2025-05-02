import asyncio
import sys
import uvicorn
from dotenv import load_dotenv


load_dotenv()


# Example usage
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("service:app", host="0.0.0.0", port=8002, log_level="info")