"""
NLP extraction module: parses prescription text into structured fields.
Uses regex + a known-medicine lookup against medicines.csv.
"""
from multiprocessing import context
import re
import os
from distro import info
from matplotlib import text
import pandas as pd
from typing import Optional
from medicine_matcher import (
    fuzzy_match_medicine,
    get_medicine_info
)
from patient_parser import (
    extract_name,
    extract_age,
    extract_gender,
    extract_date,
    extract_prescriber,
    extract_registration
)
STOP_WORDS = {
    "patient", "doctor", "hospital", "clinic", "medical",
    "medicine", "tablet", "tab", "capsule", "cap",
    "diagnosis", "findings", "complaints", "chief",
    "weight", "height", "blood", "pressure",
    "morning", "afternoon", "evening", "night",
    "days", "food", "fever", "headache",
    "follow", "review", "date", "address",
    "male", "female", "years", "year"
}
# ── Load medicine database ────────────────────────────────────────────────────
_DB_PATH = os.path.join(os.path.dirname(__file__), '../datasets/medicines.csv')
_medicine_df: Optional[pd.DataFrame] = None

def _get_medicine_db() -> pd.DataFrame:
    global _medicine_df
    if _medicine_df is None:
        _medicine_df = pd.read_csv(_DB_PATH).fillna('')
        _medicine_df['name_lower'] = _medicine_df['name'].str.lower()
        _medicine_df['generic_lower'] = _medicine_df['generic_name'].str.lower()
    return _medicine_df


# ── Normalisation helpers ─────────────────────────────────────────────────────
FREQUENCY_MAP = {
    r'\b1[-\s]?0[-\s]?1\b': 'Twice Daily (Morning & Night)',
    r'\b1[-\s]?1[-\s]?1\b': 'Three Times Daily',
    r'\b1[-\s]?0[-\s]?0\b': 'Once Daily (Morning)',
    r'\b0[-\s]?0[-\s]?1\b': 'Once Daily (Night)',
    r'\b0[-\s]?1[-\s]?0\b': 'Once Daily (Afternoon)',
    r'\b1[-\s]?1[-\s]?0\b': 'Twice Daily (Morning & Afternoon)',
    r'\bonce\s+daily\b': 'Once Daily',
    r'\bonce\s+a\s+day\b': 'Once Daily',
    r'\btwice\s+daily\b': 'Twice Daily',
    r'\btwice\s+a\s+day\b': 'Twice Daily',
    r'\bthrice\s+daily\b': 'Three Times Daily',
    r'\bthree\s+times\s+a?\s*day\b': 'Three Times Daily',
    r'\bbd\b': 'Twice Daily',
    r'\btds\b': 'Three Times Daily',
    r'\bqid\b': 'Four Times Daily',
    r'\bod\b': 'Once Daily',
    r'\bhs\b': 'At Bedtime',
    r'\bprn\b': 'As Needed',
    r'\bq\s*(\d+)\s*h(rs?)?\b': lambda m: f'Every {m.group(1)} Hours',
    # Morning / Night patterns
    r'\b1\s*morning\b': 'Once Daily (Morning)',
    r'\b1\s*night\b': 'Once Daily (Night)',
    r'\b1\s*afternoon\b': 'Once Daily (Afternoon)',
    r'\b1\s*evening\b': 'Once Daily (Evening)',

    r'\b1\s*morning\s*,?\s*1\s*night\b': 'Twice Daily',
    r'\bmorning\s*and\s*night\b': 'Twice Daily',
    r'\bmorning\s*&\s*night\b': 'Twice Daily',

    r'\bsos\b': 'As Needed',
    r'\bstat\b': 'Immediately',
}

TIMING_PATTERNS = [
    (r'\bmorning\s*,?\s*1\s*night\b', 'Morning, Night'),
    (r'\bmorning\s*&\s*night\b', 'Morning, Night'),
    (r'\bmorning\s*and\s*night\b', 'Morning, Night'),

    (r'\b1\s*morning\b', 'Morning'),
    (r'\b1\s*night\b', 'Night'),
    (r'\b1\s*afternoon\b', 'Afternoon'),
    (r'\b1\s*evening\b', 'Evening'),

    (r'\bwith\s+food\b', 'With Food'),
    (r'\bafter\s+food\b', 'After Food'),
    (r'\bafter\s+meals?\b', 'After Food'),
    (r'\bbefore\s+food\b', 'Before Food'),
    (r'\bbefore\s+meals?\b', 'Before Food'),

    (r'\bon\s+empty\s+stomach\b', 'Empty Stomach'),
    (r'\bat\s+bedtime\b', 'At Bedtime'),

    (r'\bmorning\b', 'Morning'),
    (r'\bafternoon\b', 'Afternoon'),
    (r'\bevening\b', 'Evening'),
    (r'\bnight\b', 'Night'),
]

