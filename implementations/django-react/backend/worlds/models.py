"""World（世界観）。

仕様: docs/domain/World.md
Phase 1で見送り: deleted_by（docs/project/Phase1-確定メモ.md §3.1）
"""

from django.core.validators import MaxLengthValidator
from django.db import models

from common.models import SoftDeleteModel


class World(SoftDeleteModel):
    name = models.CharField(max_length=100)
    # DB上はTEXT型のまま、上限1024文字はアプリ側バリデーションで担保（World.md）
    description = models.TextField(blank=True, validators=[MaxLengthValidator(1024)])
    cover_image = models.ImageField(upload_to="world_covers/", null=True, blank=True)
    # PenName.id（サロゲートキー）を参照。Worldを保持するPenNameは削除できない
    # ルールをDBレベルでも PROTECT で担保する
    owner_pen_name = models.ForeignKey(
        "accounts.PenName", on_delete=models.PROTECT, related_name="worlds"
    )

    def __str__(self):
        return self.name

    def soft_delete(self):
        # 配下データ（Setting・作品等）の連鎖論理削除は、該当ドメインの実装時に
        # ここへ追加する（World.md。連鎖復元の範囲はレビュー残課題 2）
        super().soft_delete()
