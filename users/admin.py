
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import Employee, User

admin.site.register(Employee)
admin.site.register(User, UserAdmin)