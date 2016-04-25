# Create your models here.
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500, null=True)
    file = models.FileField(upload_to='.')
    vcfoutput = models.CharField(max_length=500,null=True)
    snpeffvcfoutput = models.CharField(max_length=500,null=True)
    snpeffhtmloutput = models.CharField(max_length=500,null=True)
    snpeffhtmlmissenseoutput = models.CharField(max_length=500,null=True)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title