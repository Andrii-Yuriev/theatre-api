from django.urls import path, include
from rest_framework import routers
from apps.theatre.views import (
    GenreViewSet,
    ActorViewSet,
    TheatreHallViewSet,
    PlayViewSet,
    PerformanceViewSet,
    ReservationViewSet,
)

router = routers.DefaultRouter()
router.register(r"genres", GenreViewSet)
router.register(r"actors", ActorViewSet)
router.register(r"theatre_halls", TheatreHallViewSet)
router.register(r"plays", PlayViewSet)
router.register(r"performances", PerformanceViewSet)
router.register(r"reservations", ReservationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "theatre"
