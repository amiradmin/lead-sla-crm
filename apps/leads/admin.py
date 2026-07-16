"""
Common Django admin utilities.

Reusable admin classes shared across applications.
"""

from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    """
    Base admin configuration.

    Provides common fields for all models.
    """

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)


class SoftDeleteAdmin(BaseModelAdmin):
    """
    Admin configuration for soft-deletable models.
    """

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
    )

    list_filter = (
        "is_deleted",
        "created_at",
    )
