from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"Reservation {self.id} by {self.user}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(
        "Performance", on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        unique_together = ("row", "seat", "performance")

    def clean(self):
        if not (1 <= self.row <= self.performance.theatre_hall.rows):
            raise ValidationError(
                {
                    "row": f"Row must be between 1 and "
                    f"{self.performance.theatre_hall.rows}."
                }
            )
        if not (1 <= self.seat <= self.performance.theatre_hall.seats_in_row):
            raise ValidationError(
                {
                    "seat": f"Seat must be between 1 and "
                    f"{self.performance.theatre_hall.seats_in_row}."
                }
            )

    def __str__(self):
        return f"Row{self.row}, Seat{self.seat} for"
        f"{self.performance.play.title}"
