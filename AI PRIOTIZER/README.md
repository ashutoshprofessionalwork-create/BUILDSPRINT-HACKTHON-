# AI-Powered Hyperlocal Blood Donation & Emergency Matching System

A real-time, locality-based emergency blood donation platform designed to solve the last-mile coordination problem during medical crises[cite: 1].

---

## The Problem
In urban healthcare setups, critical blood shortages are predominantly coordination failures rather than absolute scarcity[cite: 1]. Existing portals like e-RaktKosh manage high-level inventory data, but lack real-time, hyperlocal emergency coordination connecting patients, eligible donors, and hospital administrators[cite: 1].

---

## Core Architecture & Workflow

1. **Patient Request:** A patient or family member logs an emergency request with hospital/locality details, blood group, urgency notes, and medical proof[cite: 1].
2. **Admin Verification & AI Prioritization:** Hospital admins review the queue[cite: 1]. Requests are dynamically ranked using an AI urgency score (accounting for blood rarity, elapsed wait time, and clinical urgency extracted via LLM triage)[cite: 1].
3. **Hyperlocal Match Engine:** Once approved by an admin, the system queries the verified donor pool against standard blood compatibility, locality, and the mandatory 90-day cooldown window[cite: 1].
4. **Donor Notification:** Matched, eligible donors receive in-app emergency alerts to accept or decline the request[cite: 1].

---

## Tech Stack

* **Backend & Database:** Python 3, Django, SQLite[cite: 1]
* **Frontend:** Bootstrap, HTML5/CSS, Vanilla JS[cite: 1]
* **AI Prioritization:** Rule-based weighting engine + Cohere Cloud LLM (`command-r`) for free-text medical triage[cite: 1]

---

## System Modules & Responsibilities

* **`scoring.py` (Ashu):** Standalone priority engine calculating baseline urgency via rarity tables, wait-time decay, and keyword parsing[cite: 1].
* **`llm_urgency.py` / Cloud Integration (Ashu & Sher):** Extracts structured urgency levels and boosts scores from patient notes via cloud LLM inference[cite: 1].
* **`matching.py` (Ashu & Sv):** Compatibility matrix, geographic locality filtering, and 90-day donation cooldown validation[cite: 1].
* **Django Models & Auth (Sv):** Custom user architecture managing 3 distinct roles (Donor, Patient, Admin)[cite: 1].
* **UI Templates (Anshika):** Responsive Bootstrap templates for dashboards, alert cards, and request submission forms[cite: 1].
* **Pitch Deck & Testing (Sher):** End-to-end edge-case validation, prompt testing, and final presentation[cite: 1].

---

## Local Setup & Execution

### 1. Prerequisites
* Python 3.10+ installed
* Cohere API key

### 2. Install Dependencies
```bash
pip install -r requirements.txt
# or install directly:
pip install django cohere
