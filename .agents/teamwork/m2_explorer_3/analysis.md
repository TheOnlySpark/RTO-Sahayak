# Synthetic Image and Field Extraction Specification & Architecture

**Explorer**: `m2_explorer_3` (Synthetic Image Explorer)  
**Date**: 2026-10-10  
**Target Milestone**: Milestone 2 (Document Verification, Synthetic Samples & Comparison)

---

## 1. Executive Summary

This document specifies the end-to-end design for the 4 synthetic ID documents, their visual layout, Pillow generation code, and expected extracted JSON metadata for RTO Sahayak Milestone 2.

All documents strictly adhere to:
1. **Synthetic data safety**: Exclusively synthetic/mock information; all documents bear prominent `"SYNTHETIC"` warnings, fake numbering (`FAKE-*`), and the banner `"DRAFT - for citizen review and officer verification"`.
2. **Key pair requirement**: Two documents (`doc1_driving_licence` and `doc2_aadhaar_card`) share the exact same person name (`Rahul Kumar Sharma`) but feature different dates of birth (`1995-05-15` vs `1993-05-15`).
3. **Matching pair requirement**: Two documents (`doc3_pan_card` and `doc4_voter_id`) represent a matching pair testing fuzzy name comparison (`Priya S. Patel` vs `Priya Sanjay Patel`) and date normalization (`1998-11-22` vs `22/11/1998`).
4. **Pillow pure rendering**: Requires only standard Pillow (`PIL.Image`, `PIL.ImageDraw`, `PIL.ImageFont`) without external image dependencies or online network calls.

---

## 2. Document Catalog & Specification

| File Prefix | Document Type | Document ID | Subject Name | DOB | Document Number | Matching Role |
|---|---|---|---|---|---|---|
| `doc1_driving_licence` | Driving Licence | `doc1_driving_licence` | Rahul Kumar Sharma | `1995-05-15` | `FAKE-DL-DL04-20150001` | **Mismatched Pair (Doc A)** |
| `doc2_aadhaar_card` | Aadhaar Card | `doc2_aadhaar_card` | Rahul Kumar Sharma | `1993-05-15` | `FAKE-UID-9999-8888-7777` | **Mismatched Pair (Doc B)** |
| `doc3_pan_card` | PAN Card | `doc3_pan_card` | Priya S. Patel | `1998-11-22` | `FAKE-PAN-ABCDE1234F` | **Matching Pair (Doc A)** |
| `doc4_voter_id` | Voter ID Card | `doc4_voter_id` | Priya Sanjay Patel | `22/11/1998` | `FAKE-EPIC-XYZ9876543` | **Matching Pair (Doc B)** |

---

## 3. Visual Layout & Pillow Design

### 3.1 Dimensions and Geometry
- **Resolution**: `800 x 500` pixels (standard card aspect ratio 1.6 : 1, ideal for OCR/visual inspection).
- **Color Palettes**:
  - `doc1_driving_licence`: Slate-blue tint `(242, 246, 252)`, Navy borders `(30, 58, 138)`.
  - `doc2_aadhaar_card`: Pale cream `(253, 251, 247)`, Saffron & Green accents, Crimson borders `(153, 27, 27)`.
  - `doc3_pan_card`: Soft icy cyan `(240, 248, 248)`, Deep Teal borders `(17, 94, 89)`.
  - `doc4_voter_id`: Warm ivory `(252, 250, 240)`, Dark Amber borders `(146, 64, 14)`.

### 3.2 Visual Components
1. **Top Synthetic Warning Banner**:
   - Area: `(0, 0, 800, 36)`.
   - Fill: `(185, 28, 28)` (Alert Red).
   - Text: `*** SYNTHETIC DOCUMENT - FOR TESTING ONLY ***` (White, Bold, Centered).
2. **Bottom Official Notice Banner**:
   - Area: `(0, 464, 800, 500)`.
   - Fill: `(30, 41, 59)` (Slate Blue).
   - Text: `DRAFT - for citizen review and officer verification` (Light Gray/White, Centered).
