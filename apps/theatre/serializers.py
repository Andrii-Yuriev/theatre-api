from rest_framework import serializers

from apps.theatre.models import (
    Genre,
    Actor,
    TheatreHall,
    Play,
    Performance,
    Reservation,
    Ticket,
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name")


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row", "capacity")

class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "title", "description", "genres", "actors")


class PlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "title")


class PlayDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = ("id", "title", "description", "genres", "actors")


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time")


class PerformanceListSerializer(serializers.ModelSerializer):
    play_title = serializers.CharField(source="play.title", read_only=True)
    theatre_hall_name = serializers.CharField(
        source="theatre_hall.name", read_only=True
    )
    theatre_hall_capacity = serializers.IntegerField(
        source="theatre_hall.capacity", read_only=True
    )

    class Meta:
        model = Performance
        fields = (
            "id",
            "show_time",
            "play_title",
            "theatre_hall_name",
            "theatre_hall_capacity",
        )


class PerformanceDetailSerializer(serializers.ModelSerializer):
    play = PlayDetailSerializer(many=False, read_only=True)
    theatre_hall = TheatreHallSerializer(many=False, read_only=True)

    class Meta(PerformanceSerializer.Meta):
        fields = PerformanceSerializer.Meta.fields + ("play", "theatre_hall")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat",  "performance")


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "created_at")
