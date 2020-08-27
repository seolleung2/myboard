from django.db import models

class Tag(models.Model):
    name        = models.CharField(max_length=100, verbose_name="태그")
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="작성일")

    def __str__(self):
        return self.name

    class Meta:
        db_table            = 'tags'
        verbose_name        = '게시판태그'
        verbose_name_plural = '게시판태그'
