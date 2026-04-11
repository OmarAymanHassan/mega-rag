# mega-rag

This project for implementing End to End Rag system from scratch


## Requirements
- python >=3.12.0

## Installing dependencies

1. Using `uv`

```bash
$ uv sync
```

or Using requirements.txt
```bash
$ uv add -r requirements.txt
```

2. Activate the `.venv`


## Setup the Environment
```bash
$ cp .env.example .env`
```
- Set your environemntal variables inside `.env` like `GEMINI_API_KEY`



3. Run the Docker Compose File
```bash
$ cd docker 
$ cp .env.example .env
```
- Update .env with your credentials

4. Run the FastAPI Server

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
