import re
import os

# ── EasyOCR reader (lazy-loaded, cached) ─────────────────────────────────────
_easyocr_reader = None

def _get_easyocr():
    global _easyocr_reader
    if _easyocr_reader is None:
        try:
            import easyocr
            print("[OCR] Loading EasyOCR model (first run may take a moment)...")
            _easyocr_reader = easyocr.Reader(['en'], gpu=False, verbose=False)
            print("[OCR] EasyOCR ready.")
        except Exception as e:
            print(f"[OCR] EasyOCR load failed: {e}")
            _easyocr_reader = None
    return _easyocr_reader

# ── Tesseract fallback ────────────────────────────────────────────────────────
TESSERACT_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    r"C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe".format(
        os.environ.get("USERNAME", "")
    ),
]

def _configure_tesseract():
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        return True
    except Exception:
        pass
    try:
        import pytesseract
        for path in TESSERACT_PATHS:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                try:
                    pytesseract.get_tesseract_version()
                    print(f"[OCR] Tesseract found at: {path}")
                    return True
                except Exception:
                    continue
    except ImportError:
        pass
    return False

_TESSERACT_OK = _configure_tesseract()

# ── Image preprocessing ───────────────────────────────────────────────────────
def _preprocess(img):
    try:
        from PIL import ImageFilter, ImageEnhance, ImageOps
        img = img.convert("L")
        img = ImageEnhance.Contrast(img).enhance(2.2)
        img = img.filter(ImageFilter.SHARPEN)
        img = ImageOps.autocontrast(img)
        return img
    except Exception:
        return img.convert("L")

# ── Main OCR function ─────────────────────────────────────────────────────────
def extract_amount_from_image(filepath):
    """
    Try EasyOCR first (no Tesseract needed), fall back to pytesseract.
    Returns (amount, raw_text).
    """
    raw_text = ""
    amount = None

    # ── Method 1: EasyOCR ────────────────────────────────────────────────────
    reader = _get_easyocr()
    if reader is not None:
        try:
            results = reader.readtext(filepath, detail=0, paragraph=True)
            raw_text = "\n".join(results)
            print(f"[OCR] EasyOCR extracted {len(raw_text)} chars")
            if raw_text.strip():
                amount = detect_amount(raw_text)
                if amount:
                    print(f"[OCR] EasyOCR found amount: {amount}")
                    return amount, raw_text
        except Exception as e:
            print(f"[OCR] EasyOCR failed: {e}")

    # ── Method 2: Tesseract fallback ────────────────────────────────────────
    if _TESSERACT_OK:
        try:
            import pytesseract
            from PIL import Image
            img = Image.open(filepath)
            img = _preprocess(img)
            text = pytesseract.image_to_string(img, config='--psm 6')
            raw_text = text if not raw_text else raw_text + "\n\n--- Tesseract ---\n" + text
            print(f"[OCR] Tesseract extracted {len(text)} chars")
            if text.strip():
                amount = detect_amount(text)
                if amount:
                    print(f"[OCR] Tesseract found amount: {amount}")
                    return amount, raw_text
        except Exception as e:
            print(f"[OCR] Tesseract failed: {e}")

    print("[OCR] No amount detected from either method")
    return None, raw_text or "No text could be extracted from the image"


