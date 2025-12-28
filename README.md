# 🏗️ Indecimal RAG – Grounded AI Assistant for Construction Documents

**Indecimal RAG** is a fully runnable Retrieval-Augmented Generation (RAG) system designed for a construction marketplace.

It enables an AI assistant to answer user queries strictly using internal documents such as policies, FAQs, pricing details, and quality standards—without relying on the model’s general knowledge.

The system combines **semantic search** (FAISS + Sentence Transformers) with a **locally hosted LLM** (Qwen 2.5 via Ollama) to ensure responses are accurate, explainable, and hallucination-free.

---

## 🚀 Key Features

- 📄 **Semantic retrieval** from internal construction documents
- 🔍 **FAISS-based vector search** with cosine similarity
- 🧠 **Local LLM inference** using Ollama (no external APIs)
- 🛡️ **Strict grounding** to retrieved context (zero hallucination design)
- 🧾 **Transparent display** of retrieved chunks used for each answer
- 💬 **Interactive chatbot interface** built with Streamlit
- ⚡ **Optimized** for low-latency local execution

---

## 🏗️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Embeddings** | Sentence Transformers (all-MiniLM-L6-v2) |
| **Vector Search** | FAISS (IndexFlatIP – cosine similarity) |
| **LLM** | Qwen 2.5 (1.5B Instruct) via Ollama |
| **Backend Logic** | Python |
| **UI** | Streamlit |
| **Environment** | uv (dependency & lock management) |

---

## ✅ Prerequisites

- Python **3.10+**
- **Ollama** installed and running locally
- CPU-based inference (GPU optional, not required)
- Internet access for first-time model download


## 🧠 Models Used

### 🔹 Embedding Model
**Model:** `all-MiniLM-L6-v2`
* **Why chosen:**
    * Lightweight and fast for local usage
    * Strong semantic similarity performance
    * Ideal for cosine similarity search with FAISS
    * Widely adopted in production RAG pipelines

### 🔹 Large Language Model (LLM)
**Model:** `qwen2.5:1.5b-instruct`
* **Runtime:** Local inference using Ollama
* **Why chosen:**
    * Instruction-tuned for strict prompt adherence
    * Faster than larger models on CPU
    * Lower hallucination risk
    * Well-suited for extractive, grounded answers

> **Note:** The LLM is used only for answer generation, never for retrieval.

---

## 📄 Document Chunking & Processing

- Input documents are **Markdown (.md)** files
- Chunking follows **semantic document structure**, not fixed token sizes:
    - Document title → separate chunk
    - Document metadata → separate chunk
    - Each `##` section → individual chunk
- Each chunk includes metadata:
    - Source document
    - Section heading

**This ensures:**
* Meaningful, human-readable chunks
* High-quality retrieval
* Transparent source attribution

---

## 🔎 Retrieval Pipeline

1. User query is normalized
2. Intent is detected (e.g., payments, delays, accountability)
3. Underspecified queries are expanded using canonical phrasing
4. Query embedding is generated
5. Top-K chunks are retrieved via FAISS
6. Metadata-only chunks are excluded
7. Policy documents are prioritized for enforcement-related queries

*All retrieval happens locally and is deterministic.*

---

## 🛡️ Grounding & Hallucination Control

Grounding is enforced at three levels:

### 1️⃣ Retrieval Constraint
Only retrieved document chunks are passed to the LLM. The model never sees full documents or external knowledge.

### 2️⃣ Strict Prompt Rules
The LLM is explicitly instructed to:
* Use only the retrieved context
* Avoid inference or interpretation
* Avoid adding benefits, reasons, or outcomes
* Refuse to answer if information is missing

**Exact refusal response:**
> “The provided documents do not contain this information.”

### 3️⃣ Output Style Enforcement
* Short, factual statements
* Bullet points for multiple mechanisms
* No combined reasoning or assumptions

*This guarantees hallucination-free answers by design.*

---

## 🖥️ User Interface

Built using **Streamlit**.

**Displays:**
* User query
* Retrieved document chunks
* Final grounded answer

*Demonstrates full end-to-end RAG behavior (not a PoC).*

---

## 📁 Project Structure

```text
RAG/
├── rag_pipeline/
│   ├── ingestion_chunking.py
│   ├── embedding_indexing.py
│   ├── retrieval.py
│   ├── generation.py
│   └── __init__.py
│
├── data/
│   ├── raw/          # Input markdown documents
│   └── processed/    # Chunks, embeddings, FAISS index
│
├── app.py            # Streamlit app
├── pyproject.toml
├── uv.lock
├── requirements.txt
└── README.md
```
## ⚙️ Ollama Installation (Required)

### 🐧 Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh

```

### 🍎 macOS
Download and install from:
👉 [https://ollama.com/download](https://ollama.com/download)
*(Ollama runs in the background after installation)*

### 🪟 Windows
Download and install from:
👉 [https://ollama.com/download](https://ollama.com/download)

### 📥 Pull Required Model
```bash
ollama pull qwen2.5:1.5b-instruct
```

## ▶️ How to Run the Project

### 1. Environment Setup
```bash
uv venv
source .venv/bin/activate
uv pip sync
```

### 2. Run Ingestion & Indexing
```bash
python rag_pipeline/ingestion_chunking.py
python rag_pipeline/embedding_indexing.py
``` 

### 3. Start the App
```bash
streamlit run app.py
```

## 🧪 Evaluation & Testing

The system was tested with:
* Fact-based queries present in documents
* Queries missing from documents (refusal behavior)
* Accountability and delay-related questions
* Pricing and payment-related questions

**Observed behavior:**
* ✅ Accurate retrieval
* ✅ Correct grounded answers
* ✅ Explicit refusal when data is missing
* ✅ No hallucinated responses

---

## 👤 Author

**Devansh Kumar Sinha**
B.Tech Computer Science
Focused on AI Systems, RAG, and LLM Engineering

---

## 📜 License

This project is licensed under the **MIT License**.