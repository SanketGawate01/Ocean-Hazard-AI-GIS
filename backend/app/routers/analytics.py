from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Dict

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/analytics", tags=["Analytics & GIS"])

@router.get("/summary")
def get_analytics_summary(db: Session = Depends(get_db)):
    """Returns top-level statistics for the dashboard cards."""
    total_reports = db.query(models.Report).count()
    
    # Count how many reports are labeled HIGH or CRITICAL
    high_risk = db.query(models.MLPrediction).filter(
        models.MLPrediction.severity.in_(["HIGH", "CRITICAL"])
    ).count()
    
    return {
        "total_reports": total_reports,
        "high_risk_hazards": high_risk,
        "active_monitoring": total_reports # In a full system, you'd filter by status
    }

@router.get("/categories")
def get_category_distribution(db: Session = Depends(get_db)):
    """Returns data formatted for a Chart.js Pie/Doughnut chart."""
    results = db.query(
        models.MLPrediction.predicted_category, 
        func.count(models.MLPrediction.id)
    ).group_by(models.MLPrediction.predicted_category).all()
    
    # Format the SQLAlchemy tuples into a clean list of dictionaries
    return [{"category": row[0], "count": row[1]} for row in results]

@router.get("/severity")
def get_severity_distribution(db: Session = Depends(get_db)):
    """Returns data formatted for a Chart.js Bar chart."""
    results = db.query(
        models.MLPrediction.severity, 
        func.count(models.MLPrediction.id)
    ).group_by(models.MLPrediction.severity).all()
    
    return [{"severity": row[0], "count": row[1]} for row in results]

@router.get("/map")
def get_map_markers(db: Session = Depends(get_db)):
    """Returns lightweight payload specifically optimized for Leaflet.js markers."""
    reports = db.query(models.Report).options(joinedload(models.Report.prediction)).all()
    
    markers = []
    for r in reports:
        if r.prediction:  # Only map reports that have been classified
            markers.append({
                "id": r.id,
                "latitude": r.latitude,
                "longitude": r.longitude,
                "category": r.prediction.predicted_category,
                "severity": r.prediction.severity,
                "date": r.created_at.strftime("%Y-%m-%d %H:%M")
            })
            
    return markers