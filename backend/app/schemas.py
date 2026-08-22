from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# --------------------------------------------------
# ENUMS FOR STRICT VALIDATION
# --------------------------------------------------
class HazardCategory(str, Enum):
    oil_spill = "Oil Spill"
    marine_pollution = "Marine Pollution"
    coastal_flooding = "Coastal Flooding"
    high_waves = "High Waves / Rough Sea"
    storm = "Storm / Cyclone"

class SeverityLevel(str, Enum):
    low = "LOW"
    medium = "MEDIUM"
    high = "HIGH"
    critical = "CRITICAL"

# --------------------------------------------------
# PREDICTION SCHEMAS
# --------------------------------------------------
class MLPredictionBase(BaseModel):
    predicted_category: HazardCategory
    confidence: float = Field(..., ge=0.0, le=1.0) # Must be between 0 and 1
    severity: SeverityLevel

class MLPredictionOut(MLPredictionBase):
    id: int
    created_at: datetime
    
    # Allows Pydantic to parse SQLAlchemy objects directly
    model_config = ConfigDict(from_attributes=True) 

# --------------------------------------------------
# REPORT SCHEMAS
# --------------------------------------------------
class ReportCreate(BaseModel):
    """Schema for incoming data from the frontend form"""
    description: str = Field(..., min_length=10, description="Detailed text of the incident")
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    image_url: Optional[str] = None
    
class ReportOut(BaseModel):
    """Schema for data being sent back to the frontend"""
    id: int
    description: str
    latitude: float
    longitude: float
    image_url: Optional[str]
    status: str
    created_at: datetime
    
    # Nested prediction data (will be populated automatically if relationship exists)
    prediction: Optional[MLPredictionOut] = None

    model_config = ConfigDict(from_attributes=True)

# --------------------------------------------------
# ANALYTICS / SOCIAL SCHEMAS
# --------------------------------------------------
class SocialPostOut(BaseModel):
    id: int
    text: str
    source: str
    latitude: Optional[float]
    longitude: Optional[float]
    predicted_category: Optional[str]
    severity: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)