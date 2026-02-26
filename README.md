# 🏦 Financial Document Analyzer

A production-ready AI-powered financial document analysis system built with CrewAI, FastAPI, Celery, and Redis.

---

## 🐛 Bugs Found and Fixes Applied

This section documents all major bugs, issues, and architectural limitations discovered in the original codebase and how they were resolved.

---

```
🚨 Note: I used Groq AI api's key for this code because i don't have any paid api of OPEN_AI so i gone for free alternative and this alternative comes with 
a limitation this the amount of tokens processed. But, This is not a big issue just replace this 
```
llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
)
```
with the orignal one and add the OPEN_AI_ API_KEY in .env file, But this version is also working perfect and satisfing all the requirements of the Internship Task.
```

### 1. Incorrect `FinancialDocumentTool` Implementation

**❌ Problem**

The original tool was defined as a simple async function instead of a proper CrewAI tool. This caused errors such as:

```
'function' object has no attribute 'get'
```

CrewAI expects tools to inherit from `BaseTool`.

**✅ Solution**

Converted tool into a proper CrewAI `BaseTool` class.

```python
from crewai.tools import BaseTool
from langchain_community.document_loaders import PyPDFLoader

class FinancialDocumentTool(BaseTool):
    name: str = "financial_document_reader"
    description: str = "Reads a financial PDF document."

    def _run(self, path: str) -> str:
        loader = PyPDFLoader(path)
        docs = loader.load()

        full_text = ""
        for doc in docs:
            full_text += doc.page_content + "\n"

        return full_text
```

---

### 2. Tool Not Receiving Correct File Path

**❌ Problem**

CrewAI agent was trying to read invalid paths like:

```
../financial_document.pdf
path_to_financial_document.pdf
```

This caused file not found errors.

**✅ Solution**

Handled file reading in backend and passed document text directly to Crew.

```python
tool = FinancialDocumentTool()
document_text = tool._run(file_path)

result = crew.kickoff({
    "query": query,
    "document_text": document_text
})
```

---

### 3. Hallucination-Prone and Unsafe Prompts

**❌ Problem**

Original prompts encouraged hallucination and fake investment advice:

- Make up financial data
- Recommend random crypto assets
- Include fake websites

This made output unreliable and unsafe.

**✅ Solution**

Rewrote prompts to enforce strict financial analysis.

```python
description = """
Analyze financial document and extract:
- revenue trends
- net income trends
- cash flow
- risk level

Do not fabricate data.
Use only document content.
"""
```

---

### 4. API Key Authentication Errors

**❌ Problem**

```
AuthenticationError: Incorrect API key provided
```

Cause:
- Missing API key
- Expired key
- Billing not enabled

**✅ Solution**

Created `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

Loaded using:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

### 5. Token Limit Exceeded Error

**❌ Problem**

```
RateLimitError: Request too large
```

PDF contained too much text.

**✅ Solution**

Added safe truncation:

```python
MAX_CHARS = 8000
document_text = document_text[:MAX_CHARS]
```

---

### 6. Blocking API (Slow Performance)

**❌ Problem**

Original system processed analysis synchronously.

This caused:
- Slow response
- No scalability
- API blocking

**✅ Solution: Implemented Queue Worker Model using Celery and Redis**

Workflow:

```
User Request
    ↓
FastAPI
    ↓
Redis Queue
    ↓
Celery Worker
    ↓
CrewAI
    ↓
Database
```

This enables:
- Async processing
- Concurrent requests
- Scalability

---

### 7. No Database to Store Results

**❌ Problem**

Results were not stored. User could not retrieve previous analysis.

**✅ Solution: Added SQLAlchemy Database**

```python
class AnalysisJob(Base):
    __tablename__ = "analysis_jobs"

    id = Column(Integer, primary_key=True)
    status = Column(String)
    result = Column(Text)
```

---

### 8. No Job Tracking System

**❌ Problem**

User could not check analysis progress.

**✅ Solution: Added Job Status Endpoint**

Submit analysis:

```
POST /analyze
```

Response:

```json
{
  "job_id": 1,
  "status": "PENDING"
}
```

Check status:

```
GET /status/1
```

---

### 9. Celery Not Working on Windows

**❌ Problem**

```
PermissionError: Access denied
```

**✅ Solution**

Used solo worker mode:

```bash
celery -A tasks.celery worker --pool=solo --loglevel=info
```

---

## 🚀 Setup Instructions (Step-by-Step)

Follow these steps to run the project on any system.

### Step 1 — Clone Repository

```bash
git clone https://github.com/yourusername/financial-document-analyzer-debug.git
cd financial-document-analyzer-debug
```

### Step 2 — Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

**Windows:**
```bash
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Create `.env` File

```env
OPENAI_API_KEY=your_api_key_here
```

### Step 5 — Start Redis Server

Using Docker:

```bash
docker run -d -p 6379:6379 redis
```

### Step 6 — Start Celery Worker

```bash
celery -A tasks.celery worker --pool=solo --loglevel=info
```

### Step 7 — Start FastAPI Server

```bash
uvicorn main:app --reload
```

### Step 8 — Open Swagger UI

Open in your browser:

```
http://127.0.0.1:8000/docs
```

### Step 9 — Test API

Upload PDF:

```
POST /analyze
```

Check result:

```
GET /status/{job_id}
```

---

## ✅ Final System Features

| Feature | Status |
|---|---|
| Financial PDF Analysis | ✔ |
| CrewAI Multi-Agent System | ✔ |
| Async Processing using Celery | ✔ |
| Redis Queue Integration | ✔ |
| SQL Database Integration | ✔ |
| Job Tracking System | ✔ |
| Production-Ready Architecture | ✔ |