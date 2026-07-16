"""
Database models for the leads application.

This module contains business entities related
to customer leads.
"""

from django.db import models

from apps.common.models import SoftDeleteModel
from apps.leads.enums import LeadStatus


class Lead(SoftDeleteModel):
    """
    Represents a potential customer.

    A lead contains contact information and
    lifecycle status.
    """

    first_name = models.CharField(
        max_length=100,
        help_text="Lead first name.",
    )

    last_name = models.CharField(
        max_length=100,
        help_text="Lead last name.",
    )

    email = models.EmailField(
        unique=True,
        help_text="Lead email address.",
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        help_text="Lead phone number.",
    )

    company = models.CharField(
        max_length=255,
        blank=True,
        help_text="Company associated with the lead.",
    )

    status = models.CharField(
        max_length=20,
        choices=LeadStatus.choices,
        default=LeadStatus.NEW,
        db_index=True,
        help_text="Current lead lifecycle status.",
    )

    notes = models.TextField(
        blank=True,
        help_text="Additional notes about the lead.",
    )

    class Meta:
        """
        Django model configuration.
        """

        ordering = [
            "-created_at",
        ]

        verbose_name = "Lead"

        verbose_name_plural = "Leads"

    def __str__(self) -> str:
        """
        Return human readable representation.
        """

        return f"{self.first_name} {self.last_name}"
