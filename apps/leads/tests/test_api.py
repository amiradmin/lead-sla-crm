"""
API tests for leads application.
"""

import pytest

from rest_framework.test import APIClient

from apps.leads.models import Lead


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestLeadAPI:
    """
    Test lead REST endpoints.
    """

    def test_list_leads(
        self,
        api_client,
        lead_factory,
    ):
        """
        GET /api/leads/
        """

        lead_factory()

        response = api_client.get(
            "/api/leads/",
        )

        assert response.status_code == 200
        assert len(response.data) == 1

    def test_create_lead(
        self,
        api_client,
    ):
        """
        POST /api/leads/
        """

        payload = {
            "first_name": "Amir",
            "last_name": "Behvandi",
            "email": "amir@test.com",
            "company": "ForgeMind",
        }

        response = api_client.post(
            "/api/leads/",
            payload,
            format="json",
        )

        assert response.status_code == 201

        assert Lead.objects.filter(
            email="amir@test.com",
        ).exists()

    def test_retrieve_lead(
        self,
        api_client,
        lead_factory,
    ):
        """
        GET /api/leads/{id}/
        """

        lead = lead_factory()

        response = api_client.get(
            f"/api/leads/{lead.id}/",
        )

        assert response.status_code == 200
        assert response.data["id"] == str(
            lead.id,
        )

    def test_update_lead(
        self,
        api_client,
        lead_factory,
    ):
        """
        PATCH /api/leads/{id}/
        """

        lead = lead_factory()

        response = api_client.patch(
            f"/api/leads/{lead.id}/",
            {
                "company": "Updated Company",
            },
            format="json",
        )

        assert response.status_code == 200

        lead.refresh_from_db()

        assert lead.company == "Updated Company"

    def test_delete_lead(
        self,
        api_client,
        lead_factory,
    ):
        """
        DELETE /api/leads/{id}/
        """

        lead = lead_factory()

        response = api_client.delete(
            f"/api/leads/{lead.id}/",
        )

        assert response.status_code == 204

        lead.refresh_from_db()

        assert lead.is_deleted is True
