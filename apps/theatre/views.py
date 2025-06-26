from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from apps.theatre.models import (
    Genre,
    Actor,
    TheatreHall,
    Play,
    Performance,
    Reservation,
    Ticket,
)
from apps.theatre.serializers import (
    GenreSerializer,
    ActorSerializer,
    TheatreHallSerializer,
    PlaySerializer,
    PlayListSerializer,
    PlayDetailSerializer,
    PerformanceSerializer,
    PerformanceListSerializer,
    PerformanceDetailSerializer,
    ReservationSerializer,
)


class IsAdminOrIfAuthenticatedReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in ("GET", "HEAD", "OPTIONS") or is_admin


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("genres", "actors")

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer
        elif self.action == "retrieve":
            return PlayDetailSerializer
        return PlaySerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("play", "show_time")

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer
        elif self.action == "retrieve":
            return PerformanceDetailSerializer
        return PerformanceSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Users can see only their own reservations"""
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Assign the current user to the reservation"""
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Custom create method to handle reservation with tickets.
        Expects {"performance": int, "tickets": [{"row": int, "seat": int}]}
        """
        performance_id = request.data.get("performance")
        tickets_data = request.data.get("tickets")

        if not performance_id or not isinstance(tickets_data, list):
            return Response(
                {"error": "perfor-ce ID and a list of tickets are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            performance = Performance.objects.get(id=performance_id)
        except Performance.DoesNotExist:
            return Response(
                {"error": "Performance not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            with transaction.atomic():
                reservation = Reservation.objects.create(user=request.user)

                tickets_to_create = []
                for ticket_data in tickets_data:
                    row = ticket_data.get("row")
                    seat = ticket_data.get("seat")

                    if not (1 <= row <= performance.theatre_hall.rows):
                        raise ValueError(f"Row {row} is out of bounds.")
                    if not (1 <= seat <= performance.theatre_hall.seats_in_row):
                        raise ValueError(f"Seat {seat} is out of bounds.")

                    if Ticket.objects.filter(
                        performance=performance, row=row, seat=seat
                    ).exists():
                        raise ValueError(f"Seat ({row}, {seat}) is taken.")

                    tickets_to_create.append(
                        Ticket(
                            reservation=reservation,
                            performance=performance,
                            row=row,
                            seat=seat,
                        )
                    )

                Ticket.objects.bulk_create(tickets_to_create)

                serializer = self.get_serializer(reservation)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(
                {"error": "An unexpected error occurred during reservation."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
