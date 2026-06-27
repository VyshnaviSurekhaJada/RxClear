"""Diet and lifestyle recommendations based on predicted disease."""

DIET_DB: dict[str, dict] = {
    "Viral Fever": {
        "eat": ["Coconut water", "Warm soups (clear)", "Fresh fruits (citrus)", "Rice congee/khichdi", "Ginger tea", "Turmeric milk"],
        "avoid": ["Spicy foods", "Oily/fried foods", "Raw/cold foods", "Alcohol", "Caffeine"],
        "lifestyle": ["Rest adequately", "Stay hydrated (3L+ fluids/day)", "Sponge baths for fever", "Avoid overexertion"],
    },
    "Fever with Pain": {
        "eat": ["Light khichdi", "Coconut water", "Herbal teas", "Bananas", "Toast/crackers"],
        "avoid": ["Heavy meals", "Dairy (if GI upset)", "Spicy food", "Alcohol"],
        "lifestyle": ["Rest", "Stay cool", "Monitor temperature every 4 hours"],
    },
    "Bacterial Fever": {
        "eat": ["Probiotic yogurt (after antibiotics)", "Fruit juices", "Soups", "Soft rice", "Buttermilk"],
        "avoid": ["Alcohol (interacts with antibiotics)", "Grapefruit", "Dairy with certain antibiotics"],
        "lifestyle": ["Complete full antibiotic course", "Rest", "Stay hydrated"],
    },
    "Type 2 Diabetes": {
        "eat": ["Leafy vegetables", "Whole grains (oats, brown rice)", "Legumes (dal, rajma)", "Low GI fruits (apple, pear)", "Nuts (walnuts, almonds)", "Fish"],
        "avoid": ["White rice (large portions)", "Sugary drinks", "Sweets/mithai", "Processed foods", "Fruit juices"],
        "lifestyle": ["30-min daily walk", "Monitor blood sugar regularly", "Eat at regular intervals", "Portion control"],
    },
    "Diabetic Hypertension": {
        "eat": ["DASH diet foods", "Potassium-rich foods (banana, spinach)", "Omega-3 rich fish", "Oats", "Low-fat dairy", "Garlic"],
        "avoid": ["High-sodium foods", "Pickles", "Processed meats", "Saturated fats", "Excess sugar"],
        "lifestyle": ["Regular BP monitoring", "Daily 30-min moderate exercise", "Stress management (yoga/meditation)", "Limit alcohol"],
    },
    "Type 2 Diabetes with Dyslipidemia": {
        "eat": ["Oats (reduces cholesterol)", "Almonds", "Olive oil", "Fatty fish (salmon)", "Avocado", "Flaxseeds"],
        "avoid": ["Trans fats", "Refined carbs", "Full-fat dairy", "Red meat", "Fried foods"],
        "lifestyle": ["Aerobic exercise 150 min/week", "Maintain healthy weight", "Regular lipid monitoring"],
    },
    "Hypertension": {
        "eat": ["Banana", "Spinach", "Beets", "Oats", "Low-fat dairy", "Berries", "Garlic", "Dark chocolate (70%)"],
        "avoid": ["Table salt", "Pickles", "Namkeen/chips", "Canned soups", "Alcohol", "Caffeine (excess)"],
        "lifestyle": ["DASH diet", "Limit sodium to <2g/day", "Regular aerobic exercise", "Manage stress", "No smoking"],
    },
    "Cardiovascular Disease": {
        "eat": ["Mediterranean diet", "Omega-3 fish", "Berries", "Leafy greens", "Olive oil", "Nuts", "Whole grains"],
        "avoid": ["Saturated fats", "Trans fats", "Excess sodium", "Alcohol", "Processed meats"],
        "lifestyle": ["Cardiac rehab if advised", "Light exercise (as per doctor)", "Stress management", "Medication adherence"],
    },
    "Allergic Rhinitis": {
        "eat": ["Honey (local)", "Ginger tea", "Turmeric milk", "Citrus fruits (Vitamin C)", "Omega-3 rich foods"],
        "avoid": ["Known allergens", "Cold foods/drinks", "Dairy (if worsens mucus)", "Alcohol"],
        "lifestyle": ["Use air purifiers", "Change pillowcases frequently", "Avoid outdoor exposure during high pollen", "Nasal rinse (saline)"],
    },
    "Allergic Asthma": {
        "eat": ["Vitamin D rich foods", "Magnesium-rich foods (dark chocolate, nuts)", "Apples", "Ginger", "Turmeric"],
        "avoid": ["Sulfites (wine, dried fruit)", "Cold drinks", "Known allergens", "Aspirin (if sensitive)"],
        "lifestyle": ["Use spacer with inhaler", "Avoid smoke/dust/pet dander", "Use peak flow meter", "Keep rescue inhaler accessible"],
    },
    "Asthma": {
        "eat": ["Anti-inflammatory foods", "Vitamin C foods", "Omega-3 fish", "Ginger", "Turmeric"],
        "avoid": ["Cold/icy foods", "Sulfites", "Food additives", "Gas-producing foods"],
        "lifestyle": ["Identify and avoid triggers", "Regular pulmonary function tests", "Breathing exercises (pranayama)"],
    },
    "GERD": {
        "eat": ["Oatmeal", "Ginger tea", "Non-citrus fruits", "Green vegetables", "Lean proteins", "Coconut water"],
        "avoid": ["Spicy foods", "Citrus fruits", "Tomatoes", "Chocolate", "Coffee", "Alcohol", "Mint", "Fatty foods"],
        "lifestyle": ["Eat smaller, more frequent meals", "Don't lie down for 2-3 hrs after eating", "Elevate head while sleeping", "Maintain healthy weight"],
    },
    "H. Pylori Infection": {
        "eat": ["Probiotic foods (yogurt, kefir)", "Broccoli sprouts", "Green tea", "Garlic", "Honey"],
        "avoid": ["Alcohol", "Coffee", "Spicy foods", "Acidic foods", "Carbonated drinks"],
        "lifestyle": ["Complete full antibiotic course", "Wash hands frequently", "Avoid sharing utensils"],
    },
    "Peptic Ulcer": {
        "eat": ["Cabbage juice", "Honey", "Probiotic yogurt", "Bland foods", "Oatmeal", "Sweet potatoes"],
        "avoid": ["NSAIDs (ibuprofen)", "Alcohol", "Coffee", "Spicy foods", "Acidic foods", "Smoking"],
        "lifestyle": ["Eat small, frequent meals", "Manage stress", "Avoid NSAIDs unless prescribed"],
    },
    "Acid Reflux": {
        "eat": ["Alkaline foods", "Bananas", "Oatmeal", "Ginger tea", "Fennel"],
        "avoid": ["Caffeine", "Alcohol", "Chocolate", "Peppermint", "Spicy or fatty foods"],
        "lifestyle": ["Don't eat 3 hours before bed", "Elevate head while sleeping", "Wear loose clothing", "Maintain healthy weight"],
    },
    "Hypothyroidism": {
        "eat": ["Selenium-rich foods (Brazil nuts)", "Iodine-rich foods (seaweed, iodized salt)", "Lean proteins", "Fruits and vegetables"],
        "avoid": ["Raw cruciferous vegetables (excess)", "Soy (excess)", "Gluten (if Hashimoto's)", "Coffee with levothyroxine"],
        "lifestyle": ["Take levothyroxine on empty stomach", "Regular thyroid function tests", "Light exercise to combat fatigue"],
    },
    "Depression": {
        "eat": ["Omega-3 fatty acids (fish, flaxseeds)", "Tryptophan foods (turkey, eggs, nuts)", "Whole grains", "Dark leafy greens", "Dark chocolate (moderate)"],
        "avoid": ["Alcohol", "Processed/sugary foods", "Caffeine (excess)", "Skipping meals"],
        "lifestyle": ["Regular aerobic exercise (natural antidepressant)", "Maintain sleep schedule", "Social connection", "Sunlight exposure", "Mindfulness/therapy"],
    },
    "Anxiety Disorder": {
        "eat": ["Magnesium-rich foods (leafy greens, nuts)", "Chamomile tea", "Omega-3 foods", "Probiotic foods", "Ashwagandha (adaptogen)"],
        "avoid": ["Caffeine (worsens anxiety)", "Alcohol", "Sugary foods", "Skipping meals"],
        "lifestyle": ["Diaphragmatic breathing exercises", "Progressive muscle relaxation", "Regular yoga/meditation", "Reduce screen time before bed"],
    },
    "Neuropathic Pain": {
        "eat": ["Alpha-lipoic acid foods (spinach, broccoli)", "B12 foods (eggs, dairy, fish)", "Anti-inflammatory foods", "Turmeric"],
        "avoid": ["Alcohol (worsens nerve damage)", "Excess sugar", "Processed foods"],
        "lifestyle": ["Gentle physiotherapy", "TENS therapy if advised", "Protect numb areas from injury", "Regular blood sugar monitoring (if diabetic)"],
    },
    "Urinary Tract Infection": {
        "eat": ["Cranberry juice (unsweetened)", "Probiotics", "Water (3L/day)", "Vitamin C foods", "Ginger tea"],
        "avoid": ["Caffeine", "Alcohol", "Spicy foods", "Artificial sweeteners", "Sugary drinks"],
        "lifestyle": ["Complete full antibiotic course", "Urinate after intercourse", "Wipe front to back", "Avoid tight synthetic underwear"],
    },
    "Musculoskeletal Pain": {
        "eat": ["Anti-inflammatory foods (turmeric, ginger)", "Calcium-rich foods", "Omega-3 fish", "Magnesium foods"],
        "avoid": ["Processed foods", "Red meat (excess)", "Alcohol", "Excess salt"],
        "lifestyle": ["RICE protocol (Rest, Ice, Compression, Elevation)", "Physiotherapy", "Gentle stretching", "Avoid overexertion"],
    },
    "Moderate to Severe Pain": {
        "eat": ["Anti-inflammatory diet", "Turmeric milk", "Ginger tea", "Omega-3 rich foods", "Magnesium foods"],
        "avoid": ["Alcohol (opioid interactions)", "Sedatives (with tramadol)", "Excess caffeine"],
        "lifestyle": ["Follow prescribed pain management", "Heat/cold therapy", "Gentle movement", "Sleep hygiene"],
    },
    "Arthritis with GERD": {
        "eat": ["Omega-3 foods (anti-inflammatory)", "Low-acid fruits", "Whole grains", "Lean proteins", "Olive oil"],
        "avoid": ["NSAIDs on empty stomach", "Acidic foods", "Spicy foods", "Alcohol", "Processed foods"],
        "lifestyle": ["Take NSAIDs with food and PPI", "Low-impact exercise (swimming)", "Weight management"],
    },
    "Autoimmune Disorder": {
        "eat": ["Anti-inflammatory foods", "Vitamin D foods", "Omega-3 rich foods", "Turmeric", "Green tea", "Probiotic foods"],
        "avoid": ["Processed/junk food", "Excess sugar", "Gluten (if sensitive)", "Alcohol", "Excess salt"],
        "lifestyle": ["Sun protection (if photosensitive)", "Stress management", "Regular rheumatology follow-up", "Adequate rest"],
    },
    "Allergic Reaction": {
        "eat": ["Anti-histamine foods (quercetin: apples, onions)", "Vitamin C foods", "Ginger tea"],
        "avoid": ["Known allergens", "Alcohol", "Aspirin (if allergic)", "Preservatives/additives"],
        "lifestyle": ["Carry emergency antihistamine", "Identify and document all allergens", "Wear medical alert bracelet if severe"],
    },
    "Mild Fever": {
        "eat": ["Warm soups", "Coconut water", "Citrus fruits", "Ginger tea", "Light khichdi"],
        "avoid": ["Spicy foods", "Oily foods", "Alcohol", "Cold drinks"],
        "lifestyle": ["Rest", "Stay hydrated", "Monitor temperature", "Sponge bath if needed"],
    },
    "Bronchospasm": {
        "eat": ["Warm fluids", "Ginger tea", "Honey", "Vitamin C foods"],
        "avoid": ["Cold foods", "Allergens", "Sulfites", "Aspirin (if sensitive)"],
        "lifestyle": ["Keep rescue inhaler always accessible", "Avoid triggers (smoke, dust, cold air)", "Breathing exercises"],
    },
    "Bacterial Infection": {
        "eat": ["Probiotic foods (yogurt)", "Garlic", "Honey", "Citrus fruits (Vitamin C)", "Bone broth"],
        "avoid": ["Alcohol (antibiotic interaction)", "Sugar (feeds bacteria)", "Processed foods"],
        "lifestyle": ["Complete full antibiotic course", "Rest", "Stay hydrated", "Practice good hygiene"],
    },
}

