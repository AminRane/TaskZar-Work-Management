from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


class EmployeeForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'password1', 'password2']


class EmployeeProfileForm(ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ['profile_picture']


class SearchUserForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['username']


class EmployeeChangeForm(UserChangeForm):
    class Meta:
        model = Employee
        fields = ['username', 'first_name', 'last_name', 'email', 'gender']


class TasksForSelfForm(ModelForm):
    class Meta:
        model = Task
        exclude = ['user', 'assignee', 'status']


class TasksForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(TasksForm, self).__init__(*args, **kwargs)
        if user.role == 'Admin':
            self.fields['user'].queryset = Employee.objects.filter(role__in=['Project Manager', 'Employee'])
        if user.role == 'Project Manager':
            project = TeamMember.objects.get(user=user).project
            self.fields['user'].queryset = Employee.objects.filter(role='Employee', teammember__project=project)

    class Meta:
        model = Task
        exclude = ['assignee', 'status']


class EditTask(ModelForm):
    class Meta:
        model = Task
        exclude = ['status', 'assignee', 'user']


class ChangeTaskStatus(ModelForm):
    class Meta:
        model = Task
        fields = ['status']


class AddProjectForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(AddProjectForm, self).__init__(*args, **kwargs)
        self.fields['project_manager'].queryset = Employee.objects.filter(role='Employee', teammember__project=None)

    class Meta:
        model = Project
        exclude = ['assignee', 'members']


class AddMemberForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(AddMemberForm, self).__init__(*args, **kwargs)
        project = TeamMember.objects.get(user=user).project
        self.fields['user'].queryset = Employee.objects.filter(role='Employee').exclude(teammember__project=project)

    class Meta:
        model = TeamMember
        fields = ['user']
