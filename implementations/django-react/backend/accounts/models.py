"""User（アカウント）・PenName（ペンネーム）。

仕様: docs/domain/User.md
Phase 1で見送り: User.status / deleted_by（docs/project/Phase1-確定メモ.md §3.1）
"""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MaxLengthValidator, RegexValidator
from django.db import models

from common.models import SoftDeleteModel

user_id_validator = RegexValidator(
    regex=r"^[A-Za-z0-9_]{3,20}$",
    message="ユーザーIDは英数字・アンダースコアのみ、3〜20文字で入力してください。",
)


class UserManager(BaseUserManager):
    def create_user(self, user_id, email, username, password=None, **extra_fields):
        if not user_id:
            raise ValueError("user_id は必須です")
        if not email:
            raise ValueError("email は必須です")
        if not username:
            raise ValueError("username は必須です")
        user = self.model(
            user_id=user_id,
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(user_id, email, username, password, **extra_fields)


class User(SoftDeleteModel, AbstractBaseUser, PermissionsMixin):
    # user_id はログイン・プロフィールURLに使う公開識別子（変更不可）。
    # 内部主キー(id)とは別物で、外部キー参照は常に id を使う
    user_id = models.CharField(max_length=20, unique=True, validators=[user_id_validator])
    email = models.EmailField(unique=True)
    # username は識別子ではなく単なる表示名（重複可・変更可）
    username = models.CharField(max_length=50)
    icon = models.ImageField(upload_to="user_icons/", null=True, blank=True)
    bio = models.TextField(blank=True, validators=[MaxLengthValidator(1024)])

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "user_id"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email", "username"]

    def __str__(self):
        return f"@{self.user_id}"

    def soft_delete(self):
        # アカウント削除時、配下データは連鎖的に論理削除（User.md）
        super().soft_delete()
        for pen_name in self.pen_names.alive():
            pen_name.soft_delete_cascade()
        self.is_active = False
        self.save(update_fields=["is_active"])


class PenName(SoftDeleteModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pen_names")
    display_name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="pen_name_icons/", null=True, blank=True)
    bio = models.TextField(blank=True, validators=[MaxLengthValidator(1024)])

    class Meta:
        constraints = [
            # 表示名の一意性は同一ユーザー内のみ（有効なレコード同士で判定）
            models.UniqueConstraint(
                fields=["user", "display_name"],
                condition=models.Q(deleted_at__isnull=True),
                name="uniq_penname_display_name_per_user",
            ),
        ]

    def __str__(self):
        return self.display_name

    def has_worlds(self):
        """Worldを1件でも保持していれば削除不可（User.md）。

        削除済みWorldも数える: 数えずに消すと、そのWorldが復元できなくなるため
        （レビュー残課題 7）。
        """
        return self.worlds.exists()

    def soft_delete_cascade(self):
        """アカウント削除からの連鎖用。配下Worldごと論理削除する。"""
        super().soft_delete()
        for world in self.worlds.alive():
            world.soft_delete()
