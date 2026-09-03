"""メールアドレスまたはユーザーIDでログインできる認証バックエンド（User.md）。"""

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class EmailOrUserIdBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        identifier = username or kwargs.get(User.USERNAME_FIELD)
        if identifier is None or password is None:
            return None
        # 「@」を含むならメールアドレス、含まないならユーザーIDとして判別
        # （画面仕様 SC-02）
        field = "email" if "@" in identifier else "user_id"
        try:
            user = User.objects.get(**{field: identifier})
        except User.DoesNotExist:
            User().set_password(password)  # タイミング攻撃対策（存在有無で応答時間を変えない）
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def user_can_authenticate(self, user):
        return super().user_can_authenticate(user) and user.deleted_at is None
