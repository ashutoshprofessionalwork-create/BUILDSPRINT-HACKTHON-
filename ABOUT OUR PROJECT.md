# BloodBridge - Smart Emergency Blood Donation & Triage Network

BloodBridge is a full-stack emergency healthcare web platform built with Django, SQLite, and AI triage scoring. It bridges the critical response gap during medical emergencies by dynamically matching verified blood donors with patients based on clinical urgency, blood compatibility, and geographic proximity.

---

## Key Features

* **Emergency Blood Requests:** Direct patient portal enabling families and hospitals to register urgent requirements with condition notes, required blood groups, and hospital locations.
* **AI Priority Queue & Dynamic Triage:** Automated scoring engine combining rule-based heuristics with semantic clinical text processing to prioritize ICU, trauma, and surgical cases in real time.
* **Smart Donor Compatibility Matching:** Instant donor matching algorithms that filter by ABO/Rh blood compatibility, geographic locality, verified donor status, and cooldown windows since previous donations.
* **Admin Verification & Action Center:** Built-in portal enabling hospital administrators to audit incoming cases, verify emergency status, and trigger matched donor callouts.
* **Live Urgent Cases Board:** Homepage broadcast of active, verified patient requirements to drive rapid volunteer mobilization across localities.

---

## Tech Stack

* **Backend Framework:** Django 6.x (Python)
* **Database:** SQLite (`db.sqlite3`)
* **AI & Urgent Triage Processing:** Semantic Urgency Extraction, Heuristic Priority Engine, SkillPatch Medical Audit API
* **Frontend:** HTML5, CSS3, Bootstrap 5, Bootstrap Icons, FontAwesome
