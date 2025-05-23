"""Minimal Flask app to display an extracted image with interactive regions."""

from __future__ import annotations

import json
import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Directory containing extracted assets (images and paragraphs.json)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), os.pardir, "output")


@app.route("/")
def index():
    # Load paragraphs from JSON
    para_file = os.path.join(OUTPUT_DIR, "paragraphs.json")
    if os.path.exists(para_file):
        with open(para_file, "r", encoding="utf-8") as f:
            paragraphs = json.load(f)
    else:
        paragraphs = ["No paragraphs found"] * 4
    return render_template("index.html", paragraphs=paragraphs)


@app.route("/images/<path:filename>")
def images(filename):
    return send_from_directory(OUTPUT_DIR, filename)


if __name__ == "__main__":
    app.run(debug=True)
