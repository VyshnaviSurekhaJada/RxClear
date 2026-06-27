# RxClear – AI-Powered Medical Prescription Analyzer

> Upload a prescription image and receive structured medicine extraction, disease prediction, diet guidance, interaction warnings, and a downloadable PDF report.

---
#LIVE DEMO

Frontend : https://rx-clear-delta.vercel.app/

Backend :

## Project Structure

```
RxClear/
├── .gitignore
├── backend/
│   ├── extractor.py
│   ├── main.py
│   ├── medicine_mapping.py
│   ├── medicine_matcher.py
│   ├── ocr.py
│   ├── patient_parser.py
│   ├── predictor.py
│   ├── recommendations.py
│   └── report_generator.py
├── datasets/
│   ├── disease_training.csv
│   ├── medicines.csv
│   └── medicine_aliases.csv
├── frontend/
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   └── Navbar.jsx
│   │   ├── index.css
│   │   ├── main.jsx
│   │   └── pages/
│   │       ├── Analyze.jsx
│   │       ├── History.jsx
│   │       ├── Home.jsx
│   │       └── MedicineSearch.jsx
│   └── vite.config.js
├── models/
│   ├── disease_model.pkl
│   └── train_model.py
├── reports/                     # Generated PDF reports
├── requirements.txt
├── rxclear.db                   # SQLite history database
├── start.sh                     # Quick startup script
└── uploads/                     # Uploaded prescription images
```

---

## Quick Start

### 1. Install backend dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Install frontend dependencies

```bash
cd frontend
npm install
```

### 3. Train the disease model

```bash
python models/train_model.py
```

### 4. Start the application

#### Option A: One-command launcher (Bash / WSL)

```bash
bash start.sh
```

#### Option B: Run separately

```bash
cd backend
uvicorn main:app --reload --port 8000
```

```bash
cd frontend
npm run dev
```

Open **http://localhost:3000**

---

## API Endpoints

| Method | Path                     | Description                              |
|--------|--------------------------|------------------------------------------|
| POST   | `/analyze`               | Upload prescription image and analyze it |
| GET    | `/report/{analysis_id}`  | Download the generated PDF report        |
| GET    | `/medicines?q=<query>`   | Search medicine database                 |
| GET    | `/history`               | List recent analyses                     |
| DELETE | `/history/{analysis_id}` | Delete a history record                  |
| GET    | `/docs`                  | FastAPI Swagger UI                       |

---

## Features

### OCR Extraction
- Extracts text from prescription images using EasyOCR
- Includes fallback support for Tesseract-style text cleaning
- Normalizes whitespace and fixes common OCR errors

### Medicine Extraction
- Finds medicine names from text using regex and the medicine database
- Extracts dosage, frequency, timing, and duration
- Normalizes common prescription abbreviations

### Disease Prediction
- Uses TF-IDF on extracted medication names
- Predicts likely disease categories with a Random Forest model
- Falls back to extracted diagnosis text when available

### Diet & Lifestyle Recommendations
- Provides condition-aware guidance for diet and lifestyle
- Covers common conditions with eat/avoid/lifestyle advice

### PDF Report Generation
- Creates a downloadable professional report via ReportLab
- Includes patient info, medicines, diagnosis, diet, warnings, and summary

### Advanced Behavior
- Drug interaction warnings with severity levels
- Age-based dosage validation and warnings
- Medicine database search and history tracking

---

## Technology Stack

| Layer     | Technology                                |
|-----------|-------------------------------------------|
| Frontend  | React 18, Vite, React Router, Recharts    |
| Backend   | FastAPI, Uvicorn, Pydantic                |
| OCR       | EasyOCR (primary), Tesseract-style fallback |
| ML        | scikit-learn (TF-IDF + Random Forest)     |
| PDF       | ReportLab                                 |
| Database  | SQLite                                    |

---

## Project Highlights

- Full-stack AI workflow: OCR → NLP extraction → prediction → recommendation
- Clinical-aware extraction of medicines, dosage, and interactions
- Downloadable PDF report generation with patient and prescription summaries
- Searchable medicine knowledge base and persistent analysis history
