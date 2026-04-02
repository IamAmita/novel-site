from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
    User, UserProfile, UserStatus, UserAction, UserPermission,
    Follow, Block, DirectMessage, LoginHistory, TwoFactorAuth,
    TwoFactorAuthCode, AuthorPermissionRequest
)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['display_name', 'icon_url', 'biography', 'website_url', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'email_verified_at', 'created_at', 'updated_at', 'profile']
        read_only_fields = ['email_verified_at', 'created_at', 'updated_at']


class UserPublicSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'profile']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    display_name = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'display_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password': 'パスワードが一致しません。'})
        return attrs

    def create(self, validated_data):
        display_name = validated_data.pop('display_name')
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        UserProfile.objects.create(user=user, display_name=display_name)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({'new_password': '新しいパスワードが一致しません。'})
        return attrs


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatus
        fields = ['id', 'user', 'status', 'reason', 'note', 'created_at']
        read_only_fields = ['created_at']


class UserActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAction
        fields = ['id', 'user', 'action', 'class_id', 'target_id', 'created_at']
        read_only_fields = ['created_at']


class UserPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermission
        fields = ['id', 'user', 'permission', 'granted_by', 'granted_at']
        read_only_fields = ['granted_at']


class FollowSerializer(serializers.ModelSerializer):
    followee_info = UserPublicSerializer(source='followee', read_only=True)
    follower_info = UserPublicSerializer(source='follower', read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followee', 'follower_info', 'followee_info', 'created_at', 'deleted_at']
        read_only_fields = ['created_at']


class BlockSerializer(serializers.ModelSerializer):
    blocked_info = UserPublicSerializer(source='blocked', read_only=True)

    class Meta:
        model = Block
        fields = ['id', 'blocker', 'blocked', 'blocked_info', 'created_at']
        read_only_fields = ['created_at']


class DirectMessageSerializer(serializers.ModelSerializer):
    sender_info = UserPublicSerializer(source='sender', read_only=True)
    receiver_info = UserPublicSerializer(source='receiver', read_only=True)

    class Meta:
        model = DirectMessage
        fields = ['id', 'sender', 'receiver', 'sender_info', 'receiver_info', 'body', 'is_read', 'created_at']
        read_only_fields = ['sender', 'is_read', 'created_at']


class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistory
        fields = ['id', 'user', 'ip_address', 'user_agent', 'created_at']
        read_only_fields = ['created_at']


class TwoFactorAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwoFactorAuth
        fields = ['id', 'user', 'method', 'is_enabled', 'created_at', 'updated_at']
        read_only_fields = ['secret', 'created_at', 'updated_at']


class AuthorPermissionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorPermissionRequest
        fields = [
            'id', 'user', 'reason', 'status', 'reviewed_by',
            'reviewed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'status', 'reviewed_by', 'reviewed_at', 'created_at', 'updated_at']


class AuthorPermissionRequestReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorPermissionRequest
        fields = ['status', 'reviewed_by', 'reviewed_at']
