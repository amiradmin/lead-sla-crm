from django.db.models import TextChoices


class LeadStatus(TextChoices):
    NEW = "new", "New"
    CONTACTED = "contacted", "Contacted"
    QUALIFIED = "qualified", "Qualified"
    WON = "won", "Won"
    LOST = "lost", "Lost"
