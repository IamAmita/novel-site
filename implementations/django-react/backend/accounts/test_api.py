import pytest
from rest_framework.test import APIClient

from accounts.models import PenName, User
from worlds.models import World


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        user_id="hoshino", email="hoshino@example.com", username="星野", password="pass-word-123"
    )


@pytest.fixture
def auth_client(client, user):
    client.force_authenticate(user)
    return client


class TestRegister:
    def test_register_logs_in(self, client, db):
        res = client.post(
            "/api/auth/register/",
            {
                "user_id": "newuser",
                "email": "new@example.com",
                "username": "新規",
                "password": "pass-word-123",
            },
        )
        assert res.status_code == 201
        assert res.json()["user_id"] == "newuser"
        # 登録成功で即ログイン状態（SC-01）
        me = client.get("/api/auth/me/")
        assert me.status_code == 200

    def test_register_rejects_weak_password(self, client, db):
        res = client.post(
            "/api/auth/register/",
            {"user_id": "x123", "email": "x@example.com", "username": "x", "password": "1234"},
        )
        assert res.status_code == 400

    def test_register_rejects_bad_user_id(self, client, db):
        res = client.post(
            "/api/auth/register/",
            {"user_id": "ab", "email": "x@example.com", "username": "x", "password": "pass-word-123"},
        )
        assert res.status_code == 400


class TestLogin:
    @pytest.mark.parametrize("identifier", ["hoshino", "hoshino@example.com"])
    def test_login(self, client, user, identifier):
        res = client.post("/api/auth/login/", {"identifier": identifier, "password": "pass-word-123"})
        assert res.status_code == 200

    def test_login_failure(self, client, user):
        res = client.post("/api/auth/login/", {"identifier": "hoshino", "password": "wrong"})
        assert res.status_code == 400

    def test_me_requires_auth(self, client, db):
        assert client.get("/api/auth/me/").status_code == 403


class TestMe:
    def test_patch_profile(self, auth_client):
        res = auth_client.patch("/api/auth/me/", {"username": "改名", "bio": "自己紹介"})
        assert res.status_code == 200
        assert res.json()["username"] == "改名"

    def test_user_id_and_email_are_read_only(self, auth_client, user):
        auth_client.patch("/api/auth/me/", {"user_id": "changed", "email": "e@example.com"})
        user.refresh_from_db()
        assert user.user_id == "hoshino"
        assert user.email == "hoshino@example.com"

    def test_delete_account(self, auth_client, user):
        res = auth_client.delete("/api/auth/me/")
        assert res.status_code == 204
        user.refresh_from_db()
        assert user.is_deleted


class TestPenNameApi:
    def test_create_and_list(self, auth_client):
        res = auth_client.post("/api/pennames/", {"display_name": "星野 蒼"})
        assert res.status_code == 201
        rows = auth_client.get("/api/pennames/").json()
        assert [r["display_name"] for r in rows] == ["星野 蒼"]
        assert rows[0]["world_count"] == 0

    def test_duplicate_display_name_rejected(self, auth_client):
        auth_client.post("/api/pennames/", {"display_name": "星野 蒼"})
        res = auth_client.post("/api/pennames/", {"display_name": "星野 蒼"})
        assert res.status_code == 400

    def test_destroy_blocked_while_owning_world(self, auth_client, user):
        pen = PenName.objects.create(user=user, display_name="星野 蒼")
        World.objects.create(name="異世界", owner_pen_name=pen)
        res = auth_client.delete(f"/api/pennames/{pen.pk}/")
        assert res.status_code == 400
        pen.refresh_from_db()
        assert not pen.is_deleted

    def test_destroy(self, auth_client, user):
        pen = PenName.objects.create(user=user, display_name="星野 蒼")
        res = auth_client.delete(f"/api/pennames/{pen.pk}/")
        assert res.status_code == 204
        pen.refresh_from_db()
        assert pen.is_deleted

    def test_other_users_pennames_hidden(self, auth_client, db):
        other = User.objects.create_user(
            user_id="other", email="o@example.com", username="別人", password="pass-word-123"
        )
        PenName.objects.create(user=other, display_name="他人の名義")
        rows = auth_client.get("/api/pennames/").json()
        assert rows == []
