import pytest
from rest_framework.test import APIClient

from accounts.models import PenName, User
from worlds.models import World


@pytest.fixture
def user(db):
    return User.objects.create_user(
        user_id="hoshino", email="hoshino@example.com", username="星野", password="pass-word-123"
    )


@pytest.fixture
def pen(user):
    return PenName.objects.create(user=user, display_name="星野 蒼")


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client


class TestWorldApi:
    def test_create(self, auth_client, pen):
        res = auth_client.post("/api/worlds/", {"name": "異世界オルディア", "owner_pen_name": pen.pk})
        assert res.status_code == 201
        assert res.json()["owner_pen_name_display"] == "星野 蒼"

    def test_cannot_use_others_penname(self, auth_client, db):
        other = User.objects.create_user(
            user_id="other", email="o@example.com", username="別人", password="pass-word-123"
        )
        other_pen = PenName.objects.create(user=other, display_name="他人の名義")
        res = auth_client.post("/api/worlds/", {"name": "異世界", "owner_pen_name": other_pen.pk})
        assert res.status_code == 400

    def test_name_max_100(self, auth_client, pen):
        res = auth_client.post("/api/worlds/", {"name": "あ" * 101, "owner_pen_name": pen.pk})
        assert res.status_code == 400

    def test_list_excludes_deleted_by_default(self, auth_client, pen):
        World.objects.create(name="有効", owner_pen_name=pen)
        deleted = World.objects.create(name="削除済み", owner_pen_name=pen)
        deleted.soft_delete()
        names = [w["name"] for w in auth_client.get("/api/worlds/").json()]
        assert names == ["有効"]
        # トグルON相当
        rows = auth_client.get("/api/worlds/?include_deleted=1").json()
        assert {w["name"]: w["is_deleted"] for w in rows} == {"有効": False, "削除済み": True}

    def test_search_by_name_only(self, auth_client, pen):
        World.objects.create(name="異世界オルディア", description="魔法", owner_pen_name=pen)
        World.objects.create(name="近未来都市", description="異世界要素あり", owner_pen_name=pen)
        names = [w["name"] for w in auth_client.get("/api/worlds/?q=異世界").json()]
        assert names == ["異世界オルディア"]  # 説明文はヒットしない

    def test_soft_delete_and_restore(self, auth_client, pen):
        world = World.objects.create(name="異世界", owner_pen_name=pen)
        assert auth_client.delete(f"/api/worlds/{world.pk}/").status_code == 204
        world.refresh_from_db()
        assert world.is_deleted
        res = auth_client.post(f"/api/worlds/{world.pk}/restore/")
        assert res.status_code == 200
        world.refresh_from_db()
        assert not world.is_deleted

    def test_change_owner_pen_name(self, auth_client, user, pen):
        world = World.objects.create(name="異世界", owner_pen_name=pen)
        pen2 = PenName.objects.create(user=user, display_name="月宮 かなた")
        res = auth_client.patch(f"/api/worlds/{world.pk}/", {"owner_pen_name": pen2.pk})
        assert res.status_code == 200
        assert res.json()["owner_pen_name_display"] == "月宮 かなた"

    def test_other_users_worlds_hidden(self, auth_client, db):
        other = User.objects.create_user(
            user_id="other", email="o@example.com", username="別人", password="pass-word-123"
        )
        other_pen = PenName.objects.create(user=other, display_name="他人の名義")
        other_world = World.objects.create(name="他人のWorld", owner_pen_name=other_pen)
        assert auth_client.get("/api/worlds/").json() == []
        assert auth_client.get(f"/api/worlds/{other_world.pk}/").status_code == 404
