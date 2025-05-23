"""Utilities for downloading a PDF and extracting content.

This module relies on the ``PyMuPDF`` package (imported as ``fitz``) to read the
PDF, extract images, and capture text. The extracted images and text are saved to
a specified output directory.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from typing import List

import fitz  # PyMuPDF
import requests


@dataclass
class ExtractedContent:
    images: List[str]
    paragraphs: List[str]


def download_pdf(url: str, output_path: str) -> None:
    """Download a PDF from ``url`` and save it to ``output_path``."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)


def extract_content(pdf_path: str, output_dir: str) -> ExtractedContent:
    """Extract two images and four paragraphs from ``pdf_path``.

    The images are saved as ``image1.png`` and ``image2.png`` in ``output_dir``.
    The paragraphs are returned as a list of strings.
    """
    doc = fitz.open(pdf_path)
    os.makedirs(output_dir, exist_ok=True)

    # Extract first two images found in the document
    images = []
    img_count = 0
    for page in doc:
        for img in page.get_images(full=True):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n > 4:  # convert CMYK or other to RGB
                pix = fitz.Pixmap(fitz.csRGB, pix)
            img_path = os.path.join(output_dir, f"image{img_count + 1}.png")
            pix.save(img_path)
            images.append(img_path)
            img_count += 1
            if img_count == 2:
                break
        if img_count == 2:
            break

    # Extract text and split into paragraphs. This is simplistic and assumes
    # paragraphs are separated by blank lines.
    full_text = "\n".join(page.get_text() for page in doc)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", full_text) if p.strip()]
    paragraphs = paragraphs[:4]

    return ExtractedContent(images=images, paragraphs=paragraphs)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract images and text from a PDF")
    parser.add_argument("--url", required=True, help="URL to the PDF file")
    parser.add_argument("--output-dir", default="output", help="Directory to save results")
    args = parser.parse_args()

    pdf_path = os.path.join(args.output_dir, "source.pdf")
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"Downloading PDF from {args.url}...")
    download_pdf(args.url, pdf_path)

    print("Extracting content...")
    content = extract_content(pdf_path, args.output_dir)

    # Save paragraphs to JSON for the web app
    with open(os.path.join(args.output_dir, "paragraphs.json"), "w", encoding="utf-8") as f:
        json.dump(content.paragraphs, f, ensure_ascii=False, indent=2)

    print("Done. Extracted files:")
    for path in content.images:
        print("  ", path)
    print("  paragraphs.json")


if __name__ == "__main__":
    main()
