from rest_framework import serializers

from accounts.models import PenName

from .models import World


class WorldSerializer(serializers.ModelSerializer):
    owner_pen_name_display = serializers.CharField(
        source="owner_pen_name.display_name", read_only=True
    )
    is_deleted = serializers.BooleanField(read_only=True)

    class Meta:
        model = World
        fields = [
            "id",
            "name",
            "description",
            "cover_image",
            "owner_pen_name",
            "owner_pen_name_display",
            "is_deleted",
            "updated_at",
        ]

    def validate_owner_pen_name(self, value: PenName):
        if value.user_id != self.context["request"].user.pk or value.is_deleted:
            raise serializers.ValidationError("自分のペンネームを指定してください。")
        return value
