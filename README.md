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

1. If you have videos, convert them to MP3 first (use `mp4_to_mp3.py`):

```bash
# example: convert a single video
python mp4_to_mp3.py input_video.mp4 output_audio.mp3
```

2. Convert MP3(s) to JSON chunks (use `mp3_to_json.py`):

```bash
# example: convert one mp3 to a chunked JSON file
python mp3_to_json.py input_audio.mp3 jsons/output_audio.json
```

3. Start your embedding service (make sure it is reachable at the address above).

4. Generate embeddings for all chunk JSON files:

```bash
python read_chunks.py
```

5. Run the query handler to ask questions using the indexed chunks:

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

Files (what each script does)

- `mp4_to_mp3.py`: Extracts the audio track from an MP4 video and saves it as an MP3 file. Use this when your source material is video and you want to transcribe the audio.
- `mp3_to_json.py`: Converts an MP3 audio file into a JSON file of transcribed chunks. It typically calls a speech-to-text tool (e.g., Whisper) to transcribe audio, splits the transcription into smaller chunk objects, and writes them into the `jsons/` folder so they can be embedded.
- `read_chunks.py`: Reads all JSON chunk files from the `jsons/` folder, collects the `text` fields from each chunk, and calls the local embedding API to create embeddings for those chunks. The script prints or stores embeddings for later retrieval.
- `process_incoming_query.py`: The query entrypoint. Accepts a user query, compares it against the stored embeddings to find relevant chunks, and composes an answer using the matched content (and optionally a local LLM).


