from django.db import models

# Create your models here.

class Detail(models.Model):
    Surname = models.CharField(max_length=100)
    Middle_name = models.CharField(max_length=100, blank=True, null=True)
    First_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    Email = models.EmailField(max_length=255)
    Number = models.CharField(max_length=50)
    DOB = models.DateTimeField()
    Amount_paid = models.IntegerField(blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.First_name