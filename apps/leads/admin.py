"""
Admin configuration for leads application.
"""

from django.contrib import admin

from apps.leads.models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Lead model.
    """

    list_display = (
        "first_name",
        "last_name",
        "email",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
        "company",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
    )
