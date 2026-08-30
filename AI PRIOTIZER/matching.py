<<<<<<< HEAD
import datetime

COMPATIBILITY = {
    "O-": ["O-"],
    "O+": ["O+", "O-"],
    "A-": ["A-", "O-"],
    "A+": ["A+", "A-", "O+", "O-"],
    "B-": ["B-", "O-"],
    "B+": ["B+", "B-", "O+", "O-"],
    "AB-": ["AB-", "A-", "B-", "O-"],
    "AB+": ["AB+", "AB-", "A+", "A-", "B+", "B-", "O+", "O-"]
}

def find_match(patient_req:dict, donor_pool:list):
    # filter list on the basis of locality
    matched_donor = []
    today = datetime.date.today()

    # FIX: Checked blood_group_needed to match data contract (with fallback)
    needed_blood = patient_req.get("blood_group_needed", patient_req.get("BLOOD GRP NEEDED", "")).upper()
    target_locality = patient_req.get("locality", "").strip().lower()

    allowed_grps = COMPATIBILITY.get(needed_blood, [])

    for donor in donor_pool:
        # FIX: Checked lowercase "verified" to match sample data
        if not donor.get("verified", donor.get("VERIFIED", False)):  # verified by admin 
            continue
        if not donor.get("is_available", True):  # current availability
            continue
            
        # blood compatibility check
        donor_blood = donor.get("blood_group", "")
        if donor_blood not in allowed_grps:
            continue
            
        # location check (case-insensitive)
        donor_locality = donor.get("locality", "").strip().lower()
        if donor_locality != target_locality:
            continue

        # 90 day cd
        last_donation = donor.get("last_donation_date") # expects datetime.date or None
        if last_donation:
            days_passed = (today - last_donation).days
            if days_passed < 90:
                continue # donor donated recently

        # FIX: Added missing colon ':' after "donot_id"
        matched_donor.append({
            "donot_id": donor.get("id"),
            "name": donor.get("name"),
            "phone": donor.get("phone"),
            "blood_group": donor_blood,
            "locality": donor.get("locality")
        })

    # FIX: Moved return OUTSIDE the for loop
    return matched_donor


if __name__ == "__main__":
    today = datetime.date.today()
    
    # Mock patient request
    sample_request = {
        "blood_group_needed": "B+",
        "locality": "Vijay Nagar"
    }

    # Mock donor database pool
    sample_donors = [
        # Match: B+, same locality, last donated 120 days ago
        {
            "id": 1,
            "name": "Rohan",
            "phone": "9876543210",
            "blood_group": "B+",
            "locality": "Vijay Nagar",
            "verified": True,
            "is_available": True,
            "last_donation_date": today - datetime.timedelta(days=120)
        },
        # Match: Universal donor O-, same locality, first time donor (None)
        {
            "id": 2,
            "name": "Aman",
            "phone": "9876543211",
            "blood_group": "O-",
            "locality": "Vijay Nagar",
            "verified": True,
            "is_available": True,
            "last_donation_date": None
        },
        # Fail: Incompatible blood (A+)
        {
            "id": 3,
            "name": "Pooja",
            "phone": "9876543212",
            "blood_group": "A+",
            "locality": "Vijay Nagar",
            "verified": True,
            "is_available": True,
            "last_donation_date": today - datetime.timedelta(days=100)
        },
        # Fail: Cooldown violation (donated 30 days ago)
        {
            "id": 4,
            "name": "Karan",
            "phone": "9876543213",
            "blood_group": "B+",
            "locality": "Vijay Nagar",
            "verified": True,
            "is_available": True,
            "last_donation_date": today - datetime.timedelta(days=30)
        },
        # Fail: Different locality
        {
            "id": 5,
            "name": "Suresh",
            "phone": "9876543214",
            "blood_group": "B+",
            "locality": "Palasia",
            "verified": True,
            "is_available": True,
            "last_donation_date": today - datetime.timedelta(days=150)
        }
    ]

    matches = find_match(sample_request, sample_donors)
    
    # FIX: Used "matches" variable instead of undefined "matched_donor"
    print(f"Matched {len(matches)} eligible donors:")
    for m in matches:
=======
import datetime

