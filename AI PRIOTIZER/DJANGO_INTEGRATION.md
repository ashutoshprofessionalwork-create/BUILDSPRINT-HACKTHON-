**Input Data Shapes**
{
    "id": 102,
    "patient_name": "Aakash Verma",
    "blood_group_needed": "O-",
    "locality": "Vijay Nagar",
    "urgency_notes": "Severe accident trauma patient in ICU",
    "created_at": datetime.datetime.now() - datetime.timedelta(hours=3)
}

**Donor Pool Dictionary / Model Representation:**
{
    "id": 1,
    "name": "Rohan Sharma",
    "phone": "9876543210",
    "blood_group": "O-",
    "locality": "Vijay Nagar",
    "verified": True,
    "is_available": True,
    "last_donation_date": datetime.date.today() - datetime.timedelta(days=120)
}
**Output Contracts
Scoring Output:**
{
    "priority_score": 21,
    "reason": "O- rarity (+8) | w8ing 3h (+3) | AI Triage: CRITICAL (trauma ICU) (+10)"
}

**Matched Donors Output:**
[
    {
        "donot_id": 1,
        "name": "Rohan Sharma",
        "phone": "9876543210",
        "blood_group": "O-",
        "locality": "Vijay Nagar"
    }
]

**Backend Usage in Django Views**
from pipeline import run_admin_dashboard
from matching import find_match

# 1. Admin Dashboard View: Fetch pending requests and auto-sort by priority
def admin_dashboard_view(request):
    # Convert Django Queryset to a list of dicts (or map attributes)
    pending_list = list(PatientRequest.objects.filter(status="Pending").values())
    ranked_requests = run_admin_dashboard(pending_list)
    return render(request, "admin_dashboard.html", {"requests": ranked_requests})

# 2. Approval Action: Trigger matching for the top-priority request
def approve_request_view(request, request_id):
    patient_req = PatientRequest.objects.get(id=request_id)
    donor_pool = list(DonorProfile.objects.filter(is_available=True, verified=True).values())
    
    # Run matching logic
    matched_donors = find_match(patient_req.__dict__, donor_pool)
    
    # Create notification/alert entries for matched donors
    for donor in matched_donors:
        Alert.objects.create(donor_id=donor["donot_id"], request=patient_req)




