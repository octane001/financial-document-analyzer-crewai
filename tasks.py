import json
from celery_app import celery
from tools import FinancialDocumentTool
from crewai import Crew, Process
from agents import financial_analyst
from task import analyze_financial_document
from database import SessionLocal
from models import AnalysisResult

@celery.task
def process_analysis(job_id, query, file_path):

    db = SessionLocal()

    try:
        tool = FinancialDocumentTool()
        document_text = tool._run(file_path)

        MAX_CHARS = 8000
        document_text = document_text[:MAX_CHARS]

        crew = Crew(
            agents=[financial_analyst],
            tasks=[analyze_financial_document],
            process=Process.sequential,
        )

        result = crew.kickoff({
            "query": query,
            "document_text": document_text
        })

        parsed = json.loads(result.raw)

        record = db.query(AnalysisResult).filter(AnalysisResult.id == job_id).first()
        record.result_json = json.dumps(parsed)
        record.status = "COMPLETED"

        db.commit()

    except Exception as e:
        record = db.query(AnalysisResult).filter(AnalysisResult.id == job_id).first()
        record.status = "FAILED"
        db.commit()

    finally:
        db.close()