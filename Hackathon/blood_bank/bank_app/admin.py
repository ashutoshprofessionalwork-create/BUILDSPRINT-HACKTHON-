
from django.contrib import admin
from django.utils.html import format_html
from .models import UserDetail, DonorDetail, PatientDetails

admin.site.site_header = "Khun Chusai Administration"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Blood Bank Management"

@admin.register(PatientDetails)
class PatientDetailsAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'required_blood_group', 'locality', 'condition', 'priority_queue_link')

    def priority_queue_link(self, obj):
        return format_html(
            '<a class="button" style="background:#dc3545; color:white; padding:4px 10px; border-radius:4px; font-weight:bold; text-decoration:none;" href="/priority-queue/">⚡ Open AI Queue</a>'
        )
    priority_queue_link.short_description = "AI Triage"

admin.site.register(UserDetail)
admin.site.register(DonorDetail)

class patient_detail_admin(admin.PatientDetails):
    