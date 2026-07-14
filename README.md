# RAG System — Quick Start (Beginner)

What this does

This small project shows how to:
- Split documents into chunks stored as JSON files in `jsons/`.
- Create embeddings for each chunk using a local embedding API.
- Run a simple query script to find relevant chunks and answer questions.

Prerequisites

- Python 3.8 or newer
- An embedding service running at `http://localhost:11434/api/embed`
  - It should accept JSON like `{ "model": "bge-m3", "input": <string_or_list> }` and return `{ "embeddings": ... }`.
- Install required Python packages:
- Download and install ollama from ollama website

```bash
pip install -r requirements.txt
# or if you don't have requirements.txt
pip install requests scikit-learn joblib
```

Folder layout

- `read_chunks.py` — reads files from `jsons/`, calls the embedding API, and builds embeddings.
- `process_incoming_query.py` — run this to ask questions against the indexed chunks.
- `jsons/` — put your chunk files here. Each file should look like:

```json
{
  "chunks": [
    {"text": "first chunk text"},
    {"text": "second chunk text"}
  ]
}
```

Step-by-step: how to run (beginner-friendly)

1. Start your embedding service (make sure it is reachable at the address above).
2. Put one or more JSON chunk files into the `jsons/` folder using the format above.
3. Generate embeddings for all chunks:

```bash
python read_chunks.py
```

4. Run the query handler to ask questions using the indexed chunks:

```bash
python process_incoming_query.py
```

Common issues and quick fixes

- Connection refused: check the embedding service URL and that the service is running.
- ImportError: run the pip install commands shown earlier.
- Unexpected embedding format: inspect the raw API response — the code expects `embeddings` in the JSON.

Simple tips

- Keep `print` debug lines while developing, then remove them later to reduce noise.
- To use another embedding model, change the `"model"` field in `read_chunks.py`.

If you want this even shorter or want examples of chunking code, tell me which part to expand.
