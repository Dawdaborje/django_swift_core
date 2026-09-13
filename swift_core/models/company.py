from django.db import models

from .base import BaseModel


class FiscalYearStartMonthChoices(models.TextChoices):
    jan = ("jan", "January")


class Company(BaseModel):
    name = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255, blank=True)
    registration_number = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=100, blank=True)

    # contact
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)

    # address
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default="Gambia")

    # defaults
    default_currency = models.ForeignKey(
        "swift_core.Currency",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="default_for_companies",
    )
    fiscal_year_start_month = models.CharField(
        max_length=10, choices=FiscalYearStartMonthChoices
    )

    parent_company = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="subsidiaries",
    )

    class Meta(BaseModel.Meta):
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name


class Branch(BaseModel):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="branches",
    )
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20)
    address_line1 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    is_headquarters = models.BooleanField(default=False)

    class Meta(BaseModel.Meta):
        unique_together = [("company", "code")]  # noqa: RUF012

    def __str__(self):
        return f"{self.company.name} — {self.name}"
