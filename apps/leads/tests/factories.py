"""
Factories for generating test data.
"""

import factory

from apps.leads.enums import LeadStatus
from apps.leads.models import Lead


class LeadFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Lead instances.
    """

    class Meta:
        model = Lead

    first_name = factory.Faker("first_name")

    last_name = factory.Faker("last_name")

    email = factory.Faker("email")

    phone = factory.Faker("phone_number")

    company = factory.Faker("company")

    status = LeadStatus.NEW

    notes = factory.Faker("sentence")