COMPATIBILITY = {
    "O-": ["O-"],
    "O+": ["O+", "O-"],
    "A-": ["A-", "O-"],
    "A+": ["A+", "A-", "O+", "O-"],
    "B-": ["B-", "O-"],
    "B+": ["B+", "B-", "O+", "O-"],
    "AB-": ["AB-", "A-", "B-", "O-"],
    "AB+": ["AB+", "AB-", "A+", "A-", "B+", "B-", "O+", "O-"]
}

def find_match(patient_req:dict, donor_pool:list):
    # filter list on the basis of locality
    matched_donor = []
    today = datetime.date.today()

    # FIX: Checked blood_group_needed to match data contract (with fallback)
    needed_blood = patient_req.get("blood_group_needed", patient_req.get("BLOOD GRP NEEDED", "")).upper()
    target_locality = patient_req.get("locality", "").strip().lower()

    allowed_grps = COMPATIBILITY.get(needed_blood, [])

    for donor in donor_pool:
        # FIX: Checked lowercase "verified" to match sample data
        if not donor.get("verified", donor.get("VERIFIED", False)):  # verified by admin 
            continue
        if not donor.get("is_available", True):  # current availability
            continue
            
        # blood compatibility check
        donor_blood = donor.get("blood_group", "")
        if donor_blood not in allowed_grps:
            continue
            
        # location check (case-insensitive)
        donor_locality = donor.get("locality", "").strip().lower()
        if donor_locality != target_locality:
            continue

        # 90 day cd
        last_donation = donor.get("last_donation_date") # expects datetime.date or None
        if last_donation:
            days_passed = (today - last_donation).days
            if days_passed < 90:
                continue # donor donated recently

        # FIX: Added missing colon ':' after "donot_id"
        matched_donor.append({
            "donot_id": donor.get("id"),
            "name": donor.get("name"),
            "phone": donor.get("phone"),
            "blood_group": donor_blood,
            "locality": donor.get("locality")
        })

    # FIX: Moved return OUTSIDE the for loop
    return matched_donor


if __name__ == "__main__":
    today = datetime.date.today()
    
    # Mock patient request
    sample_request = {
        "blood_group_needed": "B+",
        "locality": "Vijay Nagar"
    }

    # Mock donor database pool
    sample_donors = [
        # Match: B+, same locality, last donated 120 days ago
        {
            "id": 1,
            "name": "Rohan",
            "phone": "9876543210",
            "blood_group": "B+",
            "locality": "Vijay Nagar",
            "verified": True,
            "is_available": True,
            "last_donation_date": today - datetime.timedelta(days=120)
        },
        # Match: Universal donor O-, same locality, first time donor (None)
        {
            "id": 2,
            "name": "Aman",
            "phone": "9876543211",
            "blood_group": "O-",
            "locality": "Vijay Nagar",
            "verified": True,
            "is_available": True,
            "last_donation_date": None
        },
        # Fail: Incompatible blood (A+)
        {
            "id": 3,
            "name": "Pooja",
            "phone": "9876543212",
            "blood_group": "A+",
            "locality": "Vijay Nagar",
            "verified": True,
            "is_available": True,
            "last_donation_date": today - datetime.timedelta(days=100)
        },
        # Fail: Cooldown violation (donated 30 days ago)
        {
            "id": 4,
            "name": "Karan",
            "phone": "9876543213",
            "blood_group": "B+",
            "locality": "Vijay Nagar",
            "verified": True,
            "is_available": True,
            "last_donation_date": today - datetime.timedelta(days=30)
        },
        # Fail: Different locality
        {
            "id": 5,
            "name": "Suresh",
            "phone": "9876543214",
            "blood_group": "B+",
            "locality": "Palasia",
            "verified": True,
            "is_available": True,
            "last_donation_date": today - datetime.timedelta(days=150)
        }
    ]

    matches = find_match(sample_request, sample_donors)
    
    # FIX: Used "matches" variable instead of undefined "matched_donor"
    print(f"Matched {len(matches)} eligible donors:")
    for m in matches:
>>>>>>> d2ff81020421b5956a8e5e59199447b2c3f96de4
        print(f"- {m['name']} ({m['blood_group']}) | Phone: {m['phone']}")