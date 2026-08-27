import json
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


PROJECT_DIR = Path(__file__).resolve().parent
OLLAMA_URL = "http://localhost:11434"
app = FastAPI(title="Starlight AI API")
app.mount("/static", StaticFiles(directory=PROJECT_DIR), name="static")


class ChatRequest(BaseModel):
	model: str = Field(min_length=1, max_length=120)
	messages: list[dict[str, str]] = Field(min_length=1)


@app.get("/")
async def index() -> FileResponse:
	return FileResponse(PROJECT_DIR / "web_1.html")


@app.get("/favicon.ico")
async def favicon() -> Response:
	return Response(status_code=204)


@app.get("/api/models")
async def models() -> dict[str, list[str]]:
	try:
		async with httpx.AsyncClient(timeout=10) as client:
			response = await client.get(f"{OLLAMA_URL}/api/tags")
			response.raise_for_status()
			data = response.json()
			return {"models": [model["name"] for model in data.get("models", []) if model.get("name")]}
	except httpx.HTTPError as error:
		raise HTTPException(status_code=502, detail=f"无法读取 Ollama 模型列表: {error}") from error


@app.post("/api/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
	payload = {"model": request.model, "messages": request.messages, "stream": True}

	async def stream_response():
		try:
			async with httpx.AsyncClient(timeout=None) as client:
				async with client.stream("POST", f"{OLLAMA_URL}/api/chat", json=payload) as response:
					if response.status_code != 200:
						detail = await response.aread()
						raise HTTPException(response.status_code, detail.decode("utf-8", errors="replace"))
					async for line in response.aiter_lines():
						if line:
							yield f"{line}\n"
		except httpx.ConnectError as error:
			error_payload = {"error": "无法连接 Ollama，请确认 Ollama 已启动。"}
			yield json.dumps(error_payload, ensure_ascii=False) + "\n"
		except HTTPException as error:
			error_payload = {"error": f"Ollama 返回 HTTP {error.status_code}: {error.detail}"}
			yield json.dumps(error_payload, ensure_ascii=False) + "\n"

	return StreamingResponse(stream_response(), media_type="application/x-ndjson")
