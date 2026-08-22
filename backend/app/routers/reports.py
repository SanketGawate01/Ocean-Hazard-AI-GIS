from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from .. import models, schemas
from ..database import get_db
# Import our newly created real ML pipeline
from ..ml.predict import get_hazard_prediction

router = APIRouter(prefix="/api/reports", tags=["Reports"])

@router.post("/", response_model=schemas.ReportOut, status_code=status.HTTP_201_CREATED)
def create_report(report: schemas.ReportCreate, db: Session = Depends(get_db)):
    # 1. Save base report
    db_report = models.Report(
        description=report.description, latitude=report.latitude,
        longitude=report.longitude, image_url=report.image_url
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    # 2. RUN REAL ML PIPELINE
    ml_result = get_hazard_prediction(report.description)
    
    # 3. Save ML results linked to report
    db_prediction = models.MLPrediction(
        report_id=db_report.id, 
        predicted_category=ml_result["predicted_category"],
        confidence=ml_result["confidence"], 
        severity=ml_result["severity"]
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_report)
    
    return db_report

@router.get("/", response_model=List[schemas.ReportOut])
def get_reports(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(models.Report).options(joinedload(models.Report.prediction)).offset(skip).limit(limit).all()