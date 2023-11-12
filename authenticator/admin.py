from django.contrib import admin
from .models import CustomUser, Subject, Student, Results

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Results)