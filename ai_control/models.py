from django.db import models
from device.models import Device

# Create your models here.


class AIControl(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='ai_controls')
    predicted_action = models.CharField(max_length=50, choices=[('on', 'Turn On'), ('off', 'Turn Off')])
    prediction_confidence = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Prediction for {self.device.name}: {self.predicted_action} (Confidence: {self.prediction_confidence})"

    class Meta:
        ordering = ['-timestamp']
