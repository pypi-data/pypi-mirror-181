from typing import Any

from django.db import models
from django.utils.translation import gettext_lazy as _


class PaylaQuerySet(models.QuerySet):
    """
    This custom QuerySet with get_or_none method
    """

    def get_or_none(self, *args: Any, **kwargs: Any):
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None


class PaylaModel(models.Model):
    created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name=_('Last modified'), auto_now=True)

    objects = PaylaQuerySet.as_manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Overriding the save method in order to make sure that
        modified field is updated even if it is not given as
        a parameter to the update field argument.
        """
        update_fields = kwargs.get('update_fields', None)
        if update_fields:
            kwargs['update_fields'] = set(update_fields).union({'modified_at'})

        super().save(*args, **kwargs)