# Fallback for unknown diseases
_DEFAULT_DIET = {
    "eat": ["Balanced meals with fruits and vegetables", "Adequate hydration (2-3L water/day)", "Lean proteins", "Whole grains"],
    "avoid": ["Alcohol", "Processed and junk food", "Excessive salt and sugar"],
    "lifestyle": ["Regular moderate exercise", "7-8 hours sleep", "Follow medication schedule", "Regular follow-up with doctor"],
}


def get_recommendations(disease: str) -> dict:
    """Get diet and lifestyle recommendations for a given disease."""
    # Try exact match first
    if disease in DIET_DB:
        return DIET_DB[disease]

    # Try partial match
    disease_lower = str(disease or "").lower()
    for key in DIET_DB:
        if key.lower() in disease_lower or disease_lower in key.lower():
            return DIET_DB[key]

    # Keyword-based match
    keyword_map = {
        'diabetes': 'Type 2 Diabetes',
        'hypertension': 'Hypertension',
        'fever': 'Viral Fever',
        'asthma': 'Asthma',
        'allerg': 'Allergic Reaction',
        'gerd': 'GERD',
        'acid': 'Acid Reflux',
        'thyroid': 'Hypothyroidism',
        'depress': 'Depression',
        'anxiety': 'Anxiety Disorder',
        'pain': 'Moderate to Severe Pain',
        'infection': 'Bacterial Infection',
        'uti': 'Urinary Tract Infection',
        'cardiovascular': 'Cardiovascular Disease',
        'cardiac': 'Cardiovascular Disease',
    }
    for keyword, mapped_disease in keyword_map.items():
        if keyword in disease_lower:
            return DIET_DB.get(mapped_disease, _DEFAULT_DIET)

    return _DEFAULT_DIET
