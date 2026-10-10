# BRIEFING — 2026-10-10T07:44:00Z

## Mission
Design 4 synthetic ID/certificate PNG documents and their expected extracted JSON schemas using Pillow for milestone 2 testing.

## 🔒 My Identity
- Archetype: explorer
- Roles: Synthetic Image Explorer
- Working directory: e:\hackthon\.agents\teamwork\m2_explorer_3
- Original parent: e35c4cb9-e0bf-457f-8b67-5c1e9c1c606b
- Milestone: milestone_2

## 🔒 Key Constraints
- Read-only investigation — do NOT implement directly in project directories; write proposals/designs in working directory.
- Synthetic, public or mock data only. Never ask for or store real personal data.
- Label sample documents "SYNTHETIC".
- Must design Pillow generation for 4 fake ID/certificate PNGs in data/samples/.
- Must have clear fake ID patterns (e.g. FAKE-DL-XXXX, FAKE-AADHAAR-XXXX, mock watermarks/borders).
- Two images must share a person's name but differ in date of birth.
- Save expected extracted fields as a JSON file for each image in data/samples/.
- Free only, no paid tools or external image generation models. Keep code simple for students.

## Current Parent
- Conversation ID: e35c4cb9-e0bf-457f-8b67-5c1e9c1c606b
- Updated: 2026-10-10T07:39:55Z

## Investigation State
- **Explored paths**: `ORIGINAL_REQUEST.md`, `orchestrator_2/plan.md`, `data/`, `tests/`, `rto-sahayak/`
- **Key findings**:
  - Designed 4 synthetic documents: Mismatched pair (`doc1_driving_licence`, `doc2_aadhaar_card`) sharing name "Rahul Kumar Sharma" with DOB mismatch ("1995-05-15" vs "1993-05-15"). Matching pair (`doc3_pan_card`, `doc4_voter_id`) sharing identity with fuzzy name ("Priya S. Patel" vs "Priya Sanjay Patel") and date normalization ("1998-11-22" vs "22/11/1998").
  - Robust Pillow rendering architecture using pure PIL geometric primitives and safe font fallback (`load_font`) preventing runtime crashes.
  - Comprehensive JSON schemas and instances matching comparison format.
- **Unexplored areas**: None for Synthetic Image design. Ready for implementation.

## Key Decisions Made
- Paired Doc 1 (DL) & Doc 2 (Aadhaar) for DOB mismatch testing.
- Paired Doc 3 (PAN) & Doc 4 (Voter ID) for matching test with fuzzy name and alternate date format.
- Adopted 800x500 RGB dimensions with explicit banners "SYNTHETIC DOCUMENT - FOR TESTING ONLY" and "DRAFT - for citizen review and officer verification".
- Provided complete standalone Python generation script in `analysis.md` for `worker_impl_1`.

## Artifact Index
- `e:\hackthon\.agents\teamwork\m2_explorer_3\DISPATCH.md` — Incoming prompt record
- `e:\hackthon\.agents\teamwork\m2_explorer_3\BRIEFING.md` — Persistent context & state
- `e:\hackthon\.agents\teamwork\m2_explorer_3\progress.md` — Liveness & step tracking
- `e:\hackthon\.agents\teamwork\m2_explorer_3\analysis.md` — Detailed technical specifications, visual layouts, schemas, and generator script
- `e:\hackthon\.agents\teamwork\m2_explorer_3\handoff.md` — 5-component handoff report for orchestrator
