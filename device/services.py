import requests


class DeviceAutomationService:
    """
    A service class that handles third-party integration for device automation.
    This example uses IFTTT Webhooks and Home Assistant APIs.
    """
    HOME_ASSISTANT_BASE_URL = "http://home-assistant.local:8123/"

    @staticmethod
    def trigger_home_assistant_action(device, action):
        """
        Trigger a device action using Home Assistant's REST API.
        Example API endpoints: /api/services/light/turn_on, /api/services/climate/set_temperature, etc.
        """
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyYjhlNDlkOWY5ZGU0YjZjYmM5NzU5YzNhZGQ2MjhlNiIsImlhdCI6MTcyODQ1ODY1OCwiZXhwIjoyMDQzODE4NjU4fQ.Td2h8T1TAhEmcN-RUKiy567jUoyedQO21gUNOK5QVRM",
            "Content-Type": "application/json",
        }

        if device.device_type == 'light':
            url = f"{DeviceAutomationService.HOME_ASSISTANT_BASE_URL}/services/light/turn_{action}"
            data = {"entity_id": f"light.{device.name}"}

        elif device.device_type == 'thermostat':
            url = f"{DeviceAutomationService.HOME_ASSISTANT_BASE_URL}/services/climate/set_temperature"
            data = {
                "entity_id": f"climate.{device.name}",
                "temperature": device.temperature
            }

        elif device.device_type == 'camera':
            if action == 'turn_on':
                url = f"{DeviceAutomationService.HOME_ASSISTANT_BASE_URL}/services/camera/turn_on"
            elif action == 'turn_off':
                url = f"{DeviceAutomationService.HOME_ASSISTANT_BASE_URL}/services/camera/turn_off"
            data = {"entity_id": f"camera.{device.name}"}

        elif device.device_type == 'fan':
            if action == 'turn_on':
                url = f"{DeviceAutomationService.HOME_ASSISTANT_BASE_URL}/services/fan/turn_on"
            elif action == 'turn_off':
                url = f"{DeviceAutomationService.HOME_ASSISTANT_BASE_URL}/services/fan/turn_off"
            data = {"entity_id": f"fan.{device.name}"}

        elif device.device_type == 'ac':
            if action == 'turn_on':
                url = f"{DeviceAutomationService.HOME_ASSISTANT_BASE_URL}/services/climate/turn_on"
            elif action == 'turn_off':
                url = f"{DeviceAutomationService.HOME_ASSISTANT_BASE_URL}/services/climate/turn_off"
            elif action == 'adjust_temperature':
                url = f"{DeviceAutomationService.HOME_ASSISTANT_BASE_URL}/services/climate/set_temperature"
                data = {
                    "entity_id": f"climate.{device.name}",
                    "temperature": device.temperature
                }

        response = requests.post(url, json=data, headers=headers)
        return response.status_code == 200

    @staticmethod
    def trigger_device_action(device, action):
        """
        Determine whether to use IFTTT or Home Assistant for automation based on device type.
        """
        if device.device_type in ['light', 'thermostat', 'camera', 'fan', 'ac']:
            return DeviceAutomationService.trigger_home_assistant_action(device, action)
        else:
            event_name = f"{device.device_type}_{action}"
            return DeviceAutomationService.trigger_ifttt_event(event_name)

    @staticmethod
    def handle_schedule(schedule):
        """
        Automates the schedule action at the scheduled time.
        This will be triggered from a task manager (like Celery).
        """
        success = DeviceAutomationService.trigger_device_action(schedule.device, schedule.action)
        if success:
            print(f"Scheduled action {schedule.action} executed for {schedule.device.name}.")
        else:
            print(f"Failed to execute scheduled action for {schedule.device.name}.")
