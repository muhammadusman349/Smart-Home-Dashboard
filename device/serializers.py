from rest_framework import serializers
from .models import Device, Schedule


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'name', 'device_type', 'status', 'location', 'temperature', 'brightness', 'fan_speed', 'energy_usage', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'device', 'scheduled_time', 'action', 'is_active', 'recurring', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
