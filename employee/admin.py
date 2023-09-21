from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .forms import EmployeeForm, EmployeeChangeForm
from .models import Employee, Task, Project, TeamMember, EmployeeProfile


class CustomUserAdmin(UserAdmin):
    add_form = EmployeeForm
    form = EmployeeChangeForm
    model = Employee
    list_display = ['username', 'password']


admin.site.register(Employee, UserAdmin)
admin.site.register(Task)
admin.site.register(Project)
admin.site.register(TeamMember)
admin.site.register(EmployeeProfile)

