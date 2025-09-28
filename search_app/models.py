from django.db import models

# Create your models here.


class GoogleAPIKeys(models.Model):

    KEY_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    key = models.CharField(max_length=120)
    cse_id = models.CharField(max_length=120, null=True, blank=True)
    status = models.CharField(choices=KEY_STATUS, default='active', max_length=10)
    usage_count = models.IntegerField(default=0)
    last_used = models.DateTimeField(auto_now=True)
    deactivated_at = models.DateTimeField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"key- {self.key}"
