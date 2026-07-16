"""
Database models for the leads application.
"""

from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.common.models import SoftDeleteModel
from apps.leads.enums import (
    ContactChannel,
    ContactOutcome,
    LeadSource,
    LeadStatus,
)


class Lead(SoftDeleteModel):
    """
    Represents an inbound customer lead.

    A lead must be contacted within the SLA window.
    """

    full_name = models.CharField(
        max_length=255,
    )

    email = models.EmailField(
        unique=True,
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    source = models.CharField(
        max_length=20,
        choices=LeadSource.choices,
        db_index=True,
    )

    status = models.CharField(
        max_length=20,
        choices=LeadStatus.choices,
        default=LeadStatus.NEW,
        db_index=True,
    )

    assigned_advisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_leads",
    )

    sla_deadline = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    first_contacted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    converted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = [
            "-created_at",
        ]

    def save(
        self,
        *args,
        **kwargs,
    ):
        """
        SLA rule:
        New leads get 24 hour deadline.
        """

        if self._state.adding:
            self.sla_deadline = timezone.now() + timedelta(hours=24)

        super().save(
            *args,
            **kwargs,
        )

    def __str__(self):
        return self.full_name


class ContactAttempt(SoftDeleteModel):
    """
    Represents a lead contact attempt.
    """

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="contact_attempts",
    )

    channel = models.CharField(
        max_length=20,
        choices=ContactChannel.choices,
    )

    outcome = models.CharField(
        max_length=20,
        choices=ContactOutcome.choices,
    )

    notes = models.TextField(
        blank=True,
    )

    attempted_at = models.DateTimeField(
        default=timezone.now,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="contact_attempts",
    )

    class Meta:
        ordering = [
            "-attempted_at",
        ]

    def __str__(self):
        return f"{self.lead.full_name} - {self.outcome}"
