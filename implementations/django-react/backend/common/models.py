"""全ドメイン共通の抽象モデル。

論理削除の方針（docs/domain/ 各ファイル）:
- deleted_at が NULL なら有効。値ありは削除済みで、期限なく復元できる
- デフォルトマネージャは削除済みも含めて返す（復元UI・管理画面のため）。
  通常の一覧・参照は alive() を明示的に使う
"""

from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def dead(self):
        return self.filter(deleted_at__isnull=False)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(TimeStampedModel):
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteQuerySet.as_manager()

    class Meta:
        abstract = True

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    def soft_delete(self):
        if self.deleted_at is None:
            self.deleted_at = timezone.now()
            self.save(update_fields=["deleted_at", "updated_at"])

    def restore(self):
        if self.deleted_at is not None:
            self.deleted_at = None
            self.save(update_fields=["deleted_at", "updated_at"])
