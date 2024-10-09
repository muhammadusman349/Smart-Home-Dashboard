from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Device, Schedule
from .serializers import DeviceSerializer, ScheduleSerializer
from .services import DeviceAutomationService
from .tasks import trigger_scheduled_action


class DeviceListCreateView(generics.ListCreateAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DeviceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)


class ScheduleListCreateView(generics.ListCreateAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Schedule.objects.filter(device__owner=self.request.user)

    def perform_create(self, serializer):
        device = serializer.validated_data['device']
        if device.owner != self.request.user:
            return Response({'error': 'You do not have permission to schedule this device.'},
                            status=status.HTTP_403_FORBIDDEN)
        serializer.save()


class ScheduleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Schedule.objects.filter(device__owner=self.request.user)


class TriggerDeviceActionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            device = Device.objects.get(pk=pk, owner=request.user)
        except Device.DoesNotExist:
            return Response({'error': 'Device not found or permission denied.'}, status=status.HTTP_404_NOT_FOUND)

        # Get the action to perform (e.g., "turn_on", "turn_off")
        action = request.data.get('action')
        if action not in ['turn_on', 'turn_off']:
            return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

        # Use DeviceAutomationService to trigger the action
        success = DeviceAutomationService.trigger_device_action(device, action)
        if success:
            return Response({'message': f'{device.name} successfully {action}ed.'})
        else:
            return Response({'error': f'Failed to {action} {device.name}.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ScheduledActionTriggerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            schedule = Schedule.objects.get(pk=pk, device__owner=request.user)
            trigger_scheduled_action.delay(schedule.id)  # Call the Celery task asynchronously
            return Response({'message': f'Scheduled action {schedule.action} executed for {schedule.device.name}.'})
        except Schedule.DoesNotExist:
            return Response({'error': 'Schedule not found or permission denied.'}, status=status.HTTP_404_NOT_FOUND)
