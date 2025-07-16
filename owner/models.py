from django.db import models

from django.contrib.auth.models import User

class AdminActionLog(models.Model):
    """
    Logs actions performed by the admin (e.g., approving vendors, deactivating users).
    """
    action = models.CharField(max_length=255)
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    target_vendor = models.ForeignKey('vendor.Vendor', on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.timestamp}"