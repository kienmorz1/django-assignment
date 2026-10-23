from django.urls import path, include

from .views import EventViewSet, ReservationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="event")
router.register(r"reservation", ReservationViewSet, basename="reservation")

urlpatterns = [
    path("",include(router.urls)),
]