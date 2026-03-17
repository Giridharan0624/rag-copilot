# 🧠 NeuroStack RAG Copilot

A production-ready **Retrieval-Augmented Generation (RAG)** SaaS Support Copilot built with Django, React, FAISS, BM25, and Groq LLM.

---

## 🏗️ Architecture

```
┌──────────────┐     ┌──────────────────────────────────────────┐
│  React (Vite)│────▶│  Django REST API                         │
│  + TailwindCSS│     │  ├── /api/auth/signup/  (JWT)           │
│              │◀────│  ├── /api/auth/login/   (JWT)           │
│  localhost:  │     │  └── /api/query/        (RAG Pipeline)  │
│  5173        │     │       │                                  │
└──────────────┘     │       ▼                                  │
                     │  ┌─────────────────────┐                │
                     │  │ Hybrid Retrieval     │                │
                     │  │ ├── FAISS (Semantic) │                │
                     │  │ └── BM25  (Keyword)  │                │
                     │  └─────────┬───────────┘                │
                     │            ▼                             │
                     │  ┌─────────────────────┐                │
                     │  │ Groq LLM (LLaMA 3)  │                │
                     │  └─────────┬───────────┘                │
                     │            ▼                             │
                     │  ┌─────────────────────┐                │
                     │  │ Hallucination Control│                │
                     │  │ ├── Relevance Check  │                │
                     │  │ └── Answer Validation│                │
                     │  └─────────────────────┘                │
                     └──────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Groq API key ([get one free](https://console.groq.com))

### 1. Clone & Install Backend

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# backend/.env
SECRET_KEY=your-secret-key
DEBUG=True
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Build FAISS Index

```bash
cd backend
python -m rag.build_index
```

### 4. Run Migrations & Start Backend

```bash
cd backend
python manage.py migrate
python manage.py runserver 8000
```

### 5. Install & Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit **http://localhost:5173** — sign up and start chatting!

---

## 📝 Sample Queries

| Query | Expected Behavior |
|---|---|
| "How do I reset my password?" | ✅ Context-grounded answer with sources |
| "What are the pricing plans?" | ✅ Detailed plan comparison |
| "Tell me about quantum physics" | ❌ Fallback response (out of context) |
| "How do I set up SSO?" | ✅ Enterprise SSO setup instructions |

---

## 🔍 RAG Pipeline Flow

1. **User submits query** → JWT-authenticated `POST /api/query/`
2. **Hybrid Retrieval** → FAISS semantic (60%) + BM25 keyword (40%)
3. **Relevance Check** → Average score must exceed threshold (0.25)
4. **LLM Generation** → Groq API with context-only system prompt
5. **Answer Validation** → Second LLM call verifies answer is grounded
6. **Response** → Answer + sources + scores + confidence returned

---

## 🛡️ Hallucination Control

- **Relevance Threshold**: Rejects results with avg. score < 0.25
- **Context-Only Prompt**: System prompt forbids external knowledge
- **LLM Validation**: Second Groq call fact-checks the answer
- **Fallback Response**: Clear message when unable to answer

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.1 + DRF |
| Auth | JWT (SimpleJWT) |
| Frontend | React 19 (Vite) + TailwindCSS |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector DB | FAISS (Inner Product) |
| Keyword Search | BM25 (rank-bm25) |
| LLM | Groq API (llama3-8b-8192) |

---

## 📁 Project Structure

```
rag-copilot/
├── backend/
│   ├── core/           # Django project settings
│   ├── accounts/       # Auth (signup/login)
│   ├── rag/            # RAG pipeline
│   │   ├── build_index.py   # FAISS index builder
│   │   ├── retriever.py     # Hybrid search
│   │   ├── llm.py           # Groq integration
│   │   ├── validator.py     # Hallucination control
│   │   ├── pipeline.py      # Pipeline orchestrator
│   │   ├── views.py         # API endpoint
│   │   └── serializers.py   # Request/response schemas
│   ├── .env            # Environment variables
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # ChatBox, MessageBubble, SourcePanel, AuthForm
│   │   ├── pages/           # Login, Signup, Dashboard
│   │   └── services/api.js  # Axios + JWT interceptor
│   └── vite.config.js       # Vite + Tailwind + API proxy
└── data/
    ├── docs.json             # 35 FAQ entries
    └── faiss_index/          # FAISS index + chunks
```

## 🚀 Deployment

### Part 1: Deploy Backend to Hugging Face Spaces (Docker)
1. **Create Space**: Create a new Docker Space on Hugging Face.
2. **Upload Code**: Upload the entire `backend/` folder (including the provided `Dockerfile` and updated `requirements.txt`). Do NOT upload your local `.env`.
3. **Set Secrets**: Go to Space Settings -> Variables and secrets:
   - `GROQ_API_KEY`: Your API Key
   - `SECRET_KEY`: A secure random string
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `*` (or your specific space URL)
4. **Build**: HF will automatically build the Docker container and expose the API on port 7860. Grab the assigned URL as your new `API_BASE`.

### Part 2: Deploy Frontend to Netlify
1. **Update API URL**: Edit `frontend/src/services/api.js` and change `const API_BASE = '/api';` to your Hugging Face Space URL.
2. **Build App**: Run `npm run build` inside the `frontend/` directory. (The provided `public/_redirects` ensures React Router works correctly on Netlify).
3. **Deploy**: Drag and drop the generated `frontend/dist` folder into Netlify Drop, or connect your GitHub repository to Netlify, setting the build command to `npm run build` and publish dir to `frontend/dist`.

---

## 🔮 Future Improvements

- Chat history persistence (database)
- Streaming responses (WebSocket)
- Admin FAQ upload endpoint
- Multi-document chunking with overlap
- Rate limiting
- User analytics dashboard