DURATION_PATTERN = re.compile(
    r'(?:for\s+)?(\d+)\s*(day|days|week|weeks|month|months)', re.IGNORECASE
)
DOSAGE_PATTERN = re.compile(
    r'(\d+(?:\.\d+)?)\s*(mg|mcg|ml|g|iu|units?|%)', re.IGNORECASE
)

# Common prescription prefixes to strip
MED_PREFIXES = r'(?:tab(?:let)?|cap(?:sule)?|inj(?:ection)?|syp|syrup|drops?|cream|oint(?:ment)?|gel|spray)\s+'


def _clean_med_name(raw: str) -> str:
    name = re.sub(MED_PREFIXES, '', raw, flags=re.IGNORECASE).strip()
    name = re.sub(r'\s+\d.*', '', name)       # strip trailing dose
    name = re.sub(r'[^a-zA-Z0-9\s\-]', '', name).strip()
    return name.title()


def extract_medicines(text: str) -> list[dict]:
    """Return list of medicine dicts extracted from prescription text."""
    lines = text.split('\n')
    
    medicines = []
    seen = set()


    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        # Try to match a medicine name against the DB first
        matched_db = None

        # Fall back to regex for "Tab/Cap <Name>" patterns
        regex_names = re.findall(
            r'(?:tab(?:let)?|cap(?:sule)?|inj(?:ection)?|syr(?:up)?|syp|drops?|cream|ointment|oint|gel|spray|neb|respule|susp(?:ension)?|tar)[\.,]?\s+([A-Za-z][A-Za-z0-9\-/ ]{1,40})',
            line,
            re.IGNORECASE
        )

        candidates = []
        if matched_db is not None:
            candidates.append(matched_db['name'])
        for rn in regex_names:
            candidates.append(_clean_med_name(rn))
        words = re.findall(
            r'[A-Za-z][A-Za-z0-9\-]{2,}',
            line
        )

        for word in words:

            word = word.strip()

            # Ignore short words
            if len(word) < 5:
                continue

            # Ignore common non-medicine words
            if word.lower() in STOP_WORDS:
                continue

            matched = fuzzy_match_medicine(word)

            if matched:
                candidates.append(matched)
        candidates = list({
            c.lower(): c
            for c in candidates
        }.values())
        for med_name in candidates:
            # Brand → Generic mapping
            matched_name = fuzzy_match_medicine(med_name)

            print(
                f"Original: {med_name} -> Matched: {matched_name}"
            )

            if matched_name:
                med_name = matched_name

            key = med_name.lower()
            if key in seen or not med_name or len(med_name) < 3:
                continue
            seen.add(key)

            # Build context using nearby lines
            context_lines = [line]

            for j in range(i + 1, len(lines)):

                next_line = lines[j].strip()

                if not next_line:
                    continue

                # Stop when another medicine begins
                if re.search(
                    r'^(?:\d+\)|\d+\.)?\s*(?:tab(?:let)?|cap(?:sule)?|inj(?:ection)?|syr(?:up)?|drops?|cream|ointment|gel|spray|respule|neb|susp(?:ension)?)\b',
                    next_line,
                    re.IGNORECASE
                ):
                    break

                context_lines.append(next_line)

            context = " ".join(context_lines)

            # Extract frequency, timing and duration
            frequency = _extract_frequency(context)
            duration = _extract_duration(context)

            # Get medicine information from database
            db_info = get_medicine_info(med_name)

            db_info = {
                k: ("" if pd.isna(v) else v)
                for k, v in db_info.items()
            }

            # Extract dosage
            dosage_match = re.search(
                r'(\d+/\w+|\d+\s*mg\b|\d+\s*mcg\b|\d+\s*ml\b|\d+\s*g\b)',
                line,
                re.IGNORECASE
            )

            dosage = (
                dosage_match.group(1)
                if dosage_match
                else "Not specified"
            )
                    

            frequency_lower = frequency.lower()

            if "morning" in frequency_lower and "night" in frequency_lower:
                frequency = "Twice Daily"

            elif "morning" in frequency_lower:
                frequency = "Once Daily"

            elif "night" in frequency_lower:
                frequency = "Once Daily"

            elif "afternoon" in frequency_lower:
                frequency = "Once Daily"

            elif "evening" in frequency_lower:
                frequency = "Once Daily"
            
            timing = _extract_timing(context)

            if timing == "As directed":
                timing = "Not specified" 

            medicines.append({
                'name': med_name,
                'generic_name': db_info.get('generic_name', ''),
                'category': db_info.get('category', ''),
                'dosage': dosage,
                'frequency': frequency,
                'timing': timing,
                'duration': duration,
                'uses': db_info.get('uses', ''),
                'side_effects': db_info.get('side_effects', ''),
                'interactions': db_info.get('interactions', ''),
                'max_adult_dose': db_info.get('max_adult_dose', ''),
                'max_child_dose': db_info.get('max_child_dose', ''),
                'contraindications': db_info.get('contraindications', ''),
            })

            print("\n===== MEDICINES =====")

            for med in medicines:
                print(med)

            print("=====================\n")
    return medicines


