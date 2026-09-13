import typing
import uuid

from django.contrib.auth import get_user_model
from django.db import models


class BaseModel(models.Model):
    """
    Abstract base for every model in the Swift suite.
    Provides UUID primary key, audit fields, and soft delete.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_created",
    )
    updated_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_updated",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering: typing.ClassVar = ["-created_at"]


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return self.update(is_deleted=True)

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(is_deleted=False)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model).filter(is_deleted=False)


class SoftDeleteModel(BaseModel):
    """
    Extends BaseModel with soft delete.
    Use this for anything that needs an audit trail on deletion
    — journal entries, payslips, invoices.
    """

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_deleted",
    )

    objects = SoftDeleteManager()
    all_objects = models.Manager()  # bypass soft delete when needed

    def delete(self, deleted_by=None, *args, **kwargs):
        from django.utils import timezone

        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = deleted_by
        self.save()

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    class Meta(BaseModel.Meta):
        abstract = True