3. **Card Header**:
   - Simulated Emblem: Concentric circles with mock badge text `"MOCK"`.
   - Header text: `GOVERNMENT OF INDIA (MOCK / SYNTHETIC)`.
   - Document Title: e.g. `FORM 7 - DRIVING LICENCE`, `UNIQUE IDENTIFICATION AUTHORITY (MOCK)`.
4. **Watermark Pattern**:
   - Low-contrast repeating diagonal text across background: `SYNTHETIC SAMPLE - NOT REAL` in `(226, 232, 240)`.
5. **Left Column (Visual Placeholders)**:
   - Photo Frame: `(40, 110, 160, 245)`, stylized silhouette with text `[PHOTO]` and `[SYNTHETIC]`.
   - QR Code Frame: `(45, 260, 155, 370)`, procedural grid pattern simulating a 2D QR barcode, labeled `[MOCK QR]`.
   - Specimen Signature Frame: `(40, 385, 160, 440)`, mock signature line `[Specimen Signature]`.
6. **Right Column (Key Field Grid)**:
   - Primary Number Highlight Box: `(185, 108, 765, 142)` with bold document number.
   - Distinct Rows for:
     - Full Name
     - Date of Birth
     - Father / Guardian Name
     - Address
     - Issue Date / Validity
     - Authority / Vehicle Class
   - Mandatory Disclaimer Box: `(185, 385, 765, 445)` noting:
     `"Notice: Synthetic sample for testing. Final decision rests with the RTO officer."`

### 3.3 Robust Font Loading Mechanism
To avoid runtime errors across varying operating systems and container environments where system fonts might not be installed, the font loader uses a multi-tier fallback:

```python
def load_font(size: int = 14, bold: bool = False):
    font_candidates = [
        "arialbd.ttf" if bold else "arial.ttf",
        "calibrib.ttf" if bold else "calibri.ttf",
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf",
        "arial.ttf",
        "calibri.ttf",
    ]
    for font_name in font_candidates:
        try:
            return ImageFont.truetype(font_name, size)
        except (OSError, IOError):
            continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()
```

---

## 4. Expected Extracted Fields JSON Schemas

### 4.1 Schema Definition
Each JSON metadata file contains:
- `doc_id`: Unique document key (used in `doc_a` / `doc_b` comparison output).
- `document_type`: Human-readable document class.
- `document_number`: Synthetic identifier (`FAKE-*`).
- `full_name`: Name as extracted from document.
- `date_of_birth`: Extracted DOB string.
- `father_name`: Father/Guardian name.
- `address`: Residential address string.
- `issue_date`: Date of issuance.
- `expiry_date`: Expiry date or `null`.
- `issuing_authority`: Issuing entity mock title.
- `is_synthetic`: Always `true`.
- `disclaimer`: Standard verification notice.

### 4.2 Document 1: `doc1_driving_licence.json`
```json
{
  "doc_id": "doc1_driving_licence",
  "document_type": "Driving Licence",
  "document_number": "FAKE-DL-DL04-20150001",
  "full_name": "Rahul Kumar Sharma",
  "date_of_birth": "1995-05-15",
  "father_name": "Suresh Kumar Sharma",
  "address": "123, Gandhi Marg, Synthetic City, New Delhi - 110001",
  "issue_date": "2015-06-20",
  "expiry_date": "2035-05-14",
  "vehicle_class": "LMV, MCWG",
  "issuing_authority": "RTO Synthetic Zone 04, New Delhi",
  "is_synthetic": true,
  "disclaimer": "SYNTHETIC DOCUMENT - FOR TESTING ONLY. DRAFT - for citizen review and officer verification"
}
```

### 4.3 Document 2: `doc2_aadhaar_card.json`
```json
{
  "doc_id": "doc2_aadhaar_card",
  "document_type": "Aadhaar Card",
  "document_number": "FAKE-UID-9999-8888-7777",
  "full_name": "Rahul Kumar Sharma",
  "date_of_birth": "1993-05-15",
  "father_name": "Suresh Kumar Sharma",
  "address": "123, Gandhi Marg, Synthetic City, New Delhi - 110001",
  "issue_date": "2012-08-10",
  "expiry_date": null,
  "issuing_authority": "UIDAI (Synthetic Mock)",
  "is_synthetic": true,
  "disclaimer": "SYNTHETIC DOCUMENT - FOR TESTING ONLY. DRAFT - for citizen review and officer verification"
}
```

