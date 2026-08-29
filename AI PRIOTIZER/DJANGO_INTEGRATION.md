# Django Integration Guide: Priority Scoring & Hyperlocal Matching

This guide covers plugging the AI priority scoring and donor matching engine directly into the Django backend.

---

## 1. Project Directory Structure

Place `scoring.py` and `matching.py` inside the primary Django app directory (e.g., `core/`):

```text
myproject/
│
├── core/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── scoring.py      <-- AI scoring script
│   └── matching.py     <-- Matching script
│
├── templates/
│   ├── admin_dashboard.html
│   └── donor_alerts.html
│
├── manage.py
└── myproject/
    ├── settings.py
    └── urls.py

from django.db import models
from django.contrib.auth.models import User

# Blood group choices
BLOOD_GROUP_CHOICES = [
    ('O-', 'O-'), ('O+', 'O+'),
    ('A-', 'A-'), ('A+', 'A+'),
    ('B-', 'B-'), ('B+', 'B+'),
    ('AB-', 'AB-'), ('AB+', 'AB+'),
]

--------------------------------------------------------------------------------


# 1. Donor Profile Model
class DonorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donor_profile')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    locality = models.CharField(max_length=100)
    last_donation_date = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.blood_group}) - {self.locality}"

# 2. Patient Blood Request Model
class PatientRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Fulfilled', 'Fulfilled'),
        ('Rejected', 'Rejected'),
    ]

    patient_name = models.CharField(max_length=100)
    blood_group_needed = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    locality = models.CharField(max_length=100)
    urgency_notes = models.TextField(help_text="Clinical notes, OPD summary, or reason")
    proof_file = models.FileField(upload_to='proofs/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Req #{self.id}: {self.patient_name} ({self.blood_group_needed})"

# 3. In-App Alert Model for Matched Donors
class DonorAlert(models.Model):
    ALERT_STATUS = [
        ('Sent', 'Sent'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
    ]

    donor = models.ForeignKey(DonorProfile, on_delete=models.CASCADE, related_name='alerts')
    request = models.ForeignKey(PatientRequest, on_delete=models.CASCADE, related_name='alerts')
    status = models.CharField(max_length=20, choices=ALERT_STATUS, default='Sent')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert to {self.donor.name} for Req #{self.request.id}"


python manage.py makemigrations
python manage.py migrate


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import PatientRequest, DonorProfile, DonorAlert
from .scoring import priority_score
from .matching import find_match

# 1. ADMIN VIEW: Show pending requests auto-sorted by AI priority
def admin_dashboard(request):
    """
    Ranks all pending requests using priority_score before rendering.
    """
    pending_queryset = PatientRequest.objects.filter(status='Pending')
    ranked_requests = []

    for req in pending_queryset:
        # Run scoring logic on each record
        result = priority_score(
            blood_req=req.blood_group_needed,
            notes=req.urgency_notes,
            created_at=req.created_at
        )

        # Attach calculated properties dynamically without modifying DB schema
        req.priority_score = result["score"]
        req.priority_reason = result["reason"]
        ranked_requests.append(req)

    # Sort descending by priority score (highest urgency first)
    ranked_requests.sort(key=lambda x: x.priority_score, reverse=True)

    context = {
        'requests': ranked_requests
    }
    return render(request, 'admin_dashboard.html', context)


# 2. ADMIN ACTION: Approve request and trigger donor matching
def approve_and_match(request, request_id):
    """
    Approves a patient request and triggers matching against verified donors.
    """
    patient_req = get_object_or_404(PatientRequest, id=request_id)
    patient_req.status = 'Approved'
    patient_req.save()

    # Build patient dictionary expected by matching.py
    req_dict = {
        "blood_group_needed": patient_req.blood_group_needed,
        "locality": patient_req.locality
    }

    # Fetch eligible, verified donor pool
    donor_queryset = DonorProfile.objects.filter(is_available=True, verified=True)
    donor_pool = []
    for d in donor_queryset:
        donor_pool.append({
            "id": d.id,
            "name": d.name,
            "phone": d.phone,
            "blood_group": d.blood_group,
            "locality": d.locality,
            "verified": d.verified,
            "is_available": d.is_available,
            "last_donation_date": d.last_donation_date
        })

    # Run matching logic
    matched_donors = find_match(req_dict, donor_pool)

    # Create in-app alerts for matched donors
    alerts_created = 0
    for donor_data in matched_donors:
        donor_instance = DonorProfile.objects.get(id=donor_data["donot_id"])
        # Avoid duplicate alerts
        DonorAlert.objects.get_or_create(
            donor=donor_instance,
            request=patient_req,
            defaults={'status': 'Sent'}
        )
        alerts_created += 1

    messages.success(request, f"Request #{patient_req.id} approved! Alerted {alerts_created} eligible donors.")
    return redirect('admin_dashboard')


# 3. DONOR VIEW: View incoming matched emergency alerts
def donor_alerts(request, donor_id):
    """
    Displays active alerts sent to a specific donor.
    """
    donor = get_object_or_404(DonorProfile, id=donor_id)
    alerts = DonorAlert.objects.filter(donor=donor).order_by('-created_at')

    context = {
        'donor': donor,
        'alerts': alerts
    }
    return render(request, 'donor_alerts.html', context)


# 4. DONOR ACTION: Accept or Decline request
def update_alert_status(request, alert_id, action):
    """
    Updates the alert action taken by the donor.
    """
    alert = get_object_or_404(DonorAlert, id=alert_id)
    if action in ['Accepted', 'Declined']:
        alert.status = action
        alert.save()
        messages.info(request, f"Alert marked as {action}.")
    return redirect('donor_alerts', donor_id=alert.donor.id)


from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve/<int:request_id>/', views.approve_and_match, name='approve_and_match'),
    path('donor/<int:donor_id>/alerts/', views.donor_alerts, name='donor_alerts'),
    path('alert/<int:alert_id>/<str:action>/', views.update_alert_status, name='update_alert_status'),
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hospital Admin - Prioritized Blood Requests</title>
    <link rel="stylesheet" href="[https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css](https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css)">
</head>
<body class="bg-light p-4">
    <div class="container">
        <h2 class="mb-4">Pending Emergency Requests (AI Prioritized)</h2>
        
        {% if messages %}
            {% for msg in messages %}
                <div class="alert alert-success">{{ msg }}</div>
            {% endfor %}
        {% endif %}

        <div class="table-responsive bg-white rounded shadow-sm p-3">
            <table class="table table-hover align-middle">
                <thead class="table-dark">
                    <tr>
                        <th>Rank / Score</th>
                        <th>Patient</th>
                        <th>Blood Needed</th>
                        <th>Locality</th>
                        <th>AI Triage & Urgency Reason</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {% for req in requests %}
                    <tr>
                        <td>
                            <span class="badge bg-danger fs-6">{{ req.priority_score }} pts</span>
                        </td>
                        <td><strong>{{ req.patient_name }}</strong></td>
                        <td><span class="badge bg-primary">{{ req.blood_group_needed }}</span></td>
                        <td>{{ req.locality }}</td>
                        <td>
                            <small class="text-muted d-block">{{ req.urgency_notes }}</small>
                            <span class="text-danger fw-semibold">{{ req.priority_reason }}</span>
                        </td>
                        <td>
                            <a href="{% url 'approve_and_match' req.id %}" class="btn btn-sm btn-success">Approve & Alert</a>
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="6" class="text-center py-4 text-muted">No pending requests in queue.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Donor Alerts - {{ donor.name }}</title>
    <link rel="stylesheet" href="[https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css](https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css)">
</head>
<body class="bg-light p-4">
    <div class="container" style="max-width: 750px;">
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h3>Alerts for {{ donor.name }}</h3>
            <span class="badge bg-secondary">{{ donor.blood_group }} | {{ donor.locality }}</span>
        </div>

        {% if messages %}
            {% for msg in messages %}
                <div class="alert alert-info">{{ msg }}</div>
            {% endfor %}
        {% endif %}

        {% for alert in alerts %}
            <div class="card mb-3 shadow-sm border-start border-danger border-4">
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                        <h5 class="card-title text-danger">Emergency Blood Request</h5>
                        <span class="badge {% if alert.status == 'Accepted' %}bg-success{% elif alert.status == 'Declined' %}bg-secondary{% else %}bg-warning text-dark{% endif %}">
                            {{ alert.status }}
                        </span>
                    </div>
                    <p class="card-text mb-1">
                        <strong>Patient:</strong> {{ alert.request.patient_name }} <br>
                        <strong>Blood Group:</strong> {{ alert.request.blood_group_needed }} <br>
                        <strong>Hospital / Locality:</strong> {{ alert.request.locality }} <br>
                        <strong>Notes:</strong> {{ alert.request.urgency_notes }}
                    </p>
                    <small class="text-muted">Received: {{ alert.created_at|timesince }} ago</small>
                    
                    {% if alert.status == 'Sent' %}
                        <div class="mt-3">
                            <a href="{% url 'update_alert_status' alert.id 'Accepted' %}" class="btn btn-sm btn-success me-2">Accept Donation</a>
                            <a href="{% url 'update_alert_status' alert.id 'Declined' %}" class="btn btn-sm btn-outline-secondary">Decline</a>
                        </div>
                    {% endif %}
                </div>
            </div>
        {% empty %}
            <div class="alert alert-light text-center">No current emergency alerts.</div>
        {% endfor %}
    </div>
</body>
</html>
