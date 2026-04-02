from django.db import models
from apps.users.models import User
from apps.masters.models import MasterTable, MasterOperation, MasterReason


class Report(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_RESOLVED = 'resolved'
    STATUS_DISMISSED = 'dismissed'
    STATUS_CHOICES = [
        (STATUS_PENDING, '未対応'),
        (STATUS_RESOLVED, '解決'),
        (STATUS_DISMISSED, '却下'),
    ]
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    class_id = models.IntegerField()
    target_id = models.BigIntegerField()
    reason = models.ForeignKey(MasterReason, on_delete=models.PROTECT)
    body = models.TextField(max_length=1000, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    reviewed_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviewed_reports'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'administration_report'

    def __str__(self):
        return f'Report #{self.id}'


class OperationHistory(models.Model):
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='operation_histories'
    )
    table = models.ForeignKey(MasterTable, on_delete=models.PROTECT)
    target_id = models.BigIntegerField()
    operation = models.ForeignKey(MasterOperation, on_delete=models.PROTECT)
    before_data = models.JSONField(null=True, blank=True)
    after_data = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'administration_operationhistory'
        indexes = [
            models.Index(fields=['table', 'target_id']),
        ]

    def __str__(self):
        return f'OperationHistory #{self.id}'


class WorkStat(models.Model):
    novel = models.OneToOneField('novels.Novel', on_delete=models.CASCADE, related_name='stats')
    view_count = models.BigIntegerField(default=0)
    episode_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    good_count = models.IntegerField(default=0)
    bookmark_count = models.IntegerField(default=0)
    rating_sum = models.BigIntegerField(default=0)
    rating_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'administration_workstat'

    def __str__(self):
        return f'WorkStat for Novel #{self.novel_id}'

    @property
    def rating_avg(self):
        if self.rating_count == 0:
            return 0
        return round(self.rating_sum / self.rating_count, 1)
