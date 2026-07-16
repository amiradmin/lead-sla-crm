"""
Serializers for leads API.
"""

from rest_framework import serializers

from apps.leads.models import ContactAttempt, Lead


class LeadListSerializer(serializers.ModelSerializer):
    """
    Serializer for lead list.
    """

    class Meta:
        model = Lead

        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "source",
            "status",
            "assigned_advisor",
            "sla_deadline",
            "created_at",
        ]


class LeadDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for lead details.
    """

    class Meta:
        model = Lead

        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "source",
            "status",
            "assigned_advisor",
            "sla_deadline",
            "first_contacted_at",
            "converted_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "status",
            "assigned_advisor",
            "sla_deadline",
            "first_contacted_at",
            "converted_at",
            "created_at",
            "updated_at",
        ]


class LeadCreateSerializer(serializers.ModelSerializer):
    """
    Create lead serializer.
    """

    class Meta:
        model = Lead

        fields = [
            "full_name",
            "email",
            "phone",
            "source",
        ]

    def validate_email(self, value):
        return value.lower()


class LeadUpdateSerializer(serializers.ModelSerializer):
    """
    Update lead information.
    """

    class Meta:
        model = Lead

        fields = [
            "full_name",
            "email",
            "phone",
            "source",
        ]


class AssignLeadSerializer(serializers.Serializer):
    """
    Assign advisor.
    """

    assigned_advisor = serializers.IntegerField()


class ContactAttemptCreateSerializer(serializers.ModelSerializer):
    """
    Create contact attempt.
    """

    class Meta:
        model = ContactAttempt

        fields = [
            "channel",
            "outcome",
            "notes",
        ]


class ConvertLeadSerializer(serializers.Serializer):
    """
    Convert lead.
    """

    pass