def _extract_frequency(text: str) -> str:
    text_lower = text.lower()
    for pattern, label in FREQUENCY_MAP.items():
        m = re.search(pattern, text_lower, re.IGNORECASE)
        if m:
            return label(m) if callable(label) else label
    return 'As directed'

def _extract_timing(text: str) -> str:
    text_lower = text.lower()
    for pattern, label in TIMING_PATTERNS:
        if re.search(pattern, text_lower):
            return label
    return 'As directed'


def _extract_duration(text: str) -> str:

    m = DURATION_PATTERN.search(text)

    if m:
        value = int(m.group(1))
        unit = m.group(2).lower()

        if value > 1 and unit == "day":
            unit = "days"

        return f"{value} {unit}"

    # Handle OCR like:
    # 1-1-1 3 After Meal

    m = re.search(
        r'(\d+)\s+(?:After|Before)',
        text,
        re.IGNORECASE
    )

    if m:
        return f"{m.group(1)} days"

    return "Not specified"

def extract_diagnosis(text):

    labels = [
        "Diagnosis",
        "Dx",
        "Clinical Diagnosis",
        "Assessment",
        "Impression",
        "Provisional Diagnosis",
        "Final Diagnosis",
        "Primary Diagnosis"
    ]

    STOP_WORDS = {
        "rx",
        "medicine",
        "medicines",
        "treatment",
        "advice",
        "follow up",
        "follow-up",
        "prescription",
        "investigation",
        "investigations",
        "plan"
    }

    lines = text.splitlines()

    for i, line in enumerate(lines):

        line = line.strip()

        # ---------- Case 1 ----------
        # Diagnosis: Dengue

        for label in labels:

            pattern = rf'^{re.escape(label)}\s*:?\s*(.+)$'

            match = re.match(pattern, line, re.IGNORECASE)

            if match:

                value = match.group(1).strip()

                value = re.sub(r'^[*:\-\s]+', '', value)
                value = re.sub(r'\s+', ' ', value)

                if value and value.lower() not in STOP_WORDS:
                    return value.upper()

        # ---------- Case 2 ----------
        # Diagnosis:
        # Dengue

        for label in labels:

            if re.match(
                rf'^{re.escape(label)}\s*:?\s*$',
                line,
                re.IGNORECASE
            ):

                for j in range(i + 1, min(i + 6, len(lines))):

                    value = lines[j].strip()

                    value = re.sub(r'^[*:\-\s]+', '', value)
                    value = re.sub(r'\s+', ' ', value)

                    if not value:
                        continue

                    if value.lower() in STOP_WORDS:
                        continue

                    # Skip separator lines like -----
                    if re.fullmatch(r'[-=*]+', value):
                        continue

                    # Skip obvious section headers
                    if value.endswith(":"):
                        continue

                    return value.upper()

    return "Not specified"


def extract_patient_info(text: str) -> dict:
    """Try to extract patient name, age, date, prescriber from text."""
    info = {}

    info["patient_name"] = extract_name(text)

    info["registration_no"] = extract_registration(text)

    info["age"] = extract_age(text)

    info["gender"] = extract_gender(text)

    info["date"] = extract_date(text)

    info["prescriber"] = extract_prescriber(text)

    info["diagnosis"] = extract_diagnosis(text)

    #followup date
    follow_patterns = [
        r'follow\s*up\s*:\s*(.+)',
        r'next follow-up date\s*:\s*(.+)',
        r'follow-up date\s*:\s*(.+)'
    ]

    for pattern in follow_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            follow = match.group(1).strip()
            follow = follow.strip(" ,.;:")
            info["follow_up"] = follow
            break
    # Refills
    refill_m = re.search(r'refills?[:\s]*(\d+)', text, re.IGNORECASE)
    info['refills'] = refill_m.group(1) if refill_m else '0'

    return info

