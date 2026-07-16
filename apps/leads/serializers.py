"""
Serializers for the leads application.

This module handles:
- Validation of incoming API data.
- Conversion between Lead model instances and JSON responses.
"""

from rest_framework import serializers

from apps.leads.models import Lead
from apps.leads.enums import LeadStatus


class LeadListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing leads.

    Used for collection endpoints where
    full lead details are not required.
    """

    class Meta:
        """
        Serializer configuration.
        """

        model = Lead

        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "company",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]


class LeadDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for retrieving a single lead.
    """

    class Meta:
        """
        Serializer configuration.
        """

        model = Lead

        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "company",
            "status",
            "notes",
            "created_at",
            "updated_at",
            "deleted_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class LeadCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new leads.

    Validation happens here.
    Object creation should happen inside services.py.
    """

    class Meta:
        """
        Serializer configuration.
        """

        model = Lead

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "company",
            "notes",
        ]

        extra_kwargs = {
            "phone": {
                "required": False,
                "allow_blank": True,
            },
            "company": {
                "required": False,
                "allow_blank": True,
            },
            "notes": {
                "required": False,
                "allow_blank": True,
            },
        }

    def validate_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize email address.

        Args:
            value:
                Submitted email.

        Returns:
            Lowercase email.
        """

        return value.lower()


class LeadUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating existing leads.

    Supports partial updates using PATCH.
    """

    class Meta:
        """
        Serializer configuration.
        """

        model = Lead

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "company",
            "notes",
        ]

        extra_kwargs = {
            "phone": {
                "required": False,
                "allow_blank": True,
            },
            "company": {
                "required": False,
                "allow_blank": True,
            },
            "notes": {
                "required": False,
                "allow_blank": True,
            },
        }

    def validate_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize email before update.

        Args:
            value:
                New email.

        Returns:
            Lowercase email.
        """

        return value.lower()


class LeadStatusUpdateSerializer(serializers.Serializer):
    """
    Serializer dedicated to changing lead status.

    Status changes are separated because they
    represent a business action.
    """

    status = serializers.ChoiceField(
        choices=LeadStatus.choices,
    )
