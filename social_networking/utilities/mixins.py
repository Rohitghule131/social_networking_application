from django.db import models


class CustomMixins(models.Model):
    """
    Class for create a mixin for table model.
    """
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        