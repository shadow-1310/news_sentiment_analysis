from django.db import models

# Create your models here.
class article_gnews(models.Model):
    id = models.IntegerField(primary_key=True)
    method = models.CharField(max_length=30, default="")
    keyword = models.CharField(max_length=30,default="")
    headline = models.TextField(default="")
    publish_date = models.DateField()
    publish_time = models.TimeField()
    source = models.TextField(default="")
    article = models.TextField(default="")
    summary = models.TextField(default="")
    sentiment = models.CharField(max_length=30, default="")
    confidence = models.FloatField(default=0)
    url = models.TextField(default="")