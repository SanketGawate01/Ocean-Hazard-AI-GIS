# 🌊 Ocean Hazard AI-GIS

An AI-powered GIS platform for **crowdsourced ocean hazard reporting, NLP-based hazard classification, severity assessment, spatial visualization, and social analytics**.

The system allows users to submit coastal hazard descriptions along with geographic coordinates. The NLP model automatically classifies the reported hazard and the platform visualizes incidents on an interactive GIS map.

---

## 🚀 Features

- 🤖 AI-based ocean hazard classification
- 📝 Crowdsourced hazard reporting
- 🧠 NLP text classification using TF-IDF
- 📊 Machine Learning classification using Linear SVM
- ⚠️ Automatic severity assessment
- 🗺️ Interactive GIS hazard map
- 📍 Latitude and longitude based incident visualization
- 📈 Hazard distribution analytics
- 📊 Severity breakdown and statistics
- 🐘 PostgreSQL database integration
- 📥 Download reports as CSV
- 🌐 Web-based dashboard

---

## 🧠 Hazard Categories

The NLP model classifies reports into four major categories:

| Hazard | Description |
|---|---|
| 🌧️ Flooding | Flooding, heavy rainfall, overflowing rivers, submerged areas |
| 🌊 High Waves / Rough Sea | Large swells, dangerous waves, rough seas and unsafe navigation |
| 🛢️ Marine Pollution | Oil spills, fuel leaks, diesel discharge and marine contamination |
| 🌀 Storm / Cyclone | Tropical cyclones, hurricanes, typhoons and severe storms |

---

## 🤖 Machine Learning Model

The project uses a text classification pipeline based on:

- **TF-IDF Vectorization**
- Word-level TF-IDF features
- Character-level TF-IDF features
- **FeatureUnion**
- **Linear Support Vector Machine (LinearSVC)**
- Balanced class weights

The model combines word and character-level features to improve classification of different types of hazard descriptions.

### Model Pipeline

```text
Input Hazard Description
          ↓
     Text Processing
          ↓
 ┌─────────────────────┐
 │ Word-level TF-IDF   │
 │ Character TF-IDF    │
 └─────────────────────┘
          ↓
     FeatureUnion
          ↓
       LinearSVC
          ↓
   Hazard Prediction
