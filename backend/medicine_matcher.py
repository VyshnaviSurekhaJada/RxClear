import os
import pandas as pd
from rapidfuzz import process, fuzz

BASE_DIR = os.path.dirname(__file__)

CSV_PATH = os.path.join(
    BASE_DIR,
    "../datasets/medicines.csv"
)

df = pd.read_csv(CSV_PATH).fillna("")

df.fillna("", inplace=True)

medicine_names = list(
    set(
        df["name"].str.lower().tolist() +
        df["generic_name"].str.lower().tolist()
    )
)

alias_df = pd.read_csv(
    os.path.join(BASE_DIR, "../datasets/medicine_aliases.csv")
)

MEDICINE_MAPPING = dict(
    zip(
        alias_df["brand"].str.lower(),
        alias_df["generic"].str.lower()
    )
)


def fuzzy_match_medicine(name):

    if not name:
        return None

    name = name.lower().strip()

    # Exact brand mapping
    if name in MEDICINE_MAPPING:
        return MEDICINE_MAPPING[name]

    # Fuzzy match brand names
    brand_match = process.extractOne(
        name,
        MEDICINE_MAPPING.keys(),
        scorer=fuzz.WRatio,
        score_cutoff=85
    )

    if brand_match:
        return MEDICINE_MAPPING[brand_match[0]]

    # Fuzzy match generic names
    generic_match = process.extractOne(
        name,
        medicine_names,
        scorer=fuzz.WRatio,
        score_cutoff=88
    )

    if generic_match:
        return generic_match[0]

    return None


def get_medicine_info(name):

    if not name:
        return {}

    name = name.lower().strip()

    # Convert brand → generic first
    if name in MEDICINE_MAPPING:
        name = MEDICINE_MAPPING[name]

    row = df[
        (df["name"].str.lower() == name) |
        (df["generic_name"].str.lower() == name)
    ]

    if row.empty:
        return {}

    return row.iloc[0].to_dict()