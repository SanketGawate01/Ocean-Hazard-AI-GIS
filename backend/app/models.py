from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user") # 'user' or 'admin'
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    reports = relationship("Report", back_populates="reporter")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)
    status = Column(String, default="pending") # pending, verified, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Optional link to a registered user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    reporter = relationship("User", back_populates="reports")
    # uselist=False means it's a one-to-one relationship
    prediction = relationship("MLPrediction", back_populates="report", uselist=False)


class MLPrediction(Base):
    __tablename__ = "ml_predictions"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), unique=True, nullable=False)
    
    predicted_category = Column(String, nullable=False, index=True)
    confidence = Column(Float, nullable=False)
    severity = Column(String, nullable=False) # LOW, MEDIUM, HIGH, CRITICAL
    model_version = Column(String, default="v1.0")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    report = relationship("Report", back_populates="prediction")


class SocialPost(Base):
    """
    Table to store simulated social media data for dashboard analytics.
    """
    __tablename__ = "social_posts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    source = Column(String, nullable=False) # e.g., 'Twitter/X', 'Reddit'
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # ML Results baked in for simplicity in the analytics MVP
    predicted_category = Column(String, index=True)
    severity = Column(String)
    confidence = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)