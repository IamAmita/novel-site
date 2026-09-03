import pytest
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError

from accounts.models import PenName, User
from worlds.models import World


@pytest.fixture
def pen(db):
    user = User.objects.create_user(
        user_id="hoshino", email="hoshino@example.com", username="星野", password="pass-word-123"
    )
    return PenName.objects.create(user=user, display_name="星野 蒼")


class TestWorld:
    def test_create(self, pen):
        world = World.objects.create(name="異世界オルディア", owner_pen_name=pen)
        assert world.deleted_at is None

    def test_name_duplicates_allowed(self, pen):
        World.objects.create(name="異世界", owner_pen_name=pen)
        second = World.objects.create(name="異世界", owner_pen_name=pen)
        assert second.pk is not None

    def test_description_max_length(self, pen):
        world = World(name="異世界", description="あ" * 1025, owner_pen_name=pen)
        with pytest.raises(ValidationError):
            world.full_clean()
        world.description = "あ" * 1024
        world.full_clean()  # 1024文字ちょうどは通る

    def test_soft_delete_and_restore(self, pen):
        world = World.objects.create(name="異世界", owner_pen_name=pen)
        world.soft_delete()
        assert world.is_deleted
        assert World.objects.alive().count() == 0
        assert World.objects.dead().count() == 1
        world.restore()
        assert not world.is_deleted
        assert World.objects.alive().count() == 1

    def test_penname_hard_delete_protected_while_owning_world(self, pen):
        World.objects.create(name="異世界", owner_pen_name=pen)
        with pytest.raises(ProtectedError):
            pen.delete()
