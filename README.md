# AI Teaching Assistant

An AI-powered tool designed to assist students by answering course-related questions using Retrieval-Augmented Generation (RAG). Built for an NLP course, this project leverages `Llama-2-7b-Chat-GGUF` and `all-MiniLM-L6-v2` to provide context-aware responses from course materials.

## Overview

The AI Teaching Assistant (AI TA) automates responses to frequently asked questions (FAQs) and delivers precise answers based on ingested course documents (e.g., PDFs, CSVs). It uses a RAG pipeline to retrieve relevant content and generate responses, addressing the limitations of standalone LLMs by grounding answers in specific course context.

- **Key Features**:
  - Ingests and processes course files into a Chroma vector database.
  - Retrieves relevant chunks using lightweight embeddings.
  - Generates concise, accurate responses with a quantized LLM.
  - Runs locally on CPU with minimal resource demands.

## Requirements

- **Python**: 3.8+
- **Dependencies**: Install via `pip install -r requirements.txt` (see below for key libraries).
- **Hardware**: CPU (tested with 16 GB RAM); GPU optional for faster inference.
- **Course Files**: Place documents (e.g., PDFs, CSVs) in `SOURCE_DOCUMENTS/` for ingestion.

### Key Libraries

- `langchain` (RAG pipeline, document loaders)
- `transformers` (Hugging Face models)
- `chromadb` (vector database)
- `torch` (model execution)
- `llama-cpp-python` (GGUF model support)

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/[yourusername]/AI-Teaching-Assistant.git
   cd AI-Teaching-Assistant
2. ## Install Dependencies:
langchain
langchain-community
langchain-chroma
transformers
torch
llama-cpp-python
chromadb
click
sentence-transformers
nltk
