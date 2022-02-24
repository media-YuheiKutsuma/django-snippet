from django.db import models
from django.conf import settings
# Create your models here.

class Snippet(models.Model):
    title = models.CharField('タイトル', max_length=128)
    code = models.TextField('コード', blank=True)
    description = models.TextField('説明', blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    verbose_name="投稿者",
                                    on_delete=models.CASCADE)
    created_at = models.DateTimeField("投稿日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'snippets'

class Comment(models.Model):
    text = models.TextField('本文', blank=False)
    commented_at = models.DateTimeField('投稿日', auto_now_add=True)
    commented_to = models.ForeignKey(Snippet, verbose_name='スニペット', on_delete=models.CASCADE)
    commented_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='投稿者', on_delete=models.CASCADE)

    def __str__(self):
        return self.commented_to.title


class Tag(models.Model):
    name = models.CharField("タグ名", max_length=32)
    snippets = models.ManyToManyField(Snippet, related_name='tags', related_query_name='tags')

    class Meta:
        db_table = "tags"
    def __str__(self):
        return f'{self.pk} {self.name}'