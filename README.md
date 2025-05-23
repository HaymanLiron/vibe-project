# Vibe Project

This repository demonstrates a simple pipeline for extracting content from a PDF file and displaying it in a small web application. The goal is to

1. Download a PDF from a URL.
2. Extract two images and four paragraphs of text from that PDF.
3. Show one of the images in a webpage and display the associated text when the user clicks on specific regions of the image.

The code is intentionally minimal and focuses on the basic workflow. You will need to install the required Python packages listed in `requirements.txt` before running the scripts.

## Getting Started

```bash
# Install dependencies (may require internet access)
pip install -r requirements.txt

# Extract content from a PDF
python src/pdf_pipeline.py --url <PDF_URL> --output-dir output

# Run the web application
python src/app.py
```

Open `http://localhost:5000` in your browser to see the extracted image. Clicking on the defined regions will reveal the corresponding text paragraphs.

This is a starting point that can be expanded with additional features such as handling emails, processing multiple PDFs, and storing results in a database.
