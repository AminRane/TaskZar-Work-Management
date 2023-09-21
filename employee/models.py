from django.contrib.auth.models import AbstractUser, User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.datetime_safe import datetime


def validate_due_date(value):
    if value >= datetime.date(timezone.now()):
        return value
    else:
        raise ValidationError("Enter a valid date")


class TeamMember(models.Model):
    user = models.ForeignKey('Employee', blank=True, null=True, on_delete=models.SET_NULL)
    project = models.ForeignKey('Project', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.user.username}  {self.project.title}'


class Project(models.Model):
    title = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    assignee = models.ForeignKey('employee.Employee', null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name='project_assignee')
    project_manager = models.ForeignKey('employee.Employee', null=True, on_delete=models.SET_NULL,
                                        related_name='project_manager')
    due_date = models.DateField(null=True, blank=True, validators=[validate_due_date])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Employee(AbstractUser):
    username = models.CharField(unique=True, max_length=30, blank=True, null=True)
    first_name = models.CharField(max_length=15, blank=True, null=True)
    last_name = models.CharField(max_length=15, blank=True, null=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    ROLE = [
        ('Admin', 'Admin'),
        ('Project Manager', 'Project Manager'),
        ('Employee', 'Employee')
    ]
    role = models.CharField(max_length=30, choices=ROLE, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    Gender = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    gender = models.CharField(max_length=30, choices=Gender, null=True, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["first_name", "last_name", "role"]

    def is_part_of_project(self):
        return False if (TeamMember.objects.get(user=self) is None) else True

    def is_admin(self):
        return True if (self.role == "Admin") else False

    def is_project_manager(self):
        return True if (self.role == "Project Manager") else False

    def is_member(self):
        return True if (self.role in ['Project Manager', 'Employee']) else False


class EmployeeProfile(models.Model):
    user = models.OneToOneField(Employee, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='user-profile-default.png', upload_to='profile_pictures')


class Task(models.Model):
    user = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    assignee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL, related_name='assignee')
    title = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, validators=[validate_due_date])

    STATUS = [
        ('Done', 'Done'),
        ('In Progress', 'In Progress'),
        ('To Do', 'To Do')
    ]
    PRIORITY = [
        ('Critical', 'Critical'),
        ('Highest', 'Highest'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
        ('Lowest', 'Lowest'),
    ]
    priority = models.CharField(max_length=200, choices=PRIORITY, null=True, blank=True)
    status = models.CharField(max_length=200, choices=STATUS, null=True, blank=True, default='Pending')
    time_completed = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}: {self.title}'

    def is_self(self):
        return True if (self.assignee == self.user) else False

    def is_to_do(self):
        return True if (self.status == 'To Do') else False

    def is_in_progress(self):
        return True if (self.status == 'In Progress') else False

    def is_completed(self):
        return True if (self.status == 'Done') else False

    def is_critical(self):
        return True if (self.priority == 'Critical') else False

    def is_highest(self):
        return True if (self.priority == 'Highest') else False

    def is_medium(self):
        return True if (self.priority == 'Medium') else False

    def is_low(self):
        return True if (self.priority == 'Low') else False

    def is_lowest(self):
        return True if (self.priority == 'Lowest') else False
