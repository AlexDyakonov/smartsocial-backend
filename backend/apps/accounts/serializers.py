from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User


class UserListSerializer(serializers.ModelSerializer):
    place_name = serializers.CharField(source="place.name", read_only=True)
    place_id = serializers.IntegerField(source="place.id", read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "place_name",
            "place_id",
            "first_name",
            "middle_name",
            "last_name",
            "is_active",
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "phone_number",
            "place",
            "password",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
            "phone_number": {"required": True},
        }

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return User.objects.create(**validated_data)
