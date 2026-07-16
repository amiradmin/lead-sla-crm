"""
Lead API tests.
"""

import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.leads.models import Lead

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="amir",
        password="123456",
    )


@pytest.fixture
def api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def lead(db):
    return Lead.objects.create(
        full_name="Existing Lead",
        email="lead@test.com",
        source="website",
    )


@pytest.mark.django_db
def test_list_leads(api_client, lead):
    response = api_client.get("/api/leads/")

    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_create_lead(api_client):
    payload = {
        "full_name": "Amir Behvandi",
        "email": "amir2@test.com",
        "source": "website",
    }

    response = api_client.post(
        "/api/leads/",
        payload,
        format="json",
    )

    assert response.status_code == 201
    assert response.data["full_name"] == payload["full_name"]


@pytest.mark.django_db
def test_assign_lead(api_client, lead, user):
    response = api_client.post(
        f"/api/leads/{lead.id}/assign/",
        {
            "assigned_advisor": user.id,
        },
        format="json",
    )

    assert response.status_code == 200
    assert response.data["status"] == "assigned"


@pytest.mark.django_db
def test_contact_lead(api_client, lead, user):
    api_client.post(
        f"/api/leads/{lead.id}/assign/",
        {
            "assigned_advisor": user.id,
        },
        format="json",
    )

    response = api_client.post(
        f"/api/leads/{lead.id}/contact/",
        {
            "channel": "call",
            "outcome": "reached",
            "notes": "Talked to customer",
        },
        format="json",
    )

    assert response.status_code == 201
    assert "id" in response.data


@pytest.mark.django_db
def test_convert_lead(api_client, lead, user):
    api_client.post(
        f"/api/leads/{lead.id}/assign/",
        {
            "assigned_advisor": user.id,
        },
        format="json",
    )

    api_client.post(
        f"/api/leads/{lead.id}/contact/",
        {
            "channel": "call",
            "outcome": "reached",
            "notes": "Interested",
        },
        format="json",
    )

    response = api_client.post(
        f"/api/leads/{lead.id}/convert/",
    )

    assert response.status_code == 200
    assert response.data["status"] == "converted"
