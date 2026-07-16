"""
Lead API views.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model


from apps.leads.selectors import (
    get_deleted_lead_by_id,
    get_lead_by_id,
    get_leads,
)

from apps.leads.serializers import (
    AssignLeadSerializer,
    ContactAttemptCreateSerializer,
    LeadCreateSerializer,
    LeadDetailSerializer,
    LeadListSerializer,
    LeadUpdateSerializer,
)

from apps.leads.services import (
    assign_lead,
    convert_lead,
    create_contact_attempt,
    create_lead,
    delete_lead,
    restore_lead,
    update_lead,
)


User = get_user_model()


class LeadViewSet(viewsets.ViewSet):
    def list(
        self,
        request,
    ):

        serializer = LeadListSerializer(
            get_leads(),
            many=True,
        )

        return Response(serializer.data)

    def retrieve(
        self,
        request,
        pk=None,
    ):

        lead = get_lead_by_id(pk)

        if not lead:
            return Response(status=404)

        return Response(LeadDetailSerializer(lead).data)

    def create(
        self,
        request,
    ):

        serializer = LeadCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        lead = create_lead(**serializer.validated_data)

        return Response(
            LeadDetailSerializer(lead).data,
            status=201,
        )

    def partial_update(
        self,
        request,
        pk=None,
    ):

        lead = get_lead_by_id(pk)

        serializer = LeadUpdateSerializer(
            lead,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        lead = update_lead(lead, serializer.validated_data)

        return Response(LeadDetailSerializer(lead).data)

    def destroy(
        self,
        request,
        pk=None,
    ):

        lead = get_lead_by_id(pk)

        delete_lead(lead)

        return Response(status=204)

    @action(
        detail=True,
        methods=["post"],
    )
    def assign(
        self,
        request,
        pk=None,
    ):

        lead = get_lead_by_id(pk)

        serializer = AssignLeadSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        advisor = User.objects.get(id=serializer.validated_data["assigned_advisor"])

        lead = assign_lead(
            lead,
            advisor,
        )

        return Response(LeadDetailSerializer(lead).data)

    @action(
        detail=True,
        methods=["post"],
    )
    def contact(
        self,
        request,
        pk=None,
    ):

        lead = get_lead_by_id(pk)

        serializer = ContactAttemptCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        attempt = create_contact_attempt(
            lead, request.user, **serializer.validated_data
        )

        return Response(
            {"id": attempt.id},
            status=201,
        )

    @action(
        detail=True,
        methods=["post"],
    )
    def convert(
        self,
        request,
        pk=None,
    ):

        lead = get_lead_by_id(pk)

        lead = convert_lead(lead)

        return Response(LeadDetailSerializer(lead).data)

    @action(
        detail=True,
        methods=["post"],
    )
    def restore(
        self,
        request,
        pk=None,
    ):

        lead = get_deleted_lead_by_id(pk)

        restore_lead(lead)

        return Response(LeadDetailSerializer(lead).data)
