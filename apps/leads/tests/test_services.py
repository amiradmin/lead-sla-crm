"""
Lead model tests.
"""

import pytest
from django.utils import timezone

from datetime import timedelta

from apps.leads.models import Lead, ContactAttempt
from apps.leads.enums import (
    LeadSource,
    LeadStatus,
    ContactChannel,
    ContactOutcome,
)


@pytest.mark.django_db
def test_create_lead():

    lead = Lead.objects.create(
        full_name="Amir Behvandi",
        email="amir@test.com",
        source=LeadSource.WEBSITE,
    )

    assert lead.id is not None
    assert lead.full_name == "Amir Behvandi"
    assert lead.status == LeadStatus.NEW


@pytest.mark.django_db
def test_lead_sets_sla_deadline():

    before = timezone.now()

    lead = Lead.objects.create(
        full_name="Test User",
        email="test@test.com",
        source=LeadSource.EVENT,
    )

    after = timezone.now()

    assert lead.sla_deadline is not None

    assert (
        before + timedelta(hours=24) <= lead.sla_deadline <= after + timedelta(hours=24)
    )


@pytest.mark.django_db
def test_contact_attempt_relation(
    user,
):

    lead = Lead.objects.create(
        full_name="John Smith",
        email="john@test.com",
        source=LeadSource.SOCIAL,
    )

    attempt = ContactAttempt.objects.create(
        lead=lead,
        channel=ContactChannel.CALL,
        outcome=ContactOutcome.NO_ANSWER,
        created_by=user,
    )

    assert attempt.lead == lead
    assert lead.contact_attempts.count() == 1
