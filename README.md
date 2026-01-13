# RagSlides

RagSlides is a **Retrieval-Augmented Generation (RAG) system** that can generate **complete slide presentations directly from natural language prompts**.

The system retrieves structured and unstructured data from multiple sources (starting with **Google Sheets** and **Google Docs**) and uses that data to generate **presentation-ready slides**, including text, tables, and charts.

Example prompt:

> *“Please make a slide showing the graph of audience ratings for the past 5 years.”*

RagSlides will:
- Retrieve the relevant data from Google Sheets / Docs
- Understand the user intent
- Generate slide-ready content (e.g. bullet points, charts, summaries)

---

## Current Capabilities

- Ingest data from:
  - Google Sheets
  - Google Docs
- Convert external data into RAG-friendly documents
- Designed to be source-agnostic and extensible

---

## Planned Capabilities

- PDF ingestion (e.g. from Google Drive)
- Additional data sources (Notion, databases, APIs)
- Automatic slide layout generation
- Chart and visualization generation
- End-to-end “prompt → slide deck” workflow
- Pluggable embedding and LLM backends

---

## Installation

All dependencies (current and future) are managed via `requirements.txt`.

From the project root, run:

```bash
pip install -r requirements.txt
