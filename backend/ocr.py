"""OCR module: extracts text from prescription images using EasyOCR with PIL fallback."""
import re
import os
from pathlib import Path
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe\tesseract.exe"
)

def extract_text_from_image(image_path: str) -> str:
    """Extract text from prescription image using EasyOCR."""
    try:
        import easyocr
                # Read image
        image = cv2.imread(image_path)

        # Convert to grayscale
        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        # Reduce noise
        gray = cv2.GaussianBlur(
            gray,
            (3, 3),
            0
        )

        # Convert to black and white
        thresh = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )

        # Save temporary processed image
        temp_path = image_path + "_processed.jpg"

        cv2.imwrite(
            temp_path,
            thresh
        )
        reader = easyocr.Reader(['en'], gpu=False, verbose=False)

        results = reader.readtext(
            temp_path,
            detail=0,
            paragraph=True
        )

        if os.path.exists(temp_path):
            os.remove(temp_path)

        easy_text = "\n".join(
            [line.strip() for line in results if line.strip()]
        )


        tesseract_text = _fallback_ocr(image_path)

        # Keep EasyOCR for now
        if len(tesseract_text) > len(easy_text):
            text = tesseract_text
        else:
            text = easy_text

        return text.strip() if text.strip() else tesseract_text
    except Exception as e:
        print(f"EasyOCR failed: {e}. Trying fallback.")
        return _fallback_ocr(image_path)
    


def _fallback_ocr(image_path: str) -> str:
    try:
        import pytesseract
        from PIL import Image

        img = Image.open(image_path)

        text = pytesseract.image_to_string(img)

        return text.strip()

    except Exception as e:
        print(f"Tesseract also failed: {e}")
        return ""


def preprocess_text(raw_text: str) -> str:
    """Clean and normalize OCR output."""
    # Fix common OCR errors
    text = raw_text
    text = re.sub(r'\bO\b', '0', text)    # letter O → digit 0 in numeric context
    text = re.sub(r'\bl\b', '1', text)    # lowercase l → 1 in numeric context
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # remove non-ASCII
    text = re.sub(r'[ \t]+', ' ', text)   # normalize whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)  # collapse blank lines
    return text.strip()
