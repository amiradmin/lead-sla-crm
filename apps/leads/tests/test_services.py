"""
Tests for lead business logic services.
"""

import pytest

from apps.leads.enums import LeadStatus
from apps.leads.services import (
    change_lead_status,
    create_lead,
    delete_lead,
    restore_lead,
    update_lead,
)


@pytest.mark.django_db
class TestLeadServices:
    """
    Test lead service functions.
    """

    def test_create_lead(self):
        """
        Should create a new lead.
        """

        lead = create_lead(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            company="Example Inc",
        )

        assert lead.id is not None
        assert lead.first_name == "John"
        assert lead.status == LeadStatus.NEW

    def test_update_lead(self, lead_factory):
        """
        Should update lead information.
        """

        lead = lead_factory()

        updated = update_lead(
            lead=lead,
            data={
                "first_name": "Updated",
                "company": "New Company",
            },
        )

        assert updated.first_name == "Updated"
        assert updated.company == "New Company"

    def test_change_lead_status(self, lead_factory):
        """
        Should change lead status.
        """

        lead = lead_factory()

        updated = change_lead_status(
            lead=lead,
            status=LeadStatus.CONTACTED,
        )

        assert updated.status == LeadStatus.CONTACTED

    def test_soft_delete_lead(self, lead_factory):
        """
        Should soft delete lead.
        """

        lead = lead_factory()

        delete_lead(
            lead=lead,
        )

        lead.refresh_from_db()

        assert lead.is_deleted is True
        assert lead.deleted_at is not None

    def test_restore_deleted_lead(self, lead_factory):
        """
        Should restore deleted lead.
        """

        lead = lead_factory()

        delete_lead(
            lead=lead,
        )

        restore_lead(
            lead=lead,
        )

        lead.refresh_from_db()

        assert lead.is_deleted is False
        assert lead.deleted_at is None
