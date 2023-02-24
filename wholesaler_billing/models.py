from django.db import models

# Create your models here.
class WholesalerSFTPInfo(models.Model):
    company = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    port = models.SmallIntegerField()
    import_directory = models.CharField(max_length=255, null=True)
    export_directory = models.CharField(max_length=255, null=True)
    is_wholesaler = models.BooleanField(default=True)


