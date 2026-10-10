"""
Synthetic document generator for RTO Sahayak Milestone 2.

Generates 4 synthetic ID PNG images and 4 JSON expected field files using Pillow.
Adheres to project rules:
- Exclusively synthetic / mock data.
- Labeled 'SYNTHETIC' and 'DRAFT - for citizen review and officer verification'.
- Mandatory disclaimer: 'Final decision rests with the RTO officer.'
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Document definitions for 4 synthetic samples
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
        "date_of_birth": "1993-05-15",  # Mismatched DOB with doc1
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
        "date_of_birth": "22/11/1998",  # Slash format matching 1998-11-22 in doc3
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
    """Load system font with graceful multi-tier fallbacks."""
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


def generate_document_image(doc: dict, output_path: Path) -> None:
    """Generate an authentic 800x500 synthetic card PNG."""
    width, height = 800, 500
    img = Image.new("RGB", (width, height), doc["bg_color"])
    draw = ImageDraw.Draw(img)

    f_title = load_font(18, bold=True)
    f_sub = load_font(14, bold=True)
    f_label = load_font(13, bold=True)
    f_val = load_font(13, bold=False)
    f_small = load_font(11, bold=False)
    f_banner = load_font(13, bold=True)

    # 1. Outer and inner card borders
    draw.rectangle([0, 0, width - 1, height - 1], outline=doc["border_color"], width=4)
    draw.rectangle([8, 8, width - 9, height - 9], outline=(203, 213, 225), width=1)

    # 2. Diagonal background watermark
    watermark_text = "SYNTHETIC SAMPLE - NOT REAL - FOR TESTING ONLY"
    for wy in [140, 220, 300, 380]:
        draw.text((80, wy), watermark_text, fill=(225, 230, 238), font=f_title)

    # 3. Top Alert Banner
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

    # 5. Left Column: Photo Box, Mock QR, Specimen Signature
    # Photo Frame
    draw.rectangle([40, 110, 160, 245], fill=(238, 242, 246), outline=(148, 163, 184), width=2)
    draw.ellipse([75, 130, 125, 180], fill=(203, 213, 225))
    draw.arc([60, 180, 140, 235], 0, 180, fill=(148, 163, 184), width=3)
    draw.text((100, 225), "[PHOTO: SYNTHETIC]", fill=(100, 116, 139), font=f_small, anchor="mm")

    # Mock QR Frame
    draw.rectangle([45, 255, 155, 365], fill=(255, 255, 255), outline=(100, 116, 139), width=1)
    for qx in range(55, 145, 15):
        for qy in range(265, 345, 15):
            if (qx + qy) % 30 == 0 or (qx * qy) % 25 == 0:
                draw.rectangle([qx, qy, qx + 10, qy + 10], fill=(0, 0, 0))
    draw.text((100, 355), "[SYNTHETIC QR]", fill=(71, 85, 105), font=f_small, anchor="mm")

    # Specimen Signature Frame
    draw.rectangle([40, 380, 160, 440], fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    draw.text((100, 400), "[Specimen Signature]", fill=(100, 116, 139), font=f_small, anchor="mm")
    draw.text((100, 422), doc["full_name"][:16], fill=(30, 41, 59), font=f_sub, anchor="mm")

    # 6. Right Column: Document Details Grid
    rx = 185
    # Document number highlight box
    draw.rectangle([rx, 108, width - 35, 142], fill=(241, 245, 249), outline=doc["border_color"], width=1)
    draw.text((rx + 10, 125), f"DOC NO: {doc['document_number']}", fill=doc["header_color"], font=f_sub, anchor="lm")

    # Identity key-value rows
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
    draw.text((rx + 10, 415), "Final decision rests with the RTO officer.", fill=(100, 116, 139), font=f_small)

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


def generate_document_json(doc: dict, output_path: Path) -> None:
    """Generate expected extracted JSON data."""
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
        "disclaimer": "SYNTHETIC DOCUMENT - FOR TESTING ONLY. DRAFT - for citizen review and officer verification. Final decision rests with the RTO officer.",
    }
    if doc.get("vehicle_class"):
        data["vehicle_class"] = doc["vehicle_class"]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


PNG_MAGIC_BYTES = b"\x89PNG\r\n\x1a\n"


def get_default_sample_dirs() -> list[Path]:
    """Return candidate sample directories in repository root and rto-sahayak subfolder."""
    here = Path(__file__).resolve().parent
    if here.name == "rto-sahayak":
        repo_root = here.parent
    else:
        repo_root = here
    dirs = [repo_root / "data" / "samples"]
    sub = repo_root / "rto-sahayak" / "data" / "samples"
    if (repo_root / "rto-sahayak").is_dir():
        dirs.append(sub)
    return dirs


def _generate_samples_to_dir(target_path: Path) -> None:
    """Generate all 4 synthetic PNG images and JSON files into target_path."""
    target_path.mkdir(parents=True, exist_ok=True)
    for doc in DOCUMENTS:
        img_file = target_path / f"{doc['filename']}.png"
        json_file = target_path / f"{doc['filename']}.json"
        generate_document_image(doc, img_file)
        generate_document_json(doc, json_file)


def generate_all_samples(target_dir: str | Path | None = None) -> None:
    """Generate authentic Pillow-rendered 800x500 binary PNGs and JSONs to target_dir or both repositories."""
    if target_dir is None:
        for target in get_default_sample_dirs():
            _generate_samples_to_dir(target)
    else:
        _generate_samples_to_dir(Path(target_dir))


def ensure_samples(target_dir: str | Path | None = None) -> None:
    """
    Ensure authentic binary PNGs and JSONs exist in target_dir (or all default locations).
    If any sample is missing or lacks standard PNG magic bytes, regenerates them using Pillow.
    """
    if target_dir is None:
        targets = get_default_sample_dirs()
    else:
        targets = [Path(target_dir)]

    for target_path in targets:
        needs_generation = False
        for doc in DOCUMENTS:
            img_file = target_path / f"{doc['filename']}.png"
            json_file = target_path / f"{doc['filename']}.json"
            if not img_file.exists() or not json_file.exists():
                needs_generation = True
                break
            try:
                if img_file.stat().st_size < 1024:
                    needs_generation = True
                    break
                with open(img_file, "rb") as bf:
                    if bf.read(8) != PNG_MAGIC_BYTES:
                        needs_generation = True
                        break
            except Exception:
                needs_generation = True
                break

        if needs_generation:
            _generate_samples_to_dir(target_path)


if __name__ == "__main__":
    generate_all_samples()

