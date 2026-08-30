<<<<<<< HEAD
import datetime
# scoring.py
from scoring import priority_score as priority_score
from matching import find_match

def run_admin_dashboard(pending_req: list):
    """ranks all pending REQ for the admin dashboard ."""
    for req in pending_req:
        # MODIFIED: Changed req.get("blood_grp_needed") to req.get("blood_group_needed") 
        # REASON: The team's agreed data contract specifies "blood_group_needed".
        # Kept a fallback to "blood_grp_needed" just in case.
        blood_needed = req.get("blood_group_needed") or req.get("blood_grp_needed", "")

        res = priority_score(
            blood_req=blood_needed,
            notes=req.get("urgency_notes", ""),
            created_at=req.get("created_at")
        )
        req["priority_score"] = res["score"]
        req["reason"] = res["reason"]

    pending_req.sort(key=lambda x: x["priority_score"], reverse=True)
    return pending_req


# --- MOCK TEST RUN ---
if __name__ == "__main__":
    now = datetime.datetime.now()
    today = datetime.date.today()

    # 1. Mock Patient Requests
    # MODIFIED: Renamed "blood_grp_needed" to "blood_group_needed" across all 3 mock requests
    # REASON: find_match() in matching.py specifically extracts patient_request.get("blood_group_needed").
    # When this key was "blood_grp_needed", find_match() received an empty string "" for blood type,
    # found zero allowed compatibility groups, and returned 0 matched donors!
    mock_requests = [
        {
            "id": 101,
            "patient_name": "Ramesh Gupta",
            "blood_group_needed": "B+",  # <--- MODIFIED HERE
            "locality": "Vijay Nagar",
            "urgency_notes": "Routine checkup and elective knee surgery scheduled",
            "created_at": now - datetime.timedelta(hours=1)
        },
        {
            "id": 102,
            "patient_name": "Aakash Verma",
            "blood_group_needed": "O-",  # <--- MODIFIED HERE
            "locality": "Vijay Nagar",
            "urgency_notes": "Critical accident trauma victim in ICU, immediate units required",
            "created_at": now - datetime.timedelta(hours=4)
        },
        {
            "id": 103,
            "patient_name": "Simran Kaur",
            "blood_group_needed": "A-",  # <--- MODIFIED HERE
            "locality": "Palasia",
            "urgency_notes": "Emergency surgery ongoing",
            "created_at": now - datetime.timedelta(hours=2)
        }
    ]

    # 2. Mock Donors Pool (Unchanged)
    mock_donors = [
        {
            "id": 1,
            "name": "Rohan Sharma",
            "phone": "9876543210",
            "blood_group": "O-",
            "locality": "Vijay Nagar",
            "verified": True,
            "is_available": True,
            "last_donation_date": today - datetime.timedelta(days=110)
        },
        {
            "id": 2,
            "name": "Pooja Verma",
            "phone": "9876543211",
            "blood_group": "B+",
            "locality": "Vijay Nagar",
            "verified": True,
            "is_available": True,
            "last_donation_date": today - datetime.timedelta(days=15) # Ineligible (< 90 days)
        },
        {
            "id": 3,
            "name": "Amit Patel",
            "phone": "9876543212",
            "blood_group": "O-",
            "locality": "Palasia",
            "verified": True,
            "is_available": True,
            "last_donation_date": None # First-time donor
        }
    ]

    print("--- 1. ADMIN DASHBOARD: PRIORITIZED QUEUE ---")
    ranked = run_admin_dashboard(mock_requests)
    for r in ranked:
        # MODIFIED: Changed key read to "blood_group_needed" for display
        print(f"Ranked Score: {r['priority_score']} | Patient: {r['patient_name']} ({r['blood_group_needed']})")
        print(f"Explainability: {r['reason']}\n")

    print("--- 2. ADMIN APPROVES TOP PRIORITY REQUEST ---")
    top_case = ranked[0]
    print(f"Admin approved Case #{top_case['id']} ({top_case['patient_name']})\n")

    print("--- 3. SYSTEM TRIGGERS HYPERLOCAL MATCHING ---")
    matched = find_match(top_case, mock_donors)
    print(f"Found {len(matched)} matching donor(s):")
    for d in matched:
=======
import datetime
# scoring.py
from scoring import priority_score as priority_score
from matching import find_match

