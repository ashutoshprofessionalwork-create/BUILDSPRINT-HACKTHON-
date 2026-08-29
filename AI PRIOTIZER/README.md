AI Urgency Prioritization & Hyperlocal Matching ModuleOverviewThis standalone AI module prioritizes incoming emergency patient blood requests for hospital administrators and automatically matches verified cases to eligible hyperlocal donors. It combines deterministic rule-based scoring with cloud LLM semantic extraction to ensure explainability, speed, and reliability.  Core Componentsscoring.py (Rule-Based Base Engine):Blood Rarity Weighting: Awards points based on recipient group scarcity (e.g., O-: +8, AB-: +7 down to AB+: +1).  Waiting Time Penalty: Awards +1 point per elapsed hour since creation (capped dynamically) to ensure older emergencies do not starve.  Explainability Output: Returns both an integer score and an audit string explaining why points were awarded.  Cloud LLM Triage Layer (cohere):Semantic Analysis: Evaluates unstructured free-text medical notes/OPD notes without requiring strict keyword phrasing.  JSON Urgency Scoring: Classifies emergencies into CRITICAL, HIGH, MODERATE, or LOW and adds a score boost (up to +10 points).  Fallback Protection: Wraps API calls in defensive exceptions; if internet drops or API fails, base rule scores persist without breaking the server.matching.py (Hyperlocal Donor Matcher):Medical Compatibility: Enforces Red Cross blood type compatibility rules.  Hyperlocal Match: Filters strictly by locality/city neighborhood.  Clinical Cooldown: Checks that the donor's last donation date is $\ge 90$ days ago.  Status Verification: Requires verified == True and is_available == True.  How to Integrate into Django (For Backend)Sv can integrate this into Django views without altering internal models:Python# In views.py
from pipeline import run_admin_dashboard
from matching import find_match

# 1. To rank pending requests for the admin view:
# Convert Django QuerySet to list of dicts, or pass fields directly:
ranked_requests = run_admin_dashboard(pending_requests_list)

# 2. To trigger donor alerts once admin approves:
eligible_donors = find_match(approved_request_dict, all_donors_list)
Data Schema ContractsInput to Scoring (request_dict):Python{
    "blood_group_needed": "O-",          # String: Blood type[cite: 1]
    "urgency_notes": "ICU accident",     # String: Free text notes[cite: 1]
    "created_at": datetime_object        # datetime: Timestamp of submission
}
Scoring Output:Python{
    "priority_score": 21,
    "reason": "O- rarity (+8) | w8ing 3h (+3) | AI Triage: CRITICAL (trauma ICU) (+10)"
}
Input to Matcher (donor_dict):Python{
    "id": 1,
    "name": "Rohan",
    "blood_group": "O-",                 # String[cite: 1]
    "locality": "Vijay Nagar",           # String[cite: 1]
    "verified": True,                    # Boolean[cite: 1]
    "is_available": True,                # Boolean
    "last_donation_date": date_object    # datetime.date or None[cite: 1]
}