### 4.4 Document 3: `doc3_pan_card.json`
```json
{
  "doc_id": "doc3_pan_card",
  "document_type": "PAN Card",
  "document_number": "FAKE-PAN-ABCDE1234F",
  "full_name": "Priya S. Patel",
  "date_of_birth": "1998-11-22",
  "father_name": "Sanjay Patel",
  "address": "45, Patel Colony, Synthetic Nagar, Ahmedabad - 380001",
  "issue_date": "2018-03-15",
  "expiry_date": null,
  "issuing_authority": "Income Tax Department (Synthetic Mock)",
  "is_synthetic": true,
  "disclaimer": "SYNTHETIC DOCUMENT - FOR TESTING ONLY. DRAFT - for citizen review and officer verification"
}
```

### 4.5 Document 4: `doc4_voter_id.json`
```json
{
  "doc_id": "doc4_voter_id",
  "document_type": "Voter ID Card",
  "document_number": "FAKE-EPIC-XYZ9876543",
  "full_name": "Priya Sanjay Patel",
  "date_of_birth": "22/11/1998",
  "father_name": "Sanjay Patel",
  "address": "45, Patel Colony, Synthetic Nagar, Ahmedabad - 380001",
  "issue_date": "2017-01-10",
  "expiry_date": null,
  "issuing_authority": "Election Commission of India (Synthetic Mock)",
  "is_synthetic": true,
  "disclaimer": "SYNTHETIC DOCUMENT - FOR TESTING ONLY. DRAFT - for citizen review and officer verification"
}
```

---

## 5. Verification Mapping with `compare_documents`

| Test Case | Documents Passed | Expected Comparison Output |
|---|---|---|
| **Mismatched DOB Pair** | `[doc1, doc2]` | `{"mismatches": [{"field": "date_of_birth", "doc_a": "doc1_driving_licence", "value_a": "1995-05-15", "doc_b": "doc2_aadhaar_card", "value_b": "1993-05-15"}]}` |
| **Matching Pair** | `[doc3, doc4]` | `{"mismatches": []}` (Name matched fuzzy: `Priya S. Patel` == `Priya Sanjay Patel`; DOB matched after normalizing `22/11/1998` to `1998-11-22`) |
| **Mismatched Name Pair** | `[doc1, doc3]` | `{"mismatches": [{"field": "full_name", ...}, {"field": "date_of_birth", ...}]}` |

---

## 6. Complete Python Generator Script Blueprint

Below is the standalone script implementation proposed for `data/generate_samples.py`:

