"""
Global pytest configuration.

Provides shared fixtures for project tests.
"""

import os

import django
import pytest


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings.local",
)


django.setup()


from apps.leads.tests.factories import LeadFactory  # noqa: E402


@pytest.fixture
def lead_factory():
    """
    Provide Lead factory.
    """

    return LeadFactory
