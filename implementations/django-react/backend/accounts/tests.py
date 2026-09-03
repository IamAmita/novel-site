import pytest
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from accounts.models import PenName, User
from worlds.models import World


@pytest.fixture
def user(db):
    return User.objects.create_user(
        user_id="hoshino", email="hoshino@example.com", username="星野", password="pass-word-123"
    )


class TestUser:
    def test_create_user(self, user):
        assert user.pk is not None
        assert user.check_password("pass-word-123")
        assert user.deleted_at is None

    def test_user_id_format_validation(self, db):
        bad = User(user_id="ab", email="a@example.com", username="a")
        with pytest.raises(ValidationError):
            bad.full_clean()
        bad = User(user_id="日本語ですよ", email="a@example.com", username="a")
        with pytest.raises(ValidationError):
            bad.full_clean()

    def test_user_id_unique(self, user):
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                user_id="hoshino", email="other@example.com", username="別人", password="x"
            )

    def test_username_duplicates_allowed(self, user, db):
        other = User.objects.create_user(
            user_id="tsukimiya", email="tsuki@example.com", username="星野", password="pass-word-123"
        )
        assert other.username == user.username

    def test_soft_delete_cascades_to_pennames_and_worlds(self, user):
        pen = PenName.objects.create(user=user, display_name="星野 蒼")
        world = World.objects.create(name="異世界", owner_pen_name=pen)
        user.soft_delete()
        pen.refresh_from_db()
        world.refresh_from_db()
        user.refresh_from_db()
        assert user.is_deleted and not user.is_active
        assert pen.is_deleted
        assert world.is_deleted


class TestAuthBackend:
    def test_login_with_user_id(self, user):
        assert authenticate(None, username="hoshino", password="pass-word-123") == user

    def test_login_with_email(self, user):
        assert authenticate(None, username="hoshino@example.com", password="pass-word-123") == user

    def test_wrong_password(self, user):
        assert authenticate(None, username="hoshino", password="wrong") is None

    def test_deleted_user_cannot_login(self, user):
        user.soft_delete()
        assert authenticate(None, username="hoshino", password="pass-word-123") is None


class TestPenName:
    def test_display_name_unique_within_user(self, user):
        PenName.objects.create(user=user, display_name="星野 蒼")
        with pytest.raises(IntegrityError):
            PenName.objects.create(user=user, display_name="星野 蒼")

    def test_display_name_can_duplicate_across_users(self, user, db):
        other = User.objects.create_user(
            user_id="other", email="o@example.com", username="別人", password="pass-word-123"
        )
        PenName.objects.create(user=user, display_name="星野 蒼")
        pen = PenName.objects.create(user=other, display_name="星野 蒼")
        assert pen.pk is not None

    def test_deleted_name_can_be_reused(self, user):
        pen = PenName.objects.create(user=user, display_name="星野 蒼")
        pen.soft_delete()
        again = PenName.objects.create(user=user, display_name="星野 蒼")
        assert again.pk != pen.pk

    def test_has_worlds_counts_deleted_worlds(self, user):
        """削除済みWorldの所有者も削除不可（復元不能を防ぐ。レビュー残課題7）"""
        pen = PenName.objects.create(user=user, display_name="星野 蒼")
        assert not pen.has_worlds()
        world = World.objects.create(name="異世界", owner_pen_name=pen)
        world.soft_delete()
        assert pen.has_worlds()
