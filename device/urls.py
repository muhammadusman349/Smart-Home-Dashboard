from django.urls import path
from .views import (
    DeviceListCreateView,
    DeviceRetrieveUpdateDestroyView,
    ScheduleListCreateView,
    ScheduleRetrieveUpdateDestroyView,
    TriggerDeviceActionView,
    ScheduledActionTriggerView,
)

urlpatterns = [
    # Device URLs
    path('devices/', DeviceListCreateView.as_view(), name='device-list-create'),
    path('devices/<int:pk>/', DeviceRetrieveUpdateDestroyView.as_view(), name='device-retrieve-update-destroy'),

    # Schedule URLs
    path('schedules/', ScheduleListCreateView.as_view(), name='schedule-list-create'),
    path('schedules/<int:pk>/', ScheduleRetrieveUpdateDestroyView.as_view(), name='schedule-retrieve-update-destroy'),

    # Trigger device action
    path('devices/<int:pk>/trigger/', TriggerDeviceActionView.as_view(), name='trigger-device-action'),

    # Manually trigger scheduled action
    path('schedules/<int:pk>/trigger/', ScheduledActionTriggerView.as_view(), name='trigger-scheduled-action'),
]
