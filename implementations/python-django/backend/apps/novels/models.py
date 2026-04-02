from django.db import models
from apps.users.models import User, SoftDeleteManager
from apps.common.models import Category, Tag
from apps.masters.models import MasterStatus


class Novel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='novels')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, through='NovelTag', related_name='novels')
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        db_table = 'novels_novel'

    def __str__(self):
        try:
            return self.info.title
        except Exception:
            return f'Novel #{self.id}'


class NovelInfo(models.Model):
    novel = models.OneToOneField(Novel, on_delete=models.CASCADE, related_name='info')
    title = models.CharField(max_length=100)
    synopsis = models.TextField(max_length=1000, blank=True, null=True)
    cover_image_url = models.URLField(max_length=500, blank=True, null=True)
    is_r18 = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'novels_novelinfo'

    def __str__(self):
        return self.title


class NovelStatus(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='status_history')
    status = models.ForeignKey(MasterStatus, on_delete=models.PROTECT)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'novels_novelstatus'


class NovelTag(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'novels_noveltag'
        unique_together = [('novel', 'tag')]


class Section(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=200)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'novels_section'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.title


class SectionStatus(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='status_history')
    status = models.ForeignKey(MasterStatus, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'novels_sectionstatus'


class Episode(models.Model):
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='episodes')
    section = models.ForeignKey(
        Section, null=True, blank=True, on_delete=models.SET_NULL, related_name='episodes'
    )
    episode_number = models.IntegerField()
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=50000)
    sort_order = models.IntegerField(default=0)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        db_table = 'novels_episode'
        unique_together = [('novel', 'episode_number')]
        ordering = ['sort_order', 'episode_number']

    def __str__(self):
        return f'#{self.episode_number} {self.title}'


class EpisodeStatus(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='status_history')
    status = models.ForeignKey(MasterStatus, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'novels_episodestatus'
