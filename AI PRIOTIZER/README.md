<<<<<<< HEAD
# BUILDSPRINT-HACKTHON-
TEAM MEMBER - 
=======
# AI Priority Scoring & Hyperlocal Matching Engine

A dual-tier triage and matching engine built for the emergency blood donation platform[cite: 1]. It prioritizes unverified patient requests for hospital administrators and automatically matches approved requests to eligible nearby donors[cite: 1].

---

## 1. Architecture & Features

* **Deterministic Scoring (`scoring.py`):**
  * Calculates baseline urgency using blood group scarcity (e.g., O- = +8, AB- = +7, down to AB+ = +1)[cite: 1].
  * Adds wait-time penalties dynamically (+1 point per elapsed hour) to prevent older requests from starving[cite: 1].
  * Generates an audit string explaining why points were allocated[cite: 1].

* **Cloud LLM Triage Layer (`cohere`):**
  * Evaluates unstructured clinical free-text notes/OPD slips[cite: 1].
  * Extracts urgency level (`CRITICAL`, `HIGH`, `MODERATE`, `LOW`) and appends a score boost (up to +10 points).
  * Defensive fallback: if the API times out or fails, the system runs uninterrupted on the rule-based score.

* **Hyperlocal Matcher (`matching.py`):**
  * Matches recipients strictly against the Red Cross compatibility matrix[cite: 1].
  * Enforces neighborhood/locality matching[cite: 1].
  * Checks donor status (`verified == True`, `is_available == True`) and clinical cooldown (`last_donation_date >= 90 days ago` or `None`)[cite: 1].

---

## 2. Setup & Installation

Install the required client library:

```bash
pip install cohere
>>>>>>> d2ff81020421b5956a8e5e59199447b2c3f96de4
