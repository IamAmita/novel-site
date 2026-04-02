from django.db import models


class Category(models.Model):
    """カテゴリ（階層構造）"""
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children'
    )
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    sort_order = models.IntegerField(default=0)
    is_official = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'common_category'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """タグ"""
    name = models.CharField(max_length=50, unique=True)
    is_official = models.BooleanField(default=False)
    use_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'common_tag'

    def __str__(self):
        return self.name


class Template(models.Model):
    """通知・メッセージテンプレート"""
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'common_template'

    def __str__(self):
        return self.name
