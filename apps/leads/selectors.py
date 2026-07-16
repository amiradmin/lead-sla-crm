"""
Database query functions for the leads application.

Selectors contain only read operations.
Business logic should stay inside services.py.
"""

from apps.leads.models import Lead


def get_leads():
    """
    Return all active leads.

    Returns:
        QuerySet:
            Active Lead objects.
    """

    return Lead.objects.all()


def get_lead_by_id(
    lead_id,
):
    """
    Retrieve an active lead by ID.

    Args:
        lead_id:
            UUID of the lead.

    Returns:
        Lead instance or None.
    """

    return Lead.objects.filter(
        id=lead_id,
    ).first()


def get_deleted_lead_by_id(
    lead_id,
):
    """
    Retrieve a soft deleted lead.

    Args:
        lead_id:
            UUID of the lead.

    Returns:
        Deleted Lead instance or None.
    """

    return Lead.all_objects.filter(
        id=lead_id,
    ).first()
