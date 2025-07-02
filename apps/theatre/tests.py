from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.theatre.models import (
    TheatreHall,
    Play,
    Performance,
    Ticket,
    Reservation
)

RESERVATION_URL = "/api/theatre/reservations/"


class ReservationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword123"
        )
        self.client.force_authenticate(self.user)

        self.hall = TheatreHall.objects.create(
            name="Main Hall", rows=10, seats_in_row=20
        )
        self.play = Play.objects.create(
            title="King Lear", description="A tragedy"
        )
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.hall,
            show_time="2025-10-10T20:00:00Z"
        )

    def test_create_reservation_success(self):
        """Test that a reservation with tickets can be created successfully"""
        payload = {
            "performance": self.performance.id,
            "tickets": [
                {"row": 5, "seat": 10},
                {"row": 5, "seat": 11},
            ],
        }
        response = self.client.post(RESERVATION_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 2)
        reservation_id = response.data["id"]
        tickets = Ticket.objects.filter(reservation_id=reservation_id)
        self.assertEqual(len(tickets), 2)

    def test_create_reservation_with_taken_seat_fails(self):
        """Test creating a reservation for an already taken seat fails"""
        taken_seat_reservation = Reservation.objects.create(user=self.user)
        Ticket.objects.create(
            performance=self.performance,
            reservation=taken_seat_reservation,
            row=5,
            seat=10
        )

        payload = {
            "performance": self.performance.id,
            "tickets": [{"row": 5, "seat": 10}],
        }
        response = self.client.post(RESERVATION_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_reservation_with_invalid_seat_fails(self):
        """Test creating a reservation for a non-existent seat fails"""
        payload = {
            "performance": self.performance.id,
            "tickets": [{"row": 99, "seat": 99}]
        }
        response = self.client.post(RESERVATION_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_reservation_unauthenticated_fails(self):
        """Test that unauthenticated users cannot create a reservation"""
        self.client.force_authenticate(user=None)
        payload = {
            "performance": self.performance.id,
            "tickets": [{"row": 1, "seat": 1}],
        }
        response = self.client.post(RESERVATION_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
