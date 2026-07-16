"""
Business logic services for the leads application.

Services contain operations that modify data
and enforce business rules.

Database queries should be implemented in selectors.py.
"""

from __future__ import annotations

from typing import Dict, Any

from django.db import transaction

from apps.leads.models import Lead
from apps.leads.enums import LeadStatus


@transaction.atomic
def create_lead(
    *,
    first_name: str,
    last_name: str,
    email: str,
    phone: str = "",
    company: str = "",
    notes: str = "",
) -> Lead:
    """
    Create a new lead.

    Args:
        first_name:
            Lead first name.

        last_name:
            Lead last name.

        email:
            Lead email address.

        phone:
            Optional phone number.

        company:
            Optional company name.

        notes:
            Additional information.

    Returns:
        Created Lead instance.
    """

    lead = Lead.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        company=company,
        notes=notes,
        status=LeadStatus.NEW,
    )

    return lead


@transaction.atomic
def update_lead(
    *,
    lead: Lead,
    data: Dict[str, Any],
) -> Lead:
    """
    Update an existing lead.

    Args:
        lead:
            Lead instance to update.

        data:
            Fields to update.

    Returns:
        Updated Lead instance.
    """

    allowed_fields = {
        "first_name",
        "last_name",
        "email",
        "phone",
        "company",
        "notes",
        "status",
    }

    for field, value in data.items():
        if field in allowed_fields:
            setattr(
                lead,
                field,
                value,
            )

    lead.save()

    return lead


@transaction.atomic
def change_lead_status(
    *,
    lead: Lead,
    status: LeadStatus,
) -> Lead:
    """
    Change lead lifecycle status.

    Business rule:
        Only valid LeadStatus values are accepted.

    Args:
        lead:
            Lead instance.

        status:
            New lifecycle status.

    Returns:
        Updated lead.
    """

    lead.status = status

    lead.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    return lead


@transaction.atomic
def delete_lead(
    *,
    lead: Lead,
) -> Lead:
    """
    Soft delete a lead.

    The database record remains available
    through all_objects manager.

    Args:
        lead:
            Lead instance.

    Returns:
        Deleted lead.
    """

    lead.delete()

    return lead


@transaction.atomic
def restore_lead(
    *,
    lead: Lead,
) -> Lead:
    """
    Restore a previously deleted lead.

    Args:
        lead:
            Soft deleted lead.

    Returns:
        Restored lead.
    """

    lead.restore()

    return lead
