"""
Lead related enumerations.
"""

from django.db import models


class LeadSource(models.TextChoices):
    """
    Source from which the lead was acquired.
    """

    WEBSITE = "website", "Website"

    REFERRAL = "referral", "Referral"

    SOCIAL = "social", "Social Media"

    EVENT = "event", "Event"


class LeadStatus(models.TextChoices):
    """
    Lifecycle states of a lead.
    """

    NEW = "new", "New"

    ASSIGNED = "assigned", "Assigned"

    CONTACTED = "contacted", "Contacted"

    CONVERTED = "converted", "Converted"

    CLOSED_LOST = "closed_lost", "Closed Lost"


class ContactChannel(models.TextChoices):
    """
    Available communication channels.
    """

    CALL = "call", "Call"

    EMAIL = "email", "Email"

    WHATSAPP = "whatsapp", "WhatsApp"


class ContactOutcome(models.TextChoices):
    """
    Result of a contact attempt.
    """

    REACHED = "reached", "Reached"

    NO_ANSWER = "no_answer", "No Answer"

    WRONG_NUMBER = "wrong_number", "Wrong Number"
