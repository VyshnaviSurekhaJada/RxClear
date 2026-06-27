"""
RxClear FastAPI Backend
Endpoints: /analyze (POST), /report (POST), /medicines (GET), /history (GET)
"""
import os
import re
import uuid
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel


# ── Local modules ─────────────────────────────────────────────────────────────
import sys
sys.path.insert(0, os.path.dirname(__file__))

from ocr import extract_text_from_image, preprocess_text
from extractor import (
    extract_diagnosis, extract_medicines, extract_patient_info,
    check_interactions, validate_dosage_for_age,
)
from predictor import predict_disease
from recommendations import get_recommendations
from report_generator import generate_report

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent.parent
UPLOAD_DIR = BASE_DIR / 'uploads'
REPORT_DIR = BASE_DIR / 'reports'
DB_PATH    = BASE_DIR / 'rxclear.db'

UPLOAD_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(title='RxClear API', version='1.0.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

# ── DB init ────────────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS analyses (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            patient_name TEXT,
            medicines TEXT,
            disease TEXT,
            confidence REAL,
            raw_text TEXT,
            report_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()


# ── Helpers ────────────────────────────────────────────────────────────────────
def save_to_history(analysis_id, patient_info, medicines, disease_result, raw_text, report_path):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        INSERT OR REPLACE INTO analyses VALUES (?,?,?,?,?,?,?,?)
    ''', (
        analysis_id,
        datetime.now().isoformat(),
        patient_info.get('patient_name', ''),
        json.dumps([m['name'] for m in medicines]),
        disease_result.get('top_disease', ''),
        disease_result.get('confidence', 0),
        raw_text[:2000],
        report_path,
    ))
    conn.commit()
    conn.close()


# ── Routes ──────────────────────────────────────────────────────────────────────
@app.get('/')
def root():
    return {'status': 'ok', 'service': 'RxClear API v1.0'}


@app.post('/analyze')
async def analyze(file: UploadFile = File(...)):
    """Full pipeline: OCR → Extract → Predict → Recommend."""
    # Validate file type
    if file.content_type not in ('image/jpeg', 'image/png', 'image/jpg', 'image/webp'):
        raise HTTPException(400, 'Only JPEG and PNG images are accepted.')

    # Save upload
    analysis_id = str(uuid.uuid4())
    ext = Path(file.filename).suffix or '.jpg'
    img_path = UPLOAD_DIR / f'{analysis_id}{ext}'
    img_path.write_bytes(await file.read())

    # OCR
    raw_text = extract_text_from_image(str(img_path))
    if not raw_text:
        raise HTTPException(422, 'Could not extract text from image. Ensure the image is clear.')
    clean_text = preprocess_text(raw_text)

    clean_text = re.sub(r"[ \t]+", " ", clean_text)
    clean_text = re.sub(r"\n{3,}", "\n\n", clean_text)
    clean_text = clean_text.strip()
    OCR_FIXES = {

        "Nght": "Night",
        "Nite": "Night",

        "Moming": "Morning",
        "Mornng": "Morning",

        "Wieigt": "Weight",
        "Welght": "Weight",

        "Chiet": "Chief",

        "TAR": "TAB",
        "Tob": "Tab",
        "Tub": "Tab",

        "Cap.": "Cap",
        "Tab.": "Tab",

        "OD.": "OD",
        "BD.": "BD",
        "TDS.": "TDS",
    }

    for wrong, right in OCR_FIXES.items():
        clean_text = clean_text.replace(wrong, right)

    # Extraction
    medicines      = extract_medicines(clean_text)
    patient_info   = extract_patient_info(clean_text)
    interactions   = check_interactions(medicines)
    dosage_warns   = validate_dosage_for_age(medicines, patient_info.get('age', ''))
    diagnosis      = extract_diagnosis(clean_text)
    print("\n===== DIAGNOSIS =====")
    print(diagnosis)
    print("=====================\n")

    # Prediction
    diagnosis = extract_diagnosis(clean_text)

    patient_info["diagnosis"] = diagnosis

    if diagnosis != "Not specified":

        disease_result = {
            "top_disease": diagnosis,
            "confidence": 100,
            "predictions": []
        }

    else:

        med_names = [m["name"] for m in medicines]

        disease_result = predict_disease(med_names)

    # Diet
    top_disease = disease_result.get('top_disease')

    if not top_disease:
        top_disease = "general"

    diet = get_recommendations(top_disease)
    # Generate PDF
    report_path = str(REPORT_DIR / f'report_{analysis_id}.pdf')
    generate_report(
        patient_info=patient_info,
        medicines=medicines,
        disease_result=disease_result,
        diet=diet,
        interactions=interactions,
        dosage_warnings=dosage_warns,
        raw_text=clean_text,
        output_path=report_path,
    )

    # Save to history
    save_to_history(analysis_id, patient_info, medicines, disease_result, clean_text, report_path)

    return {
        'analysis_id': analysis_id,
        'raw_text': clean_text,
        'patient_info': patient_info,
        'medicines': medicines,
        'disease_prediction': disease_result,
        'diet_recommendations': diet,
        'interaction_warnings': interactions,
        'dosage_warnings': dosage_warns,
        'report_url': f'/report/{analysis_id}',
    }


@app.get('/report/{analysis_id}')
def download_report(analysis_id: str):
    """Download PDF report for a given analysis ID."""
    report_path = REPORT_DIR / f'report_{analysis_id}.pdf'
    if not report_path.exists():
        raise HTTPException(404, 'Report not found.')
    return FileResponse(
        str(report_path),
        media_type='application/pdf',
        filename=f'RxClear_Report_{analysis_id[:8]}.pdf'
    )


@app.get('/medicines')
def search_medicines(q: str = Query('', min_length=1)):
    """Search medicine database by name."""
    import pandas as pd
    db_path = BASE_DIR / 'datasets' / 'medicines.csv'
    df = pd.read_csv(db_path)
    mask = (
        df['name'].str.lower().str.contains(q.lower(), na=False) |
        df['generic_name'].str.lower().str.contains(q.lower(), na=False)
    )
    results = df[mask].to_dict(orient='records')
    return {'results': results, 'count': len(results)}


@app.get('/history')
def get_history(limit: int = 20):
    """Return recent analysis history."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        'SELECT id, timestamp, patient_name, medicines, disease, confidence FROM analyses ORDER BY timestamp DESC LIMIT ?',
        (limit,)
    ).fetchall()
    conn.close()
    history = [
        {
            'id': r[0],
            'timestamp': r[1],
            'patient_name': r[2],
            'medicines': json.loads(r[3]) if r[3] else [],
            'disease': r[4],
            'confidence': r[5],
        }
        for r in rows
    ]
    return {'history': history}


@app.delete('/history/{analysis_id}')
def delete_history_item(analysis_id: str):
    """Delete a single history record."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute('DELETE FROM analyses WHERE id = ?', (analysis_id,))
    conn.commit()
    conn.close()
    return {'deleted': analysis_id}
