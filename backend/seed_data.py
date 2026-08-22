import random
from app.database import SessionLocal, engine, Base
from app import models
from app.ml.predict import get_hazard_prediction

# Ensure tables exist
Base.metadata.create_all(bind=engine)

# Realistic sample reports
SAMPLE_REPORTS = [
    "Thick black crude oil is washing up on the sand and covering the local wildlife near the harbor.",
    "A tanker has leaked thousands of gallons of diesel into the ocean.",
    "An oil sheen has been observed near the coastline spreading rapidly.",
    "Chemical runoff from the factory is turning the water green and killing fish.",
    "Hundreds of plastic bottles and fishing nets are floating in the bay.",
    "Toxic waste detected in coastal waters near the industrial zone.",
    "Heavy rainfall caused the river to overflow and flood nearby coastal villages.",
    "Sea water has breached the sea wall and flooded the coastal streets.",
    "High tide is causing severe waterlogging in coastal homes.",
    "Extremely high waves and rough sea conditions were reported along the coastline.",
    "Large ocean swells are making navigation dangerous for fishing vessels.",
    "Ferry services have been suspended because of extremely dangerous swells.",
    "A powerful cyclone is approaching the coastal region with destructive winds.",
    "Hurricane warnings have been issued for coastal communities.",
    "A severe tropical cyclone has formed over the Arabian Sea."
]

def seed_database():
    db = SessionLocal()
    
    print("Clearing old data to prevent duplicates...")
    db.query(models.MLPrediction).delete()
    db.query(models.Report).delete()
    db.commit()

    print("Generating 50 realistic hazard reports...")
    
    for i in range(50):
        # 1. Pick a random description
        description = random.choice(SAMPLE_REPORTS)
        
        # 2. Generate random coordinates (West Coast of India / Arabian Sea)
        # Latitude roughly between Goa and Mumbai (15.0 to 20.0)
        # Longitude roughly off the coast (72.0 to 74.0)
        lat = round(random.uniform(15.0, 20.0), 4)
        lon = round(random.uniform(72.0, 74.0), 4)
        
        # 3. Create the Database Report
        db_report = models.Report(
            description=description,
            latitude=lat,
            longitude=lon,
            image_url=None
        )
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        
        # 4. Run the REAL Machine Learning Prediction
        ml_result = get_hazard_prediction(description)
        
        # 5. Save the Prediction
        db_prediction = models.MLPrediction(
            report_id=db_report.id,
            predicted_category=ml_result["predicted_category"],
            confidence=ml_result["confidence"],
            severity=ml_result["severity"]
        )
        db.add(db_prediction)
        db.commit()

    print("✅ Successfully seeded the database with 50 reports and ML predictions!")
    db.close()

if __name__ == "__main__":
    seed_database()