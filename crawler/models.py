from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=25)
    color = models.CharField(max_length=25)
    def __str__(self):
        return self.name

class Cities(models.Model):
    name = models.CharField(max_length=25)
    slug = models.SmallIntegerField()
    sub_sector_report = models.SmallIntegerField()
    sector_report = models.SmallIntegerField()
    def __str__(self):
        return f"{self.slug}-{self.name}"

class Fount(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Companies(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    city = models.OneToOneField(Cities,on_delete=models.CASCADE)
    sector = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=10)
    phone = models.IntegerField()
    site = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    personels_caount = models.IntegerField()
    fount = models.OneToOneField(Fount,on_delete=models.CASCADE)
    status = models.ManyToManyField(Status)
    note = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.city}--{self.name}"
    class Meta:
        unique_together = ('short_name', 'phone',)

