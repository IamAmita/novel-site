from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import PenName, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "user_id", "email", "username", "icon", "bio"]
        read_only_fields = ["id", "user_id", "email"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["user_id", "email", "username", "password"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class PenNameSerializer(serializers.ModelSerializer):
    world_count = serializers.SerializerMethodField()

    class Meta:
        model = PenName
        fields = ["id", "display_name", "icon", "bio", "world_count"]

    def get_world_count(self, obj):
        # 一覧に表示するWorld数は有効なもののみ（SC-06）
        return obj.worlds.alive().count()

    def validate_display_name(self, value):
        user = self.context["request"].user
        qs = user.pen_names.alive().filter(display_name=value)
        if self.instance is not None:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("同じ表示名のペンネームがすでにあります。")
        return value

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