```python
"""Synthetic document generator for RTO Sahayak Milestone 2.

Generates 4 synthetic ID PNG images and 4 JSON expected field files.
"""

from __future__ import annotations

import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Document definitions
DOCUMENTS = [
    {
        "filename": "doc1_driving_licence",
        "doc_id": "doc1_driving_licence",
        "document_type": "Driving Licence",
        "document_number": "FAKE-DL-DL04-20150001",
        "full_name": "Rahul Kumar Sharma",
        "date_of_birth": "1995-05-15",
        "father_name": "Suresh Kumar Sharma",
        "address": "123, Gandhi Marg, Synthetic City, New Delhi - 110001",
        "issue_date": "2015-06-20",
        "expiry_date": "2035-05-14",
        "vehicle_class": "LMV, MCWG",
        "issuing_authority": "RTO Synthetic Zone 04, New Delhi",
        "bg_color": (242, 246, 252),
        "border_color": (30, 58, 138),
        "header_color": (23, 37, 84),
    },
    {
        "filename": "doc2_aadhaar_card",
        "doc_id": "doc2_aadhaar_card",
        "document_type": "Aadhaar Card",
        "document_number": "FAKE-UID-9999-8888-7777",
        "full_name": "Rahul Kumar Sharma",
        "date_of_birth": "1993-05-15",  # Mismatch DOB
        "father_name": "Suresh Kumar Sharma",
        "address": "123, Gandhi Marg, Synthetic City, New Delhi - 110001",
        "issue_date": "2012-08-10",
        "expiry_date": None,
        "issuing_authority": "UIDAI (Synthetic Mock)",
        "bg_color": (253, 251, 247),
        "border_color": (153, 27, 27),
        "header_color": (127, 29, 29),
    },
    {
        "filename": "doc3_pan_card",
        "doc_id": "doc3_pan_card",
        "document_type": "PAN Card",
        "document_number": "FAKE-PAN-ABCDE1234F",
        "full_name": "Priya S. Patel",
        "date_of_birth": "1998-11-22",
        "father_name": "Sanjay Patel",
        "address": "45, Patel Colony, Synthetic Nagar, Ahmedabad - 380001",
        "issue_date": "2018-03-15",
        "expiry_date": None,
        "issuing_authority": "Income Tax Department (Synthetic Mock)",
        "bg_color": (240, 248, 248),
        "border_color": (17, 94, 89),
        "header_color": (19, 78, 74),
    },
    {
        "filename": "doc4_voter_id",
        "doc_id": "doc4_voter_id",
        "document_type": "Voter ID Card",
        "document_number": "FAKE-EPIC-XYZ9876543",
        "full_name": "Priya Sanjay Patel",
        "date_of_birth": "22/11/1998",  # Slash format matching 1998-11-22
        "father_name": "Sanjay Patel",
        "address": "45, Patel Colony, Synthetic Nagar, Ahmedabad - 380001",
        "issue_date": "2017-01-10",
        "expiry_date": None,
        "issuing_authority": "Election Commission of India (Synthetic Mock)",
        "bg_color": (252, 250, 240),
        "border_color": (146, 64, 14),
        "header_color": (120, 53, 15),
    },
]


def load_font(size: int = 14, bold: bool = False):
    font_candidates = [
        "arialbd.ttf" if bold else "arial.ttf",
        "calibrib.ttf" if bold else "calibri.ttf",
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf",
        "arial.ttf",
        "calibri.ttf",
    ]
    for font_name in font_candidates:
        try:
            return ImageFont.truetype(font_name, size)
        except (OSError, IOError):
            continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def generate_document_image(doc: dict, output_path: Path):
    width, height = 800, 500
    img = Image.new("RGB", (width, height), doc["bg_color"])
    draw = ImageDraw.Draw(img)

    f_title = load_font(18, bold=True)
    f_sub = load_font(14, bold=True)
    f_label = load_font(13, bold=True)
    f_val = load_font(13, bold=False)
    f_small = load_font(11, bold=False)
    f_banner = load_font(13, bold=True)

    # 1. Outer & inner borders
    draw.rectangle([0, 0, width - 1, height - 1], outline=doc["border_color"], width=4)
    draw.rectangle([8, 8, width - 9, height - 9], outline=(203, 213, 225), width=1)

    # 2. Diagonal Watermark
    watermark_text = "SYNTHETIC SAMPLE - NOT REAL - FOR TESTING ONLY"
    for wy in [140, 220, 300, 380]:
        draw.text((80, wy), watermark_text, fill=(225, 230, 238), font=f_title)

    # 3. Top Banner
    draw.rectangle([0, 0, width, 36], fill=(185, 28, 28))
    draw.text(
        (width // 2, 18),
        "*** SYNTHETIC DOCUMENT - FOR TESTING ONLY ***",
        fill=(255, 255, 255),
        font=f_banner,
        anchor="mm",
    )

    # 4. Header Section
    draw.ellipse([40, 48, 80, 88], outline=doc["header_color"], width=2)
    draw.text((60, 68), "MOCK", fill=doc["header_color"], font=f_small, anchor="mm")
    draw.text((100, 52), "GOVERNMENT OF INDIA (MOCK / SYNTHETIC)", fill=(51, 65, 85), font=f_small)
    draw.text((100, 68), f"FORM - {doc['document_type'].upper()}", fill=doc["header_color"], font=f_title)
    draw.line([(30, 96), (width - 30, 96)], fill=(203, 213, 225), width=2)

    # 5. Left Column: Photo, Mock QR, Specimen Signature
    # Photo box
    draw.rectangle([40, 110, 160, 245], fill=(238, 242, 246), outline=(148, 163, 184), width=2)
    draw.ellipse([75, 130, 125, 180], fill=(203, 213, 225))
    draw.arc([60, 180, 140, 235], 0, 180, fill=(148, 163, 184), width=3)
    draw.text((100, 225), "[PHOTO: SYNTHETIC]", fill=(100, 116, 139), font=f_small, anchor="mm")

    # Mock QR Box
    draw.rectangle([45, 255, 155, 365], fill=(255, 255, 255), outline=(100, 116, 139), width=1)
    for qx in range(55, 145, 15):
        for qy in range(265, 345, 15):
            if (qx + qy) % 30 == 0 or (qx * qy) % 25 == 0:
                draw.rectangle([qx, qy, qx + 10, qy + 10], fill=(0, 0, 0))
    draw.text((100, 355), "[SYNTHETIC QR]", fill=(71, 85, 105), font=f_small, anchor="mm")

    # Signature box
    draw.rectangle([40, 380, 160, 440], fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    draw.text((100, 400), "[Specimen Signature]", fill=(100, 116, 139), font=f_small, anchor="mm")
    draw.text((100, 422), doc["full_name"][:16], fill=(30, 41, 59), font=f_sub, anchor="mm")

    # 6. Right Column: Document Details
    rx = 185
    # Document number highlight box
    draw.rectangle([rx, 108, width - 35, 142], fill=(241, 245, 249), outline=doc["border_color"], width=1)
    draw.text((rx + 10, 125), f"DOC NO: {doc['document_number']}", fill=doc["header_color"], font=f_sub, anchor="lm")

    # Key-value rows
    rows = [
        ("Full Name:", doc["full_name"]),
        ("Date of Birth:", doc["date_of_birth"]),
        ("Father's Name:", doc["father_name"]),
        ("Address:", doc["address"]),
        ("Issue Date:", doc["issue_date"]),
        ("Issuing Auth:", doc["issuing_authority"]),
    ]
    if doc.get("vehicle_class"):
        rows.insert(4, ("Vehicle Class:", doc["vehicle_class"]))
    if doc.get("expiry_date"):
        rows.insert(5, ("Valid Till:", doc["expiry_date"]))

    curr_y = 155
    for label, val in rows:
        draw.text((rx, curr_y), label, fill=(71, 85, 105), font=f_label)
        draw.text((rx + 130, curr_y), str(val), fill=(15, 23, 42), font=f_val)
        curr_y += 28

    # Notice box
    draw.rectangle([rx, 380, width - 35, 440], fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    draw.text((rx + 10, 395), "Notice: Synthetic test record. Not a government-issued document.", fill=(100, 116, 139), font=f_small)
    draw.text((rx + 10, 415), "Every rule explanation cites its source file. Final decision rests with the RTO officer.", fill=(100, 116, 139), font=f_small)

    # 7. Bottom Banner
    draw.rectangle([0, height - 36, width, height], fill=(30, 41, 59))
    draw.text(
        (width // 2, height - 18),
        "DRAFT - for citizen review and officer verification",
        fill=(241, 245, 249),
        font=f_banner,
        anchor="mm",
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG")


def generate_document_json(doc: dict, output_path: Path):
    data = {
        "doc_id": doc["doc_id"],
        "document_type": doc["document_type"],
        "document_number": doc["document_number"],
        "full_name": doc["full_name"],
        "date_of_birth": doc["date_of_birth"],
        "father_name": doc["father_name"],
        "address": doc["address"],
        "issue_date": doc["issue_date"],
        "expiry_date": doc.get("expiry_date"),
        "issuing_authority": doc["issuing_authority"],
        "is_synthetic": True,
        "disclaimer": "SYNTHETIC DOCUMENT - FOR TESTING ONLY. DRAFT - for citizen review and officer verification",
    }
    if doc.get("vehicle_class"):
        data["vehicle_class"] = doc["vehicle_class"]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def generate_all_samples(target_dir: str | Path):
    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)
    for doc in DOCUMENTS:
        img_file = target_path / f"{doc['filename']}.png"
        json_file = target_path / f"{doc['filename']}.json"
        generate_document_image(doc, img_file)
        generate_document_json(doc, json_file)
        print(f"Generated: {img_file.name} and {json_file.name}")


if __name__ == "__main__":
    generate_all_samples("data/samples")
```
