"""
Global pytest configuration.

Provides shared fixtures for project tests.
"""

import pytest

from django.contrib.auth import get_user_model

from apps.leads.models import Lead

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="amir",
        password="123456",
    )


@pytest.fixture
def lead(db):
    return Lead.objects.create(
        full_name="Existing Lead",
        email="lead@test.com",
        source="website",
    )
