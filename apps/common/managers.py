"""
Custom Django model managers.

This module provides reusable managers for handling
soft-deleted records across the application.
"""

from django.db import models


class ActiveObjectsManager(models.Manager):
    """
    Manager returning only active objects.

    Objects marked as deleted using soft delete
    will not appear in normal queries.
    """

    def get_queryset(self):
        """
        Return queryset excluding deleted records.

        Returns:
            QuerySet: Active objects only.
        """

        return super().get_queryset().filter(is_deleted=False)


class AllObjectsManager(models.Manager):
    """
    Manager returning all objects.

    Includes both active and soft-deleted records.
    """

    def get_queryset(self):
        """
        Return all records without filtering.

        Returns:
            QuerySet: Complete queryset.
        """

        return super().get_queryset()


class SoftDeleteManager(ActiveObjectsManager):
    """
    Backward-compatible alias for soft delete manager.

    This allows existing imports like:

        from apps.common.managers import SoftDeleteManager

    """

    pass
