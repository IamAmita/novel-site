from django.contrib.auth.models import AbstractUser
from django.db import models


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users_user'

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=50)
    icon_url = models.URLField(max_length=500, blank=True, null=True)
    biography = models.TextField(max_length=1000, blank=True, null=True)
    website_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users_userprofile'

    def __str__(self):
        return self.display_name


class UserStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='statuses')
    status = models.ForeignKey('masters.MasterStatus', on_delete=models.PROTECT)
    reason = models.ForeignKey('masters.MasterReason', null=True, blank=True, on_delete=models.SET_NULL)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_userstatus'


class UserAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions')
    action = models.ForeignKey('masters.MasterAction', on_delete=models.PROTECT)
    class_id = models.IntegerField()
    target_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_useraction'
        unique_together = [('user', 'action', 'class_id', 'target_id')]


class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permissions_list')
    permission = models.ForeignKey('masters.MasterPermission', on_delete=models.PROTECT)
    granted_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='granted_permissions'
    )
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_userpermission'
        unique_together = [('user', 'permission')]


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'users_follow'
        unique_together = [('follower', 'followee')]


class Block(models.Model):
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocking')
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_block'
        unique_together = [('blocker', 'blocked')]


class DirectMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    body = models.TextField(max_length=2000)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_directmessage'


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_histories')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_loginhistory'


class TwoFactorAuth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='two_factor_auth')
    method = models.ForeignKey('masters.MasterTwoFactorMethod', on_delete=models.PROTECT)
    secret = models.CharField(max_length=200)
    is_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users_twofactorauth'


class TwoFactorAuthCode(models.Model):
    two_factor_auth = models.ForeignKey(TwoFactorAuth, on_delete=models.CASCADE, related_name='codes')
    code = models.CharField(max_length=10)
    is_backup = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_twofactorauthcode'


class AuthorPermissionRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, '審査中'),
        (STATUS_APPROVED, '承認'),
        (STATUS_REJECTED, '却下'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author_request')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    reviewed_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviewed_requests'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users_authorpermissionrequest'
