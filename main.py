from __future__ import annotations

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ai import OpenAIClient, Summarizer

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = OpenAIClient(
        base_url=os.getenv("OPENAI_BASE_URL", "http://localhost:1234/v1"),
        api_key=os.getenv("OPENAI_API_KEY", "not-needed"),
        model=os.getenv("OPENAI_MODEL", "local-model"),
    )
    app.state.summarizer = Summarizer(client)
    yield


app = FastAPI(lifespan=lifespan)


class SummaryRequest(BaseModel):
    text: str


class SummaryResponse(BaseModel):
    summary: str


@app.post("/summary", response_model=SummaryResponse)
async def summarize(req: SummaryRequest):
    try:
        result = app.state.summarizer.summarize(req.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    return SummaryResponse(summary=result.text)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8585, reload=True)
