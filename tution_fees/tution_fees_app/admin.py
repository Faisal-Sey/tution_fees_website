from django.contrib import admin
from .models import Details, Transaction, StudentList
# Register your models here.

admin.site.register(Details)
admin.site.register(Transaction)
admin.site.register(StudentList)