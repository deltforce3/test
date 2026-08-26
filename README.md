# Starlight AI

一个星空主题的 AI 助手网页，通过 FastAPI 后端代理 Ollama 的 `/api/chat` 流式接口。

## 使用

1. 安装 Python 3.10 或更高版本，并在项目目录安装依赖：

	```powershell
	python -m pip install -r requirements.txt
	```

2. 安装并启动 [Ollama](https://ollama.com/)，然后准备一个模型：

	```powershell
	ollama serve
	ollama pull llama3.2
	```

3. 启动 FastAPI 后端：

	```powershell
	python -m uvicorn back:app --reload --host 0.0.0.0 --port 8000
	```

4. 访问 `http://localhost:8000`。网页会请求同源的 `/api/chat`，后端默认连接 `http://127.0.0.1:11434`。

如果 Ollama 不在本机，可先设置后端环境变量：

	```powershell
	$env:OLLAMA_URL = "http://你的 Ollama 服务器地址:11434"
	python -m uvicorn back:app --host 0.0.0.0 --port 8000
	```

直接双击 `web_1.html` 不再是完整运行方式，需要通过 FastAPI 地址访问。
