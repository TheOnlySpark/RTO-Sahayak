## 2026-10-10T07:39:55Z
You are m2_explorer_3 (Role: Synthetic Image Explorer).
Your assigned working directory is: e:\hackthon\.agents\teamwork\m2_explorer_3

Read the authoritative user request at:
e:\hackthon\.agents\teamwork\ORIGINAL_REQUEST.md (specifically the latest request timestamped 2026-10-10T07:36:23Z).
Also review the orchestrator plan at:
e:\hackthon\.agents\teamwork\orchestrator_2\plan.md

Constraints:
- You are strictly READ-ONLY. Do NOT write or modify any code files. Write only to your working directory.
- Synthetic, public or mock data only. Never ask for or store real personal data.
- Label sample documents "SYNTHETIC".
- Must use Pillow to generate 4 fake ID/certificate PNGs in data/samples/.
- Must have clear fake ID patterns (e.g. FAKE-DL-XXXX, FAKE-AADHAAR-XXXX, mock watermarks/borders).
- Two images must share a person's name but differ in date of birth.
- Save expected extracted fields as a JSON file for each image in data/samples/.

Your tasks:
1. Design the 4 synthetic ID documents:
   - What document types? (e.g., Driving Licence, Aadhaar Card / Identity Card, Voter ID, Birth Certificate / School Leaving Certificate).
   - Details for each: Name, DOB, Document Number, Address/Father's Name, Issue Date.
   - Crucial requirement: Two images MUST share a person's name (e.g. "Rahul Kumar Sharma") but differ in DOB (e.g. "1995-05-15" vs "1993-05-15").
   - The other two documents (e.g., a matching pair or distinct docs).
2. Design the visual layout and text rendering using Pillow (Image, ImageDraw, ImageFont):
   - Banner: "SYNTHETIC" prominent banner.
   - "DRAFT - for citizen review and officer verification" or "SYNTHETIC DOCUMENT - FOR TESTING ONLY".
   - Watermark / border / badge patterns.
   - Fallback font handling (PIL's ImageFont.load_default() or common system truetype fonts).
3. Design the JSON schema for expected extracted fields for each of the 4 images.
4. Provide a complete, robust generation script architecture that can run stand-alone or via python script.

Output:
Write a comprehensive report to e:\hackthon\.agents\teamwork\m2_explorer_3\handoff.md.
When done, send a message back to caller (parent) using send_message with your completion summary.
