from django.db import models
from apps.users.models import User, SoftDeleteManager
from apps.common.models import Category, Tag
from apps.masters.models import MasterStatus, MasterClass


class World(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='worlds')
    novel = models.ForeignKey(
        'novels.Novel', null=True, blank=True, on_delete=models.SET_NULL, related_name='worlds'
    )
    categories = models.ManyToManyField(Category, through='WorldCategory', related_name='worlds')
    tags = models.ManyToManyField(Tag, through='WorldTag', related_name='worlds')
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        db_table = 'worlds_world'

    def __str__(self):
        try:
            return self.info.title
        except Exception:
            return f'World #{self.id}'


class WorldInfo(models.Model):
    world = models.OneToOneField(World, on_delete=models.CASCADE, related_name='info')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2000, blank=True, null=True)
    cover_image_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'worlds_worldinfo'

    def __str__(self):
        return self.title


class WorldStatus(models.Model):
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name='status_history')
    status = models.ForeignKey(MasterStatus, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'worlds_worldstatus'


class WorldCategory(models.Model):
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'worlds_worldcategory'
        unique_together = [('world', 'category')]


class WorldTag(models.Model):
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'worlds_worldtag'
        unique_together = [('world', 'tag')]


class Setting(models.Model):
    world = models.ForeignKey(World, on_delete=models.CASCADE, related_name='settings')
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children'
    )
    name = models.CharField(max_length=100)
    class_id = models.ForeignKey(MasterClass, on_delete=models.PROTECT, db_column='class_id')
    sort_order = models.IntegerField(default=0)
    is_public = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        db_table = 'worlds_setting'

    def __str__(self):
        return self.name


class SettingField(models.Model):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE, related_name='fields')
    label = models.CharField(max_length=100)
    value = models.TextField(blank=True, null=True)
    data = models.JSONField(null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'worlds_settingfield'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.label


class SettingRelation(models.Model):
    from_setting = models.ForeignKey(Setting, on_delete=models.CASCADE, related_name='relations_from')
    to_setting = models.ForeignKey(Setting, on_delete=models.CASCADE, related_name='relations_to')
    relation_label = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'worlds_settingrelation'
        unique_together = [('from_setting', 'to_setting', 'relation_label')]
