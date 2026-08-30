# AI Priority Scoring & Hyperlocal Matching Engine

A dual-tier triage and matching engine built for the emergency blood donation platform. It prioritizes unverified patient requests for hospital administrators and automatically matches approved requests to eligible nearby donors.

---

## 1. Architecture & Features

* **Deterministic Scoring (`scoring.py`):**
  * Calculates baseline urgency using blood group scarcity (e.g., O- = +8, AB- = +7, down to AB+ = +1).
  * Adds wait-time penalties dynamically (+1 point per elapsed hour) to prevent older requests from starving.
  * Generates an audit string explaining why points were allocated.

* **Cloud LLM Triage Layer (`cohere`):**
  * Evaluates unstructured clinical free-text notes/OPD slips.
  * Extracts urgency level (`CRITICAL`, `HIGH`, `MODERATE`, `LOW`) and appends a score boost (up to +10 points).
  * Defensive fallback: if the API times out or fails, the system runs uninterrupted on the rule-based score.

* **Hyperlocal Matcher (`matching.py`):**
  * Matches recipients strictly against the Red Cross compatibility matrix.
  * Enforces neighborhood/locality matching.
  * Checks donor status (`verified == True`, `is_available == True`) and clinical cooldown (`last_donation_date >= 90 days ago` or `None`).

---

## 2. Setup & Installation

Install the required client library:

```bash
pip install cohere
```
