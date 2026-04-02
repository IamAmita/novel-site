from django.db import models
from apps.users.models import User
from apps.masters.models import MasterClass


class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    title = models.CharField(max_length=200)
    class_id = models.IntegerField()
    target_id = models.BigIntegerField()
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'communications_board'

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    class_id = models.IntegerField()
    target_id = models.BigIntegerField()
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='replies'
    )
    body = models.CharField(max_length=500)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'communications_comment'
        indexes = [
            models.Index(fields=['class_id', 'target_id']),
        ]

    def __str__(self):
        return f'Comment #{self.id}'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    class_id = models.IntegerField()
    target_id = models.BigIntegerField()
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=2000)
    rating = models.IntegerField(default=0)  # 1-5
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'communications_review'
        unique_together = [('user', 'class_id', 'target_id')]

    def __str__(self):
        return f'Review #{self.id}'


class Evaluation(models.Model):
    GOOD = 'good'
    BAD = 'bad'
    TYPE_CHOICES = [(GOOD, 'Good'), (BAD, 'Bad')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluations')
    class_id = models.IntegerField()
    target_id = models.BigIntegerField()
    eval_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=GOOD)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'communications_evaluation'
        unique_together = [('user', 'class_id', 'target_id')]


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    class_id = models.IntegerField()
    target_id = models.BigIntegerField(null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'communications_notification'

    def __str__(self):
        return f'Notification #{self.id}'


class NotificationStatus(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE, related_name='status')
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'communications_notificationstatus'
