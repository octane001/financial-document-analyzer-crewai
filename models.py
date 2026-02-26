from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    query = Column(String)
    result_json = Column(Text)
    status = Column(String, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)