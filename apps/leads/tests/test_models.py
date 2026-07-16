"""
Tests for Lead models.
"""

import pytest

from apps.leads.enums import LeadStatus
from apps.leads.tests.factories import LeadFactory


@pytest.mark.django_db
def test_create_lead():

    lead = LeadFactory()

    assert lead.id is not None

    assert lead.status == LeadStatus.NEW

    assert lead.is_deleted is False


@pytest.mark.django_db
def test_soft_delete_lead():

    lead = LeadFactory()

    lead.delete()

    lead.refresh_from_db()

    assert lead.is_deleted is True

    assert lead.deleted_at is not None


@pytest.mark.django_db
def test_restore_lead():

    lead = LeadFactory()

    lead.delete()

    lead.restore()

    lead.refresh_from_db()

    assert lead.is_deleted is False

    assert lead.deleted_at is None
