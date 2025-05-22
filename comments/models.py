from django.db import models
# from django.contrib.contenttypes.models import


class Comment(models.Model):
    time_create = models.DateTimeField(auto_now_add=True)
    # ip_address = models.IPAddressField()
    # тут скорее нужна связаная модель с наборм комнентов и уникальным хешем на их основе

    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='nested_comments',
        blank=True
    )

    user_name = models.CharField(max_length=30)
    email = models.EmailField()
    home_page = models.URLField(blank=True)
    text = models.TextField(max_length=5000)

    class Meta:
        pass
