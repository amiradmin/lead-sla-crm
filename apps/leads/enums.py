"""
Lead related enumerations.
"""

from django.db import models


class LeadStatus(models.TextChoices):
    """
    Possible lifecycle states for a lead.
    """

    NEW = "new", "New"

    CONTACTED = "contacted", "Contacted"

    QUALIFIED = "qualified", "Qualified"

    CONVERTED = "converted", "Converted"

    LOST = "lost", "Lost"
