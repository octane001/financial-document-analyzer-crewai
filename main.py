from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import json

from crewai import Crew, Process
from agents import financial_analyst
from task import analyze_financial_document
from tools import FinancialDocumentTool

app = FastAPI(title="Financial Document Analyzer")
from database import engine
from models import Base

Base.metadata.create_all(bind=engine)


def run_crew(query: str, file_path: str):
    """
    Backend-controlled PDF loading + safe truncation
    """

    # 1️⃣ Extract PDF text
    tool = FinancialDocumentTool()
    document_text = tool._run(file_path)

    # 2️⃣ Prevent token overflow (Groq free-tier safe)
    MAX_CHARS = 8000
    document_text = document_text[:MAX_CHARS]

    # 3️⃣ Run Crew
    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[analyze_financial_document],
        process=Process.sequential,
    )

    result = financial_crew.kickoff({
        "query": query,
        "document_text": document_text
    })

    return result


@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}


# @app.post("/analyze")
# async def analyze_financial_endpoint(
#     file: UploadFile = File(...),
#     query: str = Form(default="Analyze this financial document for investment insights")
# ):
#     """
#     Upload financial PDF and return structured investment analysis
#     """

#     file_id = str(uuid.uuid4())
#     file_path = f"data/financial_document_{file_id}.pdf"

#     try:
#         os.makedirs("data", exist_ok=True)

#         # Save uploaded file
#         with open(file_path, "wb") as f:
#             content = await file.read()
#             f.write(content)

#         if not query or query.strip() == "":
#             query = "Analyze this financial document for investment insights"

#         # 🔥 Run analysis
#         response = run_crew(query=query.strip(), file_path=file_path)

#         # 4️⃣ Parse CrewAI response safely
#         parsed_output = None

#         try:
#             # Crew returns object with .raw
#             parsed_output = json.loads(response.raw)
#         except:
#             # fallback if already dict or different format
#             try:
#                 parsed_output = response.raw
#             except:
#                 parsed_output = str(response)

#         return {
#             "status": "success",
#             "query": query,
#             "analysis": parsed_output,
#             "file_processed": file.filename
#         }

#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error processing financial document: {str(e)}"
#         )

#     finally:
#         if os.path.exists(file_path):
#             try:
#                 os.remove(file_path)
#             except:
#                 pass

from database import SessionLocal
from models import AnalysisResult
from tasks import process_analysis

@app.post("/analyze")
async def analyze_financial_endpoint(file: UploadFile = File(...), query: str = Form(...)):

    db = SessionLocal()

    file_id = str(uuid.uuid4())
    file_path = f"data/{file_id}.pdf"

    os.makedirs("data", exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    new_record = AnalysisResult(
        file_name=file.filename,
        query=query,
        status="PENDING"
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    # 🔥 Send to background worker
    process_analysis.delay(new_record.id, query, file_path)

    db.close()

    return {
        "job_id": new_record.id,
        "status": "PENDING",
        "message": "Analysis started. Use /status/{job_id} to check progress."
    }
    
    
@app.get("/status/{job_id}")
def get_status(job_id: int):

    db = SessionLocal()
    record = db.query(AnalysisResult).filter(AnalysisResult.id == job_id).first()
    db.close()

    if not record:
        return {"error": "Job not found"}

    return {
        "job_id": record.id,
        "status": record.status,
        "result": json.loads(record.result_json) if record.result_json else None
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)