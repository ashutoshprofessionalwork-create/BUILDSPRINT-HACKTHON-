import datetime
import json
import re
import cohere

# Import your two working functions
from scoring import priority_score
from matching import find_match

# Initialize Cohere Client
COHERE_API_KEY = "cohere_dx8d4pfSVaNwwNmQTd2725GcdzeAJT3VbcOehSvX492Xzn"  # Replace with your key securely
co = cohere.Client(COHERE_API_KEY)


def extract_cohere_urgency(notes: str) -> dict:
    if not notes or not notes.strip():
        return {"score_boost": 0, "reason_tag": ""}

    prompt = (
        f"Analyze these emergency patient notes: '{notes}'.\n"
        "Return ONLY a JSON object: "
        '{"urgency_level": "CRITICAL", "score_boost": 10, "detected_condition": "trauma ICU"}'
    )

    try:
        # Use v2 chat endpoint or standard command-r
        response = co.chat(
            model="command-r-08-2024",
            message=prompt,
            temperature=0.1
        )
        
        # Get raw response text
        raw_text = response.text.strip()
        
        # Strip markdown ```json ... ```
        if "```" in raw_text:
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:].strip()
                
        data = json.loads(raw_text)
        boost = int(data.get("score_boost", 0))
        level = data.get("urgency_level", "URGENT")
        cond = data.get("detected_condition", "Medical Need")
        
        return {
            "score_boost": boost,
            "reason_tag": f"AI Triage: {level} ({cond}) (+{boost})"
        }
    except Exception as e:
        # PRINT THE EXACT ERROR SO WE CAN SEE WHY IT SKIPS
        print(f"[COHERE ERROR DEBUG]: {type(e).__name__} -> {e}")
        return {"score_boost": 0, "reason_tag": ""}

def run_admin_dashboard(pending_requests: list) -> list:
    """
    Ranks all pending requests for the admin dashboard.
    Combines rule-based priority score with Cohere cloud LLM analysis.
    """
    for req in pending_requests:
        # 1. Base rule-based score
        res = priority_score(
            blood_req=req.get("blood_group_needed", ""),
            notes=req.get("urgency_notes", ""),
            created_at=req.get("created_at")
        )
        
        # 2. Cloud LLM urgency boost
        llm_res = extract_cohere_urgency(req.get("urgency_notes", ""))
        
        # Combine scores and explainability reasons
        final_score = res["score"] + llm_res["score_boost"]
        reasons = [res["reason"]]
        if llm_res["reason_tag"]:
            reasons.append(llm_res["reason_tag"])
            
        req["priority_score"] = final_score
        req["reason"] = " | ".join(reasons)

    # Sort in descending order (highest score first)
    pending_requests.sort(key=lambda x: x["priority_score"], reverse=True)
    return pending_requests


# --- FULL END-TO-END TEST RUN ---
if __name__ == "__main__":
    now = datetime.datetime.now()

    # 1. Incoming unranked patient requests
    mock_requests = [
        {
            "id": 101,
            "patient_name": "Rajesh Kumar",
            "blood_group_needed": "B+",
            "locality": "Vijay Nagar",
            "urgency_notes": "Routine elective knee surgery next week",
            "created_at": now - datetime.timedelta(hours=1)
        },
        {
            "id": 102,
            "patient_name": "Aakash Verma",
            "blood_group_needed": "O-",
            "locality": "Vijay Nagar",
            "urgency_notes": "Severe accident trauma patient in ICU",
            "created_at": now - datetime.timedelta(hours=3)
        },
        {
            "id": 103,
            "patient_name": "Sunita Sharma",
            "blood_group_needed": "A+",
            "locality": "Palasia",
            "urgency_notes": "Emergency surgery required",
            "created_at": now - datetime.timedelta(minutes=30)
        }
    ]

    # 2. Donor pool in the system
    today = datetime.date.today()
    mock_donors = [
        {"id": 1, "name": "Rohan", "phone": "9876543210", "blood_group": "O-", "locality": "Vijay Nagar", "verified": True, "is_available": True, "last_donation_date": today - datetime.timedelta(days=120)},
        {"id": 2, "name": "Aman", "phone": "9876543211", "blood_group": "B+", "locality": "Vijay Nagar", "verified": True, "is_available": True, "last_donation_date": None},
        {"id": 3, "name": "Deepak", "phone": "9876543212", "blood_group": "O-", "locality": "Vijay Nagar", "verified": False, "is_available": True, "last_donation_date": None}, # Unverified
    ]

    print("=== STEP 1: ADMIN DASHBOARD (RANKED BY PRIORITY) ===")
    ranked_requests = run_admin_dashboard(mock_requests)
    for r in ranked_requests:
        print(f"[{r['priority_score']} pts] {r['patient_name']} ({r['blood_group_needed']}) - {r['locality']}")
        print(f"       Reason: {r['reason']}\n")

    print("=== STEP 2: ADMIN APPROVES TOP REQUEST ===")
    top_request = ranked_requests[0]
    print(f"Approved Request #{top_request['id']} for {top_request['patient_name']}")

    print("\n=== STEP 3: MATCHING DONORS FOUND FOR ALERTS ===")
    matched = find_match(top_request, mock_donors)
    for m in matched:
        print(f"Alerting: {m['name']} ({m['blood_group']}) | Locality: {m['locality']} | Phone: {m['phone']}")