def check_interactions(medicines: list[dict]) -> list[dict]:
    """Flag known dangerous drug-drug or drug-substance interactions."""
    KNOWN_INTERACTIONS = [
        (['paracetamol', 'acetaminophen'], 'alcohol', '⚠️ Paracetamol + Alcohol may cause severe liver damage.', 'HIGH'),
        (['warfarin'], 'aspirin', '⚠️ Warfarin + Aspirin significantly increases bleeding risk.', 'HIGH'),
        (['metformin'], 'alcohol', '⚠️ Metformin + Alcohol may cause lactic acidosis.', 'HIGH'),
        (['tramadol'], ['ssri', 'sertraline', 'fluoxetine'], '⚠️ Tramadol + SSRIs may cause Serotonin Syndrome.', 'HIGH'),
        (['ciprofloxacin', 'doxycycline', 'azithromycin'], 'antacids', '⚠️ Antacids reduce antibiotic absorption. Take 2 hours apart.', 'MEDIUM'),
        (['ibuprofen', 'diclofenac'], ['lisinopril', 'amlodipine'], '⚠️ NSAIDs may reduce antihypertensive effectiveness.', 'MEDIUM'),
        (['ibuprofen', 'diclofenac'], ['warfarin'], '⚠️ NSAIDs + Blood thinners increase bleeding risk.', 'HIGH'),
        (['levothyroxine'], ['calcium', 'iron', 'antacid'], '⚠️ Calcium/Iron reduces levothyroxine absorption. Take on empty stomach.', 'MEDIUM'),
        (['sertraline', 'fluoxetine'], ['tramadol', 'linezolid'], '⚠️ SSRIs + MAOIs/Tramadol risk Serotonin Syndrome.', 'HIGH'),
        (['metronidazole'], 'alcohol', '⚠️ Metronidazole + Alcohol causes severe nausea/flushing (disulfiram reaction).', 'HIGH'),
    ]

    med_names_lower = [m['name'].lower() for m in medicines]
    warnings = []

    for trigger_meds, interacting, message, severity in KNOWN_INTERACTIONS:
        triggers_present = any(
            any(t in mn for mn in med_names_lower) for t in (trigger_meds if isinstance(trigger_meds, list) else [trigger_meds])
        )
        if not triggers_present:
            continue
        interacting_list = interacting if isinstance(interacting, list) else [interacting]
        interacts_present = any(
            any(i in mn for mn in med_names_lower) for i in interacting_list
        )
        if triggers_present and (interacts_present or any(i in ' '.join(med_names_lower) for i in interacting_list)):
            warnings.append({'message': message, 'severity': severity})

    # Multi-medicine interaction check
    if len(med_names_lower) >= 3:
        warnings.append({
            'message': 'ℹ️ Multiple medications detected. Consult your pharmacist about potential interactions.',
            'severity': 'INFO'
        })

    return warnings


def validate_dosage_for_age(medicines: list[dict], age: str) -> list[dict]:
    """Flag if dosage may be unsafe for the patient's age."""
    warnings = []
    try:
        age_val = int(age)
    except (ValueError, TypeError):
        return warnings

    for med in medicines:
        if age_val < 18:
            max_child = med.get('max_child_dose', 'N/A')
            if max_child == 'N/A':
                warnings.append({
                    'message': f"⚠️ {med['name']} – no established pediatric dose. Use with caution in children.",
                    'severity': 'HIGH'
                })
            # Parse dosage and compare
            dosage_m = re.search(r'(\d+(?:\.\d+)?)', med.get('dosage', ''))
            if dosage_m:
                dose_val = float(dosage_m.group(1))
                child_m = re.search(r'(\d+(?:\.\d+)?)', str(max_child))
                if child_m and dose_val > float(child_m.group(1)) * age_val:
                    warnings.append({
                        'message': f"⚠️ {med['name']} {med['dosage']} may exceed recommended pediatric dose.",
                        'severity': 'HIGH'
                    })

        if age_val >= 65:
            if med.get('name', '').lower() in ['tramadol', 'diazepam', 'amitriptyline']:
                warnings.append({
                    'message': f"⚠️ {med['name']} requires extra caution in elderly patients (Beers Criteria).",
                    'severity': 'MEDIUM'
                })

    return warnings
