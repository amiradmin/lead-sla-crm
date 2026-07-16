"""
Business logic for leads.
"""

from django.db import transaction
from django.utils import timezone

from apps.leads.enums import (
    ContactOutcome,
    LeadStatus,
)
from apps.leads.models import (
    ContactAttempt,
    Lead,
)


@transaction.atomic
def create_lead(**data):
    """
    Create lead.

    SLA:
    created_at + 24 hours
    """

    lead = Lead.objects.create(
        **data,
    )

    return lead


@transaction.atomic
def update_lead(
    lead,
    data,
):
    """
    Update lead.
    """

    for key, value in data.items():
        setattr(
            lead,
            key,
            value,
        )

    lead.save()

    return lead


@transaction.atomic
def delete_lead(lead):
    """
    Soft delete.
    """

    lead.delete()


@transaction.atomic
def restore_lead(lead):
    """
    Restore deleted lead.
    """

    lead.restore()

    return lead


@transaction.atomic
def assign_lead(
    lead,
    advisor,
):
    """
    Assign advisor.

    Rules:
    Only NEW or ASSIGNED allowed.
    """

    lead = Lead.objects.select_for_update().get(id=lead.id)

    if lead.status not in [
        LeadStatus.NEW,
        LeadStatus.ASSIGNED,
    ]:
        raise ValueError("Only NEW or ASSIGNED leads can be assigned.")

    lead.assigned_advisor = advisor
    lead.status = LeadStatus.ASSIGNED

    lead.save()

    return lead


@transaction.atomic
def create_contact_attempt(
    lead,
    created_by,
    **data,
):
    """
    Create contact attempt.

    Rules:
    - Only ASSIGNED or CONTACTED
    - First REACHED updates first_contacted_at
    """

    lead = Lead.objects.select_for_update().get(id=lead.id)

    if lead.status not in [
        LeadStatus.ASSIGNED,
        LeadStatus.CONTACTED,
    ]:
        raise ValueError("Lead cannot receive contact attempts.")

    attempt = ContactAttempt.objects.create(
        lead=lead,
        created_by=created_by,
        **data,
    )

    if data["outcome"] == ContactOutcome.REACHED and lead.first_contacted_at is None:
        lead.first_contacted_at = timezone.now()
        lead.status = LeadStatus.CONTACTED

        lead.save()

    return attempt


@transaction.atomic
def convert_lead(lead):
    """
    Convert lead.

    Only CONTACTED allowed.
    """

    lead = Lead.objects.select_for_update().get(id=lead.id)

    if lead.status != LeadStatus.CONTACTED:
        raise ValueError("Only CONTACTED leads can be converted.")

    lead.status = LeadStatus.CONVERTED
    lead.converted_at = timezone.now()

    lead.save()

    return lead
