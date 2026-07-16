"""
API views for the leads application.

This module exposes REST API endpoints for:

- Listing leads
- Creating leads
- Retrieving lead details
- Updating leads
- Soft deleting leads
- Restoring deleted leads
- Updating lead status

The view layer is responsible only for:
- HTTP request handling
- Serializer validation
- Returning responses

Database operations belong to selectors.py.
Business logic belongs to services.py.
"""

from __future__ import annotations

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.leads.selectors import (
    get_deleted_lead_by_id,
    get_lead_by_id,
    get_leads,
)
from apps.leads.serializers import (
    LeadCreateSerializer,
    LeadDetailSerializer,
    LeadListSerializer,
    LeadStatusUpdateSerializer,
    LeadUpdateSerializer,
)
from apps.leads.services import (
    change_lead_status,
    create_lead,
    delete_lead,
    restore_lead,
    update_lead,
)


class LeadViewSet(viewsets.ViewSet):
    """
    ViewSet providing CRUD operations for Lead objects.

    The implementation follows service-layer architecture.
    """

    def list(
        self,
        request: Request,
    ) -> Response:
        """
        Return all active leads.
        """

        leads = get_leads()

        serializer = LeadListSerializer(
            leads,
            many=True,
        )

        return Response(
            serializer.data,
        )

    def retrieve(
        self,
        request: Request,
        pk=None,
    ) -> Response:
        """
        Retrieve a single lead.
        """

        lead = get_lead_by_id(
            pk,
        )

        if not lead:
            return Response(
                {
                    "detail": "Lead not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = LeadDetailSerializer(
            lead,
        )

        return Response(
            serializer.data,
        )

    def create(
        self,
        request: Request,
    ) -> Response:
        """
        Create a new lead.
        """

        serializer = LeadCreateSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        lead = create_lead(
            data=serializer.validated_data,
        )

        output = LeadDetailSerializer(
            lead,
        )

        return Response(
            output.data,
            status=status.HTTP_201_CREATED,
        )

    def update(
        self,
        request: Request,
        pk=None,
    ) -> Response:
        """
        Fully update a lead.
        """

        lead = get_lead_by_id(
            pk,
        )

        if not lead:
            return Response(
                {
                    "detail": "Lead not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = LeadUpdateSerializer(
            lead,
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        lead = update_lead(
            lead=lead,
            data=serializer.validated_data,
        )

        output = LeadDetailSerializer(
            lead,
        )

        return Response(
            output.data,
        )

    def partial_update(
        self,
        request: Request,
        pk=None,
    ) -> Response:
        """
        Partially update a lead.
        """

        lead = get_lead_by_id(
            pk,
        )

        if not lead:
            return Response(
                {
                    "detail": "Lead not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = LeadUpdateSerializer(
            lead,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        lead = update_lead(
            lead=lead,
            data=serializer.validated_data,
        )

        output = LeadDetailSerializer(
            lead,
        )

        return Response(
            output.data,
        )

    def destroy(
        self,
        request: Request,
        pk=None,
    ) -> Response:
        """
        Soft delete a lead.
        """

        lead = get_lead_by_id(
            pk,
        )

        if not lead:
            return Response(
                {
                    "detail": "Lead not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        delete_lead(
            lead=lead,
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(
        detail=True,
        methods=["patch"],
        url_path="status",
    )
    def update_status(
        self,
        request: Request,
        pk=None,
    ) -> Response:
        """
        Update lead lifecycle status.
        """

        lead = get_lead_by_id(
            pk,
        )

        if not lead:
            return Response(
                {
                    "detail": "Lead not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = LeadStatusUpdateSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        lead = change_lead_status(
            lead=lead,
            status=serializer.validated_data["status"],
        )

        output = LeadDetailSerializer(
            lead,
        )

        return Response(
            output.data,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="restore",
    )
    def restore(
        self,
        request: Request,
        pk=None,
    ) -> Response:
        """
        Restore a soft deleted lead.
        """

        lead = get_deleted_lead_by_id(
            pk,
        )

        if not lead:
            return Response(
                {
                    "detail": "Lead not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        restore_lead(
            lead=lead,
        )

        output = LeadDetailSerializer(
            lead,
        )

        return Response(
            output.data,
        )