def run_admin_dashboard(pending_req: list):
    """ranks all pending REQ for the admin dashboard ."""
    for req in pending_req:
        # MODIFIED: Changed req.get("blood_grp_needed") to req.get("blood_group_needed") 
        # REASON: The team's agreed data contract specifies "blood_group_needed".
        # Kept a fallback to "blood_grp_needed" just in case.
        blood_needed = req.get("blood_group_needed") or req.get("blood_grp_needed", "")

        res = priority_score(
            blood_req=blood_needed,
            notes=req.get("urgency_notes", ""),
            created_at=req.get("created_at")
        )
        req["priority_score"] = res["score"]
        req["reason"] = res["reason"]

    pending_req.sort(key=lambda x: x["priority_score"], reverse=True)
    return pending_req


# --- MOCK TEST RUN ---
if __name__ == "__main__":
    now = datetime.datetime.now()
    today = datetime.date.today()

    # 1. Mock Patient Requests
    # MODIFIED: Renamed "blood_grp_needed" to "blood_group_needed" across all 3 mock requests
    # REASON: find_match() in matching.py specifically extracts patient_request.get("blood_group_needed").
    # When this key was "blood_grp_needed", find_match() received an empty string "" for blood type,
    # found zero allowed compatibility groups, and returned 0 matched donors!
    mock_requests = [
        {
            "id": 101,
            "patient_name": "Ramesh Gupta",
            "blood_group_needed": "B+",  # <--- MODIFIED HERE
            "locality": "Vijay Nagar",
            "urgency_notes": "Routine checkup and elective knee surgery scheduled",
            "created_at": now - datetime.timedelta(hours=1)
        },
        {
            "id": 102,
            "patient_name": "Aakash Verma",
            "blood_group_needed": "O-",  # <--- MODIFIED HERE
            "locality": "Vijay Nagar",
            "urgency_notes": "Critical accident trauma victim in ICU, immediate units required",
            "created_at": now - datetime.timedelta(hours=4)
        },
        {
            "id": 103,
            "patient_name": "Simran Kaur",
            "blood_group_needed": "A-",  # <--- MODIFIED HERE
            "locality": "Palasia",
            "urgency_notes": "Emergency surgery ongoing",
            "created_at": now - datetime.timedelta(hours=2)
        }
    ]

    # 2. Mock Donors Pool (Unchanged)
    mock_donors = [
        {
            "id": 1,
            "name": "Rohan Sharma",
            "phone": "9876543210",
            "blood_group": "O-",
            "locality": "Vijay Nagar",
            "verified": True,
            "is_available": True,
            "last_donation_date": today - datetime.timedelta(days=110)
        },
        {
            "id": 2,
            "name": "Pooja Verma",
            "phone": "9876543211",
            "blood_group": "B+",
            "locality": "Vijay Nagar",
            "verified": True,
            "is_available": True,
            "last_donation_date": today - datetime.timedelta(days=15) # Ineligible (< 90 days)
        },
        {
            "id": 3,
            "name": "Amit Patel",
            "phone": "9876543212",
            "blood_group": "O-",
            "locality": "Palasia",
            "verified": True,
            "is_available": True,
            "last_donation_date": None # First-time donor
        }
    ]

    print("--- 1. ADMIN DASHBOARD: PRIORITIZED QUEUE ---")
    ranked = run_admin_dashboard(mock_requests)
    for r in ranked:
        # MODIFIED: Changed key read to "blood_group_needed" for display
        print(f"Ranked Score: {r['priority_score']} | Patient: {r['patient_name']} ({r['blood_group_needed']})")
        print(f"Explainability: {r['reason']}\n")

    print("--- 2. ADMIN APPROVES TOP PRIORITY REQUEST ---")
    top_case = ranked[0]
    print(f"Admin approved Case #{top_case['id']} ({top_case['patient_name']})\n")

    print("--- 3. SYSTEM TRIGGERS HYPERLOCAL MATCHING ---")
    matched = find_match(top_case, mock_donors)
    print(f"Found {len(matched)} matching donor(s):")
    for d in matched:
>>>>>>> d2ff81020421b5956a8e5e59199447b2c3f96de4
        print(f"-> Alert sent to: {d['name']} | Blood: {d['blood_group']} | Locality: {d['locality']} | Phone: {d['phone']}")