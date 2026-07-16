"""
Lead API views.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from uuid import UUID

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

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter


User = get_user_model()


@extend_schema_view(
    list=extend_schema(
        responses=LeadListSerializer(many=True),
        summary="List leads",
    ),
    retrieve=extend_schema(
        responses=LeadDetailSerializer,
        summary="Retrieve lead",
    ),
    create=extend_schema(
        request=LeadCreateSerializer,
        responses=LeadDetailSerializer,
        summary="Create lead",
    ),
    partial_update=extend_schema(
        request=LeadUpdateSerializer,
        responses=LeadDetailSerializer,
        summary="Update lead",
    ),
)
class LeadViewSet(viewsets.ViewSet):
    serializer_class = LeadDetailSerializer

    def list(
        self,
        request,
    ):

        serializer = LeadListSerializer(
            get_leads(),
            many=True,
        )

        return Response(serializer.data)

    @extend_schema(
        summary="Retrieve lead",
        parameters=[
            OpenApiParameter(
                name="id",
                type=str,
                location=OpenApiParameter.PATH,
                description="Lead UUID",
            ),
        ],
        responses=LeadDetailSerializer,
    )
    def retrieve(
        self,
        request,
        pk: UUID = None,
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

    @extend_schema(
        summary="Partial update lead",
        parameters=[
            OpenApiParameter(
                name="id",
                type=str,
                location=OpenApiParameter.PATH,
                description="Lead UUID",
            ),
        ],
        responses=LeadDetailSerializer,
    )
    def partial_update(
        self,
        request,
        pk: UUID = None,
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

    @extend_schema(
        summary="Soft delete lead",
        parameters=[
            OpenApiParameter(
                name="id",
                type=str,
                location=OpenApiParameter.PATH,
                description="Lead UUID",
            ),
        ],
        responses=LeadDetailSerializer,
    )
    def destroy(
        self,
        request,
        pk: UUID = None,
    ):

        lead = get_lead_by_id(pk)

        delete_lead(lead)

        return Response(status=204)

    @extend_schema(
        summary="Assign lead",
        parameters=[
            OpenApiParameter(
                name="id",
                type=str,
                location=OpenApiParameter.PATH,
                description="Lead UUID",
            ),
        ],
        responses=LeadDetailSerializer,
    )
    @action(
        detail=True,
        methods=["post"],
    )
    def assign(
        self,
        request,
        pk: UUID = None,
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

    @extend_schema(
        summary="Create contact attempt",
        parameters=[
            OpenApiParameter(
                name="id",
                type=str,
                location=OpenApiParameter.PATH,
                description="Lead UUID",
            ),
        ],
        responses=LeadDetailSerializer,
    )
    @action(
        detail=True,
        methods=["post"],
    )
    def contact(
        self,
        request,
        pk: UUID = None,
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

    @extend_schema(
        summary="Convert lead",
        parameters=[
            OpenApiParameter(
                name="id",
                type=str,
                location=OpenApiParameter.PATH,
                description="Lead UUID",
            ),
        ],
        responses=LeadDetailSerializer,
    )
    @action(
        detail=True,
        methods=["post"],
    )
    def convert(
        self,
        request,
        pk: UUID = None,
    ):

        lead = get_lead_by_id(pk)

        lead = convert_lead(lead)

        return Response(LeadDetailSerializer(lead).data)

    @extend_schema(
        summary="Restore lead",
        parameters=[
            OpenApiParameter(
                name="id",
                type=str,
                location=OpenApiParameter.PATH,
                description="Lead UUID",
            ),
        ],
        responses=LeadDetailSerializer,
    )
    @action(
        detail=True,
        methods=["post"],
    )
    def restore(
        self,
        request,
        pk: UUID = None,
    ):

        lead = get_deleted_lead_by_id(pk)

        restore_lead(lead)

        return Response(LeadDetailSerializer(lead).data)
