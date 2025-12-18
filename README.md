# ✨ Semantic Emoji Search

AI-powered emoji search engine. This application understands the *meaning* (semantics) behind your query to find the most relevant emojis. It supports over 50 languages and offers compound word analysis.

## Description

Semantic Emoji Search is a web application built with Streamlit that leverages vector embeddings to perform semantic searches. Unlike traditional search engines that rely on exact text matches, this tool uses a embedding model to understand the context and sentiment of your input.

Key features include:
- **Semantic Understanding**: Finds emojis conceptually related to your query (e.g., "sad" might return 😢, 🌧️, or 💔).
- **Multilingual Support**: Supports 50+ languages.
- **Compound Word Analysis**: Automatically breaks down compound words (e.g., "Sunflower" → "Sun" + "Flower") to provide granular emoji suggestions for each part (Supports 25+ languages).
- **Interactive UI**: Clean and responsive interface with grid visualizations.

## Technical Details

### Dataset
The application utilizes the [badrex/LLM-generated-emoji-descriptions](https://huggingface.co/datasets/badrex/LLM-generated-emoji-descriptions) dataset.

### Embedding Functions
The system supports state-of-the-art embedding models to capture semantic meaning:
- **`intfloat/multilingual-e5-base`**
- **`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`** (Default & Recommended)

### Language Support
- **Normal Search**: Supports **50+ languages**.
  > Details are in our publication *Making Monolingual Sentence Embeddings Multilingual using Knowledge Distillation*. We used the following 50+ languages: ar, bg, ca, cs, da, de, el, en, es, et, fa, fi, fr, fr-ca, gl, gu, he, hi, hr, hu, hy, id, it, ja, ka, ko, ku, lt, lv, mk, mn, mr, ms, my, nb, nl, pl, pt, pt-br, ro, ru, sk, sl, sq, sr, sv, th, tr, uk, ur, vi, zh-cn, zh-tw.
  [link](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html)

- **Compound Search**: Supports **25+ languages** (based on WordNet OMW-1.4).
  [link](https://omwn.org/omw1.html)

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- **Python** 3.13 or higher
- **pip** (Python package installer) or **uv** (Project manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository_url>
   cd emoji-search
   ```

2. **Install Dependencies**
   It is recommended to use a virtual environment.

   Using `pip`:
   ```bash
   pip install streamlit chromadb sentence-transformers nltk langdetect
   ```

   Using `uv` (if applicable):
   ```bash
   uv sync
   ```

3. **NLTK Data**
   The application will attempt to download necessary NLTK data (WordNet, OMW-1.4) on the first run. Ensure you have an internet connection.

## Configuration

The application expects a pre-populated vector database for the embeddings.

- **ChromaDB**: Ensure the `chroma_db` directory is present in the root of the project. This directory should contain the vector collection `LLM-generated-emoji-multilingual-MiniLM-L12-v2`.

*Note: If the database is missing, the search functionality will not work.*

## Usage

To start the application, run the following command in your terminal:

```bash
streamlit run app.py
```

Once the server starts, your default web browser will open to `http://localhost:8501`.

1. **Enter a Phrase**: Type any word or phrase into the search box (e.g., "Spicy food", "แมวน่ารัก", "Bonjour").
2. **View Results**: The most semantically relevant emojis will appear instantly.
3. **Compound Analysis**: If you enter a compound word (like "Firefly"), the app will also show results for the individual components ("Fire" + "Fly").

## Acknowledgements

This project makes use of several open-source libraries and datasets:

- **[Streamlit](https://streamlit.io/)** - For the web application framework.
- **[ChromaDB](https://www.trychroma.com/)** - For the vector database storage and retrieval.
- **[Sentence Transformers](https://www.sbert.net/)** - For generating semantic embeddings.
- **[NLTK](https://www.nltk.org/)** - For natural language processing and WordNet integration.
- **[LangDetect](https://pypi.org/project/langdetect/)** - For language detection.
- **[Open Multilingual Wordnet (OMW)](http://compling.hss.ntu.edu.sg/omw/)** - For multilingual support.
