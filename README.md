# Starlight AI

一个星空主题的 AI 助手网页，通过 FastAPI 后端代理 Ollama 的 `/api/chat` 流式接口,适合新手尝鲜。

## 使用

1. 安装 Python 3.10 或更高版本，并在项目目录安装依赖：

	```powershell
	python -m pip install -r requirements.txt
	```

2. 安装并启动 [Ollama](https://ollama.com/)，然后准备一个模型：

	```powershell
	ollama serve
	ollama pull deepseek-r1:1.5b
	```

3. 启动 FastAPI 后端：

	```powershell
	python -m uvicorn back:app --reload --host 0.0.0.0 --port 8000
	```

4. 访问 `http://localhost:8000`。网页会请求同源的 `/api/chat`，后端固定连接 `http://localhost:11434`。网页中的模型菜单会读取 Ollama 已部署的模型，默认选择 `deepseek-r1:1.5b`。

直接双击 `web_1.html` 不再是完整运行方式，需要通过 FastAPI 地址访问。
