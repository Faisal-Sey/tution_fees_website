from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.shortcuts import reverse
# Create your models here.


class Details(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    studentid = models.CharField(max_length=100, blank=True, null=True)
    fees = models.IntegerField(blank=True, null=True)
    amount_paid = models.IntegerField(default=0)
    pin = models.IntegerField(blank=True, null=True)
    balance = models.IntegerField()
    created = models.DateTimeField(auto_now=True)
    Slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.Slug:
            self.Slug = slugify(self.studentid)
        super(Details, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("detailview", args=[str(self.Slug)])

    def add_student_url(self):
        return reverse("add")

    class Meta:
        verbose_name_plural = "Details"


class Transaction(models.Model):
    fullname = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now=True)
    amount = models.FloatField()
    reference = models.CharField(max_length=100, blank=True, null=True)
    studentid = models.CharField(max_length=100, blank=True, null=True)
    network = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=10, blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.fullname


class StudentList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    transactions = models.ManyToManyField(Transaction)
    details = models.ForeignKey(Details, on_delete=models.CASCADE)
    Slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.Slug:
            self.Slug = slugify(self.user.studentid)
        super(StudentList, self).save(*args, **kwargs)

