# English Wordlister

Classifies the words of any English text by **part of speech** and **Oxford level**. It runs entirely on your machine: a local Flask server and a React UI, with no external services, CDNs, or databases.

## Classes
- Types: Noun, Verb, Phrasal verb, Adjective, Undefined
- Oxford levels: A1, A2, B1, B2, C1, Other

## Features
- Paste text, or upload a file by drag and drop: `.txt`, `.srt`, `.md`, `.csv`, up to 16 MB
- SRT subtitles: cue numbers, timings and inline markup are stripped before analysis
- Encoding fallback: UTF-8 (with or without BOM), then Windows-1252
- Filter by type and level, search, sort, and paginate
- Export the current view as CSV or TXT (generated in the browser)
- The last pasted text is remembered in the browser

## Running it

Requirements: Python 3.9+ and Node 18+.

```bash
# backend (Flask is the only Python dependency)
cd backend
pip install -r requirements.txt
python app.py                  # serves on http://127.0.0.1:4242

# frontend: build once, the backend then serves the UI
cd ../frontend
npm install
npm run build                  # open http://127.0.0.1:4242
```

For development with live reload:

```bash
cd frontend && npm run dev     # http://127.0.0.1:5173, /api is proxied to the backend
```

The server binds to `127.0.0.1` only, so other machines cannot reach it.

## Layout
- `backend/wordlister.py`: analysis engine (tokenise, clean, lemmatise, merge phrasal verbs, classify). Pure functions with no module-level state.
- `backend/app.py`: local HTTP server, upload handling, and UI hosting
- `backend/datasets.py`, `backend/oxfords.py`: word lists
- `frontend/src/`: React UI (`components/`, plus `lib/` for API and export helpers)