# ── Amount detection ──────────────────────────────────────────────────────────
def detect_amount(text):
    """
    Find the most likely total/bill amount from OCR text.
    Handles ₹, Rs., $, £, €, Indian bill formats, and plain numbers.
    """
    if not text:
        return None

    # Normalize common OCR misreads
    normalized = text
    # Rs. variants
    normalized = re.sub(r'\bR[s5][.\s]?\b', 'Rs. ', normalized, flags=re.IGNORECASE)
    normalized = re.sub(r'\bINR\b', 'Rs. ', normalized, flags=re.IGNORECASE)
    # Remove trailing /- (Indian bill style: 1250/-)
    normalized = re.sub(r'([\d,]+)\s*/\s*-', r'\1', normalized)

    print(f"[OCR] Detecting amount from text:\n{text[:300]}")

    # ── Priority 1: labeled totals ────────────────────────────────────────────
    labeled_patterns = [
        # Grand total / net payable etc. followed by amount (same line or next line)
        r"(?:grand\s*total|total\s*amount|net\s*amount|amount\s*due|"
        r"balance\s*due|total\s*payable|payable\s*amount|bill\s*amount|"
        r"net\s*payable|amount\s*payable|total\s*bill|final\s*amount)"
        r"[\s:Rs.₹$]*([0-9][0-9,]*\.?[0-9]{0,2})",

        r"(?:total|subtotal|sub\s*total|bill\s*total|to\s*pay|to\s*be\s*paid)"
        r"[\s:Rs.₹$]*([0-9][0-9,]*\.?[0-9]{0,2})",

        # Rs./₹ followed by number
        r"(?:rs\.?|₹|inr)\s*([0-9][0-9,]*\.?[0-9]{0,2})",
    ]
    for pattern in labeled_patterns:
        match = re.search(pattern, normalized, re.IGNORECASE)
        if match:
            val = match.group(1).replace(",", "")
            try:
                f = float(val)
                if f > 0:
                    print(f"[OCR] Amount found via labeled pattern: {f}")
                    return f
            except ValueError:
                continue

    # ── Priority 2: multi-line — label on one line, amount on next ───────────
    lines = [l.strip() for l in normalized.split('\n') if l.strip()]
    total_keywords = {'total', 'amount', 'payable', 'pay', 'bill', 'net', 'grand', 'due', 'balance'}
    for i, line in enumerate(lines):
        words = set(re.findall(r'\w+', line.lower()))
        if words & total_keywords:
            # Check this line and next 2 lines for a number
            for j in range(i, min(i + 3, len(lines))):
                nums = re.findall(r'[₹$]?\s*([0-9][0-9,]*\.[0-9]{2})', lines[j])
                if not nums:
                    nums = re.findall(r'[₹$]?\s*([0-9]{2,6})', lines[j])
                for n in nums:
                    try:
                        f = float(n.replace(',', ''))
                        if f >= 1:
                            print(f"[OCR] Amount found via multi-line: {f}")
                            return f
                    except ValueError:
                        pass

    # ── Priority 3: currency symbol + number ─────────────────────────────────
    currency_matches = re.findall(r"[₹\$\£\€]\s*([0-9][0-9,]*\.?[0-9]{0,2})", normalized)
    if currency_matches:
        amounts = []
        for m in currency_matches:
            try:
                amounts.append(float(m.replace(",", "")))
            except ValueError:
                pass
        if amounts:
            result = max(amounts)
            print(f"[OCR] Amount found via currency symbol: {result}")
            return result

    # ── Priority 4: decimal numbers like 1,250.00 ────────────────────────────
    decimal_matches = re.findall(r"\b([0-9][0-9,]{0,8}\.[0-9]{2})\b", normalized)
    if decimal_matches:
        amounts = []
        for m in decimal_matches:
            try:
                amounts.append(float(m.replace(",", "")))
            except ValueError:
                pass
        if amounts:
            result = max(amounts)
            print(f"[OCR] Amount found via decimal: {result}")
            return result

    # ── Priority 5: largest plain number that looks like a price ─────────────
    plain_matches = re.findall(r"\b([0-9]{2,7})\b", normalized)
    if plain_matches:
        prices = []
        for x in plain_matches:
            try:
                n = int(x)
                if 10 <= n <= 9999999:
                    prices.append(n)
            except ValueError:
                pass
        if prices:
            result = float(max(prices))
            print(f"[OCR] Amount found via plain number: {result}")
            return result

    print("[OCR] No amount detected")
    return None
