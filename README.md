# Simple Summary

A lightweight news/article summarization API powered by FastAPI and an OpenAI-compatible LLM. Summaries are returned in Korean, limited to 3 sentences.

## Features

- **Text summary** — Send raw text, get a concise Korean summary.
- **URL scrape + summary** — Send a URL, the server scrapes the page and summarizes it.
- Long articles are automatically chunked and summarized in stages.
- Works with any OpenAI-compatible endpoint (local LLM, OpenAI, etc.).

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- An OpenAI-compatible API server (e.g. [LM Studio](https://lmstudio.ai/))

## Setup

```bash
git clone <repo-url> && cd simple-summary
cp .env.example .env   # edit if needed
uv sync
```

### Environment variables

| Variable | Default | Description |
|---|---|---|
| `OPENAI_BASE_URL` | `http://localhost:1234/v1` | LLM API base URL |
| `OPENAI_API_KEY` | `not-needed` | API key (set if using OpenAI) |
| `OPENAI_MODEL` | `local-model` | Model name to use |

## Usage

Start the server:

```bash
uv run python main.py
```

The server runs at `http://localhost:8585`. Interactive docs are available at `http://localhost:8585/docs`.

### POST /summary

Summarize plain text.

```bash
curl -X POST http://localhost:8585/summary \
  -H "Content-Type: application/json" \
  -d '{"text": "Your article text here..."}'
```

**Response:**

```json
{
  "summary": "Korean summary in up to 3 lines."
}
```

### POST /scrape-summary

Scrape a web page and summarize its content.

```bash
curl -X POST http://localhost:8585/scrape-summary \
  -H "Content-Type: application/json" \
  -d '{"url": "https://n.news.naver.com/mnews/article/..."}'
```

**Response:**

```json
{
  "summary": "Korean summary in up to 3 lines."
}
```

## Project Structure

```
simple-summary/
├── main.py              # FastAPI app, endpoints, lifespan
├── ai/
│   ├── open_ai_client.py  # OpenAI-compatible chat client
│   ├── summarizer.py      # Chunking + summarization logic
│   └── scraper.py         # URL fetching + HTML text extraction
├── pyproject.toml
└── .env.example
```

## License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
