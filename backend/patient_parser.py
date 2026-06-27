import re

def extract_name(text):

    NAME_PATTERNS = [
        r'Patient\s*:\s*([A-Za-z ]+)',
        r'Patient Name\s*:\s*([A-Za-z ]+)',
        r'Name\s*:\s*([A-Za-z ]+)',
        r'Pt Name\s*:\s*([A-Za-z ]+)'
    ]

    for pattern in NAME_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:

            name = match.group(1).strip()

            # Remove titles
            name = re.sub(
                r'\b(Mr|Mrs|Ms|Miss)\.?\b',
                '',
                name,
                flags=re.IGNORECASE
            )

            # Remove extra spaces
            name = re.sub(r'\s+', ' ', name).strip()

            return name

        # ---------- Fallback ----------
    lines = text.splitlines()

    IGNORE = [
        "hospital",
        "clinic",
        "doctor",
        "date",
        "reg",
        "phone",
        "diagnosis",
        "prescription",
        "male",
        "female",
        "years"
    ]

    for line in lines[:12]:

        value = line.strip()

        if len(value.split()) < 2:
            continue

        if any(word in value.lower() for word in IGNORE):
            continue

        if re.fullmatch(r"[A-Za-z .]+", value):
            return value

    return "Not specified"

def extract_age(text):

    age = "Not specified"

    age_m = re.search(
        r'(\d{1,3})\s*years?',
        text,
        re.IGNORECASE
    )

    if age_m:
        age = age_m.group(1)

    if age == "Not specified":

        age_m = re.search(
            r'/\s*(\d{1,3})',
            text
        )

        if age_m:
            age = age_m.group(1)

    return age

def extract_gender(text):

    gender = "Not specified"

    gender_m = re.search(
        r'(Male|Female)',
        text,
        re.IGNORECASE
    )

    if gender_m:
        gender = gender_m.group(1).title()

    if gender == "Not specified":

        gender_m = re.search(
            r'\((M|F)\)',
            text,
            re.IGNORECASE
        )

        if gender_m:

            gender = (
                "Male"
                if gender_m.group(1).upper() == "M"
                else "Female"
            )

    return gender

def extract_date(text):

    patterns = [

        r'date\s*:\s*(\d{2}-\d{2}-\d{4})',

        r'date\s*:\s*(\d{2}/\d{2}/\d{4})',

        r'date\s*:\s*([A-Za-z0-9\- ]+)'

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    return "Not specified"

def extract_prescriber(text):

    patterns = [

        r'Dr\.?\s*([A-Za-z ]+)',

        r'Doctor\s*:?\s*([A-Za-z ]+)',

        r'Consultant\s*:?\s*([A-Za-z ]+)',

        r'Physician\s*:?\s*([A-Za-z ]+)',

        r'([A-Za-z ]+?)\s+(?:MBBS|MD|MS|MDS|DNB|DM)'
    ]

    STOP_WORDS = [
        "Hospital",
        "Clinic",
        "Medical",
        "Centre",
        "Center",
        "Nursing",
        "Reg",
        "Date",
        "Phone",
        "Ph",
        "MBBS",
        "MD",
        "MS",
        "MDS",
        "DNB",
        "DM"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            doctor = match.group(1).strip()

            for stop in STOP_WORDS:

                doctor = re.split(
                    rf"\b{re.escape(stop)}\b",
                    doctor,
                    flags=re.IGNORECASE
                )[0].strip()

            doctor = re.sub(
                r'\s+',
                ' ',
                doctor
            )

            if doctor:

                return "Dr. " + doctor

    return "Not specified"

def extract_registration(text):

    reg = re.search(
        r'(?:Reg(?:istration)?\s*No\.?)\s*:?\s*([A-Za-z0-9\-/ ]+)',
        text,
        re.IGNORECASE
    )

    if reg:

        value = reg.group(1).strip()

        value = re.sub(r'\s+', ' ', value)

        value = value.strip(" ,.;:")

        return value

    return "Not specified"

