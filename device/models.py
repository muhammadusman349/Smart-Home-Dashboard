from django.db import models
from account.models import User
from device import DEVICE_TYPES, SCHEDULE_ACTIONS, RECURRING_CHOICES


class Device(models.Model):
    name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPES)
    status = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="devices")
    location = models.CharField(max_length=255, blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Thermostats, AC
    brightness = models.IntegerField(null=True, blank=True)  # Lights
    fan_speed = models.IntegerField(null=True, blank=True)  # Fan speed (0-100)
    energy_usage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # kWh consumption
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.device_type})"

    class Meta:
        ordering = ['device_type', 'name']


class Schedule(models.Model):    
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='schedules')
    scheduled_time = models.DateTimeField()
    action = models.CharField(max_length=50, choices=SCHEDULE_ACTIONS)
    is_active = models.BooleanField(default=True)
    recurring = models.CharField(max_length=10, choices=RECURRING_CHOICES, default='none')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Schedule {self.action} for {self.device.name} at {self.scheduled_time}"

    class Meta:
        ordering = ['scheduled_time']
