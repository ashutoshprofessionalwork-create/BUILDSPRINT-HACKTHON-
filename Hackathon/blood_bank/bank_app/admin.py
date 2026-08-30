from django.contrib import admin
from django.utils.html import format_html
from .models import UserDetail, DonorDetail, PatientDetails

admin.site.site_header = "Lifeline Administration"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Blood Bank Management"

@admin.action(description="Approve selected patient requests")
def make_approved(modeladmin, request, queryset):
    queryset.update(is_approved=True)

@admin.action(description="Unapprove selected patient requests")
def make_unapproved(modeladmin, request, queryset):
    queryset.update(is_approved=False)

@admin.register(PatientDetails)
class PatientDetailsAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'required_blood_group', 'locality', 'is_approved', 'hospital', 'condition', 'priority_queue_link')
    list_editable = ('is_approved',)
    list_filter = ('is_approved', 'required_blood_group', 'locality')
    search_fields = ('patient_name', 'patient_email', 'hospital', 'locality')
    actions = [make_approved, make_unapproved]

    def priority_queue_link(self, obj):
        return format_html(
            '<a class="button" style="background:#dc3545; color:white; padding:4px 10px; border-radius:4px; font-weight:bold; text-decoration:none;" href="{}">⚡ Open AI Queue</a>',
            '/priority-queue/'
        )
    priority_queue_link.short_description = "AI Triage"

admin.site.register(UserDetail)
admin.site.register(DonorDetail)
