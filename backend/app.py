# -*- coding: UTF-8 -*-
"""Local-only Flask server.

Serves the built UI from ../frontend/dist and a single analysis endpoint.
Binds to 127.0.0.1 only, so nothing outside this machine can reach it.
"""
import os
import re

from flask import Flask, jsonify, request, send_from_directory

from wordlister import analyse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "frontend", "dist"))

ALLOWED_EXTENSIONS = {"txt", "srt", "md", "csv"}
MAX_UPLOAD_BYTES = 16 * 1024 * 1024
HOST = "127.0.0.1"
PORT = int(os.environ.get("PORT", 4242))

SRT_INDEX = re.compile(r"^\s*\d+\s*$")
SRT_TIMING = re.compile(r"^\s*\d{1,2}:\d{2}:\d{2}[,.]\d{1,3}\s*-->")
MARKUP = re.compile(r"<[^>]+>|\{\\[^}]*\}")

app = Flask(__name__, static_folder=None)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES


def extension_of(filename):
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def decode_bytes(data):
    """UTF-8 first (with or without BOM), then Windows-1252. Never fails."""
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return data.decode("cp1252", errors="replace")


def strip_srt(text):
    """Remove cue numbers, timing lines and inline markup from subtitle files."""
    kept = []
    for line in text.splitlines():
        if SRT_INDEX.match(line) or SRT_TIMING.match(line):
            continue
        kept.append(MARKUP.sub("", line))
    return "\n".join(kept)


def error(message, status):
    return jsonify(error=message), status


@app.errorhandler(413)
def too_large(_):
    return error("File is larger than 16 MB.", 413)


@app.get("/api/health")
def health():
    return {"ok": True}


@app.post("/api/analyze")
def analyze_endpoint():
    upload = request.files.get("file")
    if upload is not None and upload.filename:
        ext = extension_of(upload.filename)
        if ext not in ALLOWED_EXTENSIONS:
            return error(f"Unsupported file type .{ext or '?'}. Use txt, srt, md or csv.", 415)
        text = decode_bytes(upload.read())
        if ext == "srt":
            text = strip_srt(text)
        source = upload.filename
    else:
        payload = request.get_json(silent=True) or {}
        text = request.form.get("text") or payload.get("text") or ""
        source = "pasted text"

    if not text.strip():
        return error("Nothing to analyse: the input is empty.", 400)

    result = analyse(text)
    return {
        "info": {
            "time": result["elapsed"],
            "count": len(result["wordlist"]),
            "source": source,
        },
        "wordlist": result["wordlist"],
        "stats": result["stats"],
    }


@app.get("/", defaults={"path": "index.html"})
@app.get("/<path:path>")
def frontend(path):
    if not os.path.isfile(os.path.join(DIST_DIR, "index.html")):
        return (
            "The UI has not been built yet. Run `npm install && npm run build` in frontend/, "
            "or use `npm run dev` for live reload.",
            503,
        )
    if os.path.isfile(os.path.join(DIST_DIR, path)):
        return send_from_directory(DIST_DIR, path)
    return send_from_directory(DIST_DIR, "index.html")


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=False)
