from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from swift_core.models.base import BaseModel


class Party(BaseModel, MPTTModel):
    """
    A person or organisation that your business interacts with.
    Could be a customer, vendor, employee, or your own company.
    """

    INDIVIDUAL = "individual"
    ORGANISATION = "organisation"
    TYPE_CHOICES = [
        (INDIVIDUAL, "Individual"),
        (ORGANISATION, "Organisation"),
    ]

    name = models.CharField(max_length=255)
    party_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    # if individual, optionally link to their organisation
    organisation = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="contacts",
        limit_choices_to={"party_type": "organisation"},
    )

    # identity fields — live here once
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    tax_id = models.CharField(max_length=100, blank=True)

    # address
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    company = models.ForeignKey(
        "swift_core.Company",
        on_delete=models.CASCADE,
        related_name="parties",
    )

    def __str__(self):
        return self.name
