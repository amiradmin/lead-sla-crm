"""
Common abstract models shared across the application.

Provides:
- UUID primary keys
- Created/updated timestamps
- Soft delete functionality
"""

from __future__ import annotations

import uuid

from django.db import models
from django.utils import timezone

from apps.common.managers import (
    ActiveObjectsManager,
    AllObjectsManager,
)


class BaseModel(models.Model):
    """
    Base abstract model.

    Adds UUID primary key and timestamps.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Creation timestamp.",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last update timestamp.",
    )

    class Meta:
        abstract = True

    def __str__(self):
        """
        Return object identifier.
        """

        return str(self.id)


class SoftDeleteModel(BaseModel):
    """
    Abstract model supporting soft deletion.

    Records are never physically deleted by default.
    """

    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    # Default manager
    objects = ActiveObjectsManager()

    # Manager including deleted records
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True

    def delete(
        self,
        using=None,
        keep_parents=False,
    ):
        """
        Soft delete object.
        """

        self.is_deleted = True
        self.deleted_at = timezone.now()

        self.save(
            update_fields=[
                "is_deleted",
                "deleted_at",
                "updated_at",
            ]
        )

    def restore(self):
        """
        Restore soft deleted object.
        """

        self.is_deleted = False
        self.deleted_at = None

        self.save(
            update_fields=[
                "is_deleted",
                "deleted_at",
                "updated_at",
            ]
        )

    def hard_delete(
        self,
        using=None,
        keep_parents=False,
    ):
        """
        Permanently remove object.
        """

        return super().delete(
            using=using,
            keep_parents=keep_parents,
        )
