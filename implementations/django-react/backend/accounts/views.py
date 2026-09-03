from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView


@method_decorator(ensure_csrf_cookie, name="get")
class CsrfView(APIView):
    """フロントエンドがCSRFクッキーを受け取るためのエンドポイント。"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"detail": "ok"})

from .models import PenName
from .serializers import PenNameSerializer, RegisterSerializer, UserSerializer


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # メール確認は行わず、登録成功で即ログイン状態にする（SC-01）
        login(request, user)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = authenticate(
            request,
            username=request.data.get("identifier"),
            password=request.data.get("password"),
        )
        if user is None:
            return Response(
                {"detail": "メールアドレス（またはユーザーID）かパスワードが違います。"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        login(request, user)
        return Response(UserSerializer(user).data)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        user = request.user
        logout(request)
        user.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PenNameViewSet(viewsets.ModelViewSet):
    serializer_class = PenNameSerializer

    def get_queryset(self):
        return self.request.user.pen_names.alive().order_by("created_at")

    def destroy(self, request, *args, **kwargs):
        pen_name = self.get_object()
        # 削除済みWorldの所有者も削除不可（復元不能を防ぐ）
        if pen_name.has_worlds():
            return Response(
                {"detail": "Worldを保持しているため削除できません。"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        pen_name.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
