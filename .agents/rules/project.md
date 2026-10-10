---
trigger: always_on
---

# RTO Sahayak rules
- This is a Gen AI AGENT: Gemini decides when to call tools. Do not replace
  it with a fixed if/else flow.
- Synthetic, public or mock data only. Never ask for or store real personal
  data. Label sample documents "SYNTHETIC".
- Never decide eligibility, give legal guarantees, claim to be an RTO officer,
  or say anything was submitted to a government system. Explain, check, draft.
- Every rule explanation cites its source file and ends with:
  "Final decision rests with the RTO officer."
- Handoff PDFs carry the banner: "DRAFT - for citizen review and officer verification".
- Open data lives in data/open/ with its source URL and year in SOURCES.md.
  Always state the year and say it is historical statistics.
- Free only: Gemini free tier, Streamlit, local files. No Hugging Face, no paid
  services, no billing, no image/video generation models.
- Fee and rule data is PLACEHOLDER until a human verifies it.
- Max 2-3 LLM calls per user turn. Retry with backoff on 429; fall back to
  the Flash-Lite model, then to cached demo responses.
- Never hardcode, log or commit API keys. Read from .env.
- Plan first for tasks touching more than 3 files and wait for approval. Run
  tests before saying done. Never weaken a guardrail or delete a test to pass.
- Keep code small enough for a student to explain line by line.
- Terminal: no git push, no force commands, no deleting folders.
- Respect file ownership. If you need a change in a file you don't own, write
  it in HANDOFF_NOTES.md and use a stub.