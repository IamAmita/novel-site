from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import World
from .serializers import WorldSerializer


class WorldViewSet(viewsets.ModelViewSet):
    """自分のWorldのCRUD。

    - 一覧はデフォルトで有効なWorldのみ・更新日時の新しい順（SC-08）
    - `?include_deleted=1` で削除済みも含める（「削除済みを表示」トグル）
    - 削除は論理削除、`POST /:id/restore` で復元
    """

    serializer_class = WorldSerializer

    def get_queryset(self):
        qs = World.objects.filter(
            owner_pen_name__user=self.request.user
        ).select_related("owner_pen_name")
        include_deleted = self.request.query_params.get("include_deleted") == "1"
        if self.action == "list" and not include_deleted:
            qs = qs.alive()
        return qs.order_by("-updated_at")

    def perform_destroy(self, instance):
        instance.soft_delete()

    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        world = self.get_object()
        world.restore()
        return Response(self.get_serializer(world).data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        # 検索: World名の部分一致（説明文は対象外、SC-08）
        queryset = self.get_queryset()
        q = request.query_params.get("q")
        if q:
            queryset = queryset.filter(name__icontains=q)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
