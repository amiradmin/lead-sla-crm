from django.db import models


class ActiveObjectsManager(models.Manager):
    """Returns only non-soft-deleted objects."""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class AllObjectsManager(models.Manager):
    """Returns all objects including soft-deleted ones."""

    pass
