from django.db import models

# Create your models here.


class YandexPage(models.Model):
    title = models.CharField(max_length=250)
    url = models.TextField()
    page = models.IntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
