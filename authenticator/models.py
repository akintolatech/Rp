from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django import forms


class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)

    # students_registered = models.ManyToManyField(Student, related_name='written_tests')
    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    # subject = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} - {self.subject}"


class Student(models.Model):
    name = models.CharField(max_length=255, unique=True)
    photo = models.ImageField(upload_to='photo/')
    student_no = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=100, default="0")
    year = models.CharField(max_length=255, default="2023")
    form = models.CharField(max_length=255, default="REM 6")
    registered_subject = models.ManyToManyField(Subject)
    avg = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_score = models.IntegerField(default=0)
    total_remark = models.CharField(max_length=255, default="FAIL")
    coordinator_remark = models.CharField(max_length=500, default="Poor result, you failed. Ensure you work very hard next Semester")
    total_grade = models.CharField(max_length=2, default="F")
    qr_code = models.CharField(max_length=255, default="url")

    def __str__(self):
        return self.name


class Results(models.Model):
    # student = models.CharField(max_length=255)
    # student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default=0)
    cat1 = models.IntegerField()
    cat2 = models.IntegerField()
    exam = models.IntegerField()
    total = models.IntegerField()
    grade = models.CharField(max_length=2)
    remark = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.student.name} - {self.subject}"
