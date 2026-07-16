"""
Database queries for leads.

No business logic here.
"""

from django.utils import timezone

from apps.leads.models import Lead


def get_leads():
    """
    Return active leads only.
    """

    return Lead.objects.filter(
        deleted_at__isnull=True,
    )


def get_lead_by_id(pk):
    """
    Get active lead.
    """

    return Lead.objects.filter(
        id=pk,
        deleted_at__isnull=True,
    ).first()


def get_deleted_lead_by_id(pk):
    """
    Get soft deleted lead.
    """

    return Lead.objects.filter(
        id=pk,
        deleted_at__isnull=False,
    ).first()


def get_overdue_leads():
    """
    Return SLA breached leads.
    """

    return Lead.objects.filter(
        status__in=[
            "new",
            "assigned",
        ],
        sla_deadline__lt=timezone.now(),
        first_contacted_at__isnull=True,
        deleted_at__isnull=True,
    )
