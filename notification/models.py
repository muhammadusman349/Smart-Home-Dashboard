from django.db import models
from device.models import Device
from notification import NOTIFICATION_TYPES
# Create your models here.


class Notification(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES, default='info')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification: {self.message} for {self.device.name} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
