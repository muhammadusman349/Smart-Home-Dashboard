from celery import shared_task
from django.utils import timezone
from .models import Schedule
from .services import DeviceAutomationService


@shared_task
def process_device_schedule():
    """
    Check active schedules and execute actions for devices based on the scheduled time.
    This function will be called periodically by Celery Beat.
    """
    current_time = timezone.now()
    active_schedules = Schedule.objects.filter(is_active=True, scheduled_time__lte=current_time)

    for schedule in active_schedules:
        device = schedule.device

        # Execute the scheduled action
        execute_device_action(device, schedule)

        # Update the schedule for recurring tasks
        update_schedule(schedule)


def execute_device_action(device, schedule):
    """
    Execute the action specified in the schedule for the given device.
    This also checks if the device is available before executing actions.
    """
    # Use the DeviceAutomationService to handle the actual device action
    success = DeviceAutomationService.trigger_device_action(device, schedule.action)
    if not success:
        print(f"Failed to execute {schedule.action} for device {device.name}.")  # Log failure

    # Update device status based on the action if successful
    if success:
        if schedule.action == 'on':
            device.status = True
        elif schedule.action == 'off':
            device.status = False
        elif schedule.action == 'adjust':
            adjust_device_settings(device)

    device.save()


def adjust_device_settings(device):
    """
    Adjust device settings based on its type.
    """
    if device.device_type == 'ac':
        device.temperature = 24.0  # Adjust temperature
    elif device.device_type == 'light':
        device.brightness = 80  # Set brightness level
    elif device.device_type == 'fan':
        device.fan_speed = 50  # Set fan speed, for example


def update_schedule(schedule):
    """
    Update the schedule for recurring tasks.
    """
    if schedule.recurring == 'daily':
        schedule.scheduled_time += timezone.timedelta(days=1)
    elif schedule.recurring == 'weekly':
        schedule.scheduled_time += timezone.timedelta(weeks=1)

    # Ensure the updated schedule is saved
    schedule.save()


@shared_task
def trigger_scheduled_action(schedule_id):
    try:
        schedule = Schedule.objects.get(id=schedule_id)
        DeviceAutomationService.handle_schedule(schedule)
    except Schedule.DoesNotExist:
        print(f"Schedule {schedule_id} not found.")
