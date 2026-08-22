# 🌊 Ocean Hazard AI-GIS

An AI-powered GIS platform for **crowdsourced ocean hazard reporting, NLP-based hazard classification, severity assessment, spatial visualization, and social analytics**.

## 🚀 Features

* 🤖 AI-based ocean hazard classification
* 📝 Crowdsourced hazard reporting
* 🧠 NLP-based text classification
* 📊 TF-IDF + Linear SVM machine learning model
* ⚠️ Automatic severity assessment
* 🗺️ Interactive GIS hazard map
* 📍 Latitude/Longitude-based incident visualization
* 📈 Hazard distribution analytics
* 📊 Severity analysis
* 🐘 PostgreSQL database integration
* 📥 CSV data export
* 🌐 Web-based dashboard

---

## 🧠 Hazard Categories

The system classifies hazard reports into four categories:

| Category                      | Examples                                              |
| ----------------------------- | ----------------------------------------------------- |
| 🌧️ **Flooding**              | Heavy rainfall, overflowing rivers, submerged streets |
| 🌊 **High Waves / Rough Sea** | Large swells, dangerous waves, rough seas             |
| 🛢️ **Marine Pollution**      | Oil spills, diesel leaks, fuel discharge              |
| 🌀 **Storm / Cyclone**        | Cyclones, hurricanes, typhoons, severe storms         |

---

## 🤖 Machine Learning

The NLP classification pipeline uses:

* **Word-level TF-IDF**
* **Character-level TF-IDF**
* **FeatureUnion**
* **LinearSVC**
* Balanced class weights
* Word and character n-grams

### Model Pipeline

```text
Hazard Description
        ↓
Text Input
        ↓
 ┌───────────────────┐
 │ Word TF-IDF       │
 │ Character TF-IDF  │
 └───────────────────┘
        ↓
    FeatureUnion
        ↓
      LinearSVC
        ↓
 Hazard Classification
```

### Model Performance

The trained model achieved approximately:

**99.89% accuracy**

Evaluation was performed on a held-out test dataset containing **1,827 samples**.

The model achieved approximately **1.00 precision, recall, and F1-score** across the four hazard classes on the evaluation dataset.

Additional unseen-text testing was performed to validate predictions on new hazard descriptions.

---

## 🗺️ GIS Hazard Map

The platform provides an interactive GIS map for visualizing reported hazards geographically.

Each report can contain:

* Latitude
* Longitude
* Hazard category
* Severity
* Incident information

This allows users to understand the **spatial distribution of ocean and coastal hazards**.

---

## 📊 Analytics Dashboard

The analytics dashboard provides aggregated statistics from the PostgreSQL database.

### Available analytics

* Total reports
* High-risk incidents
* System status
* Hazard distribution
* Severity breakdown
* AI-classified incidents
* CSV data export

---

## 🏗️ System Architecture

```text
                    USER
                     │
                     ▼
              Web Application
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
  Report Hazard   GIS Map    Analytics
        │
        ▼
   FastAPI Backend
        │
        ▼
    NLP / ML Model
        │
        ├── Word TF-IDF
        ├── Character TF-IDF
        ├── FeatureUnion
        └── LinearSVC
        │
        ▼
 Hazard Classification
        │
        ▼
 Severity Assessment
        │
        ▼
 PostgreSQL Database
        │
        ▼
 Analytics & Visualization
```

---

## 🛠️ Technologies Used

### Machine Learning / AI

* Python
* Scikit-learn
* TF-IDF
* LinearSVC
* NLP
* FeatureUnion
* Joblib

### Backend

* FastAPI
* Python
* Pydantic
* SQLAlchemy

### Database

* PostgreSQL

### Frontend

* HTML
* CSS
* JavaScript
* Leaflet.js

### Data & Visualization

* Pandas
* NumPy
* CSV
* Interactive GIS visualization
* Analytics charts

---

## 📁 Project Structure

```text
Ocean-Hazard-AI-GIS/
│
├── backend/
│   ├── app/
│   │   ├── ml/
│   │   │   ├── train.py
│   │   │   ├── predict.py
│   │   │   └── ocean_hazard_lr_model.pkl
│   │   │
│   │   ├── routers/
│   │   │   ├── analytics.py
│   │   │   └── reports.py
│   │   │
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── main.py
│   │
│   └── seed_data.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Ocean-Hazard-AI-GIS.git
cd Ocean-Hazard-AI-GIS
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ PostgreSQL Setup

Create a PostgreSQL database and configure the database connection used by the backend.

Example:

```text
DATABASE_URL=postgresql://username:password@localhost:5432/ocean_hazard
```

Keep database credentials in environment variables and **never commit `.env` files to GitHub**.

---

## ▶️ Run the Application

Start the FastAPI backend:

```bash
uvicorn backend.app.main:app --reload
```

Then open the frontend application in your browser.

---

## 🧪 Example Predictions

### Marine Pollution

**Input:**

```text
A tanker is leaking diesel into coastal waters.
```

**Prediction:**

```text
Marine Pollution
```

### Storm / Cyclone

**Input:**

```text
A tropical cyclone is approaching the coastline.
```

**Prediction:**

```text
Storm / Cyclone
```

### Flooding

**Input:**

```text
Several streets are completely submerged after continuous rainfall.
```

**Prediction:**

```text
Flooding
```

### High Waves / Rough Sea

**Input:**

```text
Large ocean swells are making navigation dangerous.
```

**Prediction:**

```text
High Waves / Rough Sea
```

---

## 🔄 Application Workflow

```text
1. User submits hazard description
              ↓
2. AI analyzes the text
              ↓
3. Hazard category is predicted
              ↓
4. Severity is assessed
              ↓
5. Report is stored in PostgreSQL
              ↓
6. Location appears on GIS map
              ↓
7. Analytics are updated
```

---

## 📈 Project Results

The system was tested using both:

* Held-out test data
* Unseen manually written hazard descriptions

The final NLP model demonstrated high classification performance across:

* Flooding
* High Waves / Rough Sea
* Marine Pollution
* Storm / Cyclone

The platform successfully integrates the ML model with a **FastAPI backend, PostgreSQL database, web interface, GIS visualization, and analytics dashboard**.

---

## 🔮 Future Improvements

* Real-time social media hazard monitoring
* Satellite imagery integration
* Real-time weather and ocean data
* Advanced deep-learning NLP models
* Automated emergency notifications
* Multi-language hazard reporting
* Real-time ocean-condition APIs
* Advanced geospatial analysis

---

## 👨‍💻 Project Information

**Project:** Ocean Hazard AI-GIS

**Domain:** Artificial Intelligence + Machine Learning + NLP + GIS

**Purpose:** Educational / Academic Project

### Key Concepts Demonstrated

```text
Artificial Intelligence
Machine Learning
Natural Language Processing
Text Classification
GIS
REST API
Database Management
Data Analytics
Web Development
```

---

## 📄 License

This project is developed for **educational and academic purposes**.
