# SCORING SYSTEM
import datetime

blood_rarity = {"O-": 8, "AB-": 7, "B-": 6, "A-": 5, "O+": 4, "B+": 3, "A+": 2, "AB+": 1}
clinical_urgency = {"ICU": 4, "CRITICAL": 3, "EMERGENCY": 2, "TRAUMA": 1}
wait_time_delay = False


def priority_score(blood_req, notes, created_at=None):
    reason = []
    b = blood_rarity.get(blood_req, 0)
    reason.append(f"{blood_req.upper()} rarity (+{b})")
    u = 0
    matched_words = []
    lowered_notes = notes.lower()
    for word, points in clinical_urgency.items():
        if word in lowered_notes:
            u += points
            matched_words.append(f"{word.upper()} (+{points})")
    if matched_words:
        reason.append(f"urgency flags : {','.join(matched_words)}")
    t = 0
    if created_at:
        now = datetime.datetime.now()
        hours_pass = int((now - created_at).total_seconds() // 3600)
        t = min(hours_pass, 5)
        if t > 0:
            reason.append(f"w8ing {hours_pass}h (+{t})")
    s = int(b) + int(u) + int(t)
    return {
        "score": s,
        "reason": " | ".join(reason),
        "TOTAL_SCORE": f"{s}"
    }
