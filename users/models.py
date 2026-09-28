from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    age = models.PositiveIntegerField(default=18)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    position = models.ForeignKey('app.Positions', on_delete=models.CASCADE, related_name='employees')
    shift = models.ManyToManyField('app.Shifts', blank=True, related_name='employees')
    library=models.ForeignKey('app.Libraries', on_delete=models.CASCADE, related_name='employees',null=True,blank=True)

    def __str__(self):
        return self.user.username