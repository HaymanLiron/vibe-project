import os
import sys
import json
import base64

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

flask = pytest.importorskip("flask")

import app as flask_app

SAMPLE_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWP4////fwAJ+wP7gfKTDwAAAABJRU5ErkJggg=="
)


def test_index_route(tmp_path, monkeypatch):
    monkeypatch.setattr(flask_app, "OUTPUT_DIR", str(tmp_path))
    paragraphs = ["p1", "p2", "p3", "p4"]
    with open(tmp_path / "paragraphs.json", "w", encoding="utf-8") as f:
        json.dump(paragraphs, f)
    with open(tmp_path / "image1.png", "wb") as f:
        f.write(SAMPLE_PNG)

    client = flask_app.app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.get_data(as_text=True)
    assert "p1" in data
