import calendar
from datetime import datetime, timedelta, date
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.views import generic
from django.views.generic.dates import MonthMixin

from .decorators import unauthenticated_user, admin_only, allowed_users
from .forms import EmployeeForm, EmployeeChangeForm, TasksForm, TasksForSelfForm, AddProjectForm, AddMemberForm, \
    EmployeeProfileForm, EditTask, ChangeTaskStatus
from .models import Employee, Task, TeamMember, EmployeeProfile, Project
from .utils import Calendar


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.info(request, 'Username OR password is incorrect')

    return render(request, 'employee/login.html', {'messages': messages})


# View to Register Employee
@login_required(login_url='login')
@admin_only
def register_employee(request):
    form = EmployeeForm()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'Employee'
            user.save()
            EmployeeProfile.objects.create(user=user)

            return redirect('register')
    context = {'form': form}
    return render(request, 'employee/register.html', context)


# change password
@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'employee/change_password.html', {
        'form': form
    })


# Calender Class based View
class CalendarView(generic.ListView):
    model = Employee
    template_name = 'employee/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.request.user
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True, employee=employee)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


# View for List Page
@login_required(login_url='login')
def list_page(request):
    tasks = request.user.task_set.all().order_by('-time_created')
    context = {
        'tasks': tasks,
    }
    return render(request, 'employee/list.html', context)


# View for search task Page
@login_required(login_url='login')
def search_task(request):
    if request.method == "GET":
        search = request.GET.get('search')
        if search == '':
            tasks = request.user.task_set.all().order_by('-time_created')
        else:
            tasks = request.user.task_set.all().filter(title__icontains=search)
        context = {
            'tasks': tasks,
        }
        return render(request, 'employee/list.html', context)


# View for Board Page
@login_required(login_url='login')
def board_page(request):
    pending = request.user.task_set.filter(status='To Do')
    total_pending = pending.count
    in_progress = request.user.task_set.filter(status='In Progress')
    total_progress = in_progress.count
    completed = request.user.task_set.filter(status='Done')
    total_completed = completed.count
    context = {
        'pending': pending,
        'total_pending': total_pending,
        'completed': completed,
        'total_completed': total_completed,
        'in_progress': in_progress,
        'total_progress': total_progress,
    }
    return render(request, 'employee/boards.html', context)


# View for Profile Page
@login_required(login_url='login')
def profile_page(request):
    total_task = request.user.task_set.filter(due_date__month=datetime.now().strftime('%m')).count()
    tasks_completed = request.user.task_set.filter(status='Done',  due_date__month=datetime.now().strftime('%m')).count()
    tasks_in_progress = request.user.task_set.filter(status='In Progress',  due_date__month=datetime.now().strftime('%m')).count()
    tasks_to_do = request.user.task_set.filter(status='To Do',  due_date__month=datetime.now().strftime('%m')).count()
    tasks_pending = tasks_to_do + tasks_in_progress
    if total_task != 0:
        context = {
            'total_task': total_task,
            'tasks_completed': tasks_completed,
            'tasks_in_progress': (tasks_in_progress/total_task)*100,
            'tasks_done': (tasks_completed/total_task)*100,
            'tasks_to_do': 100-((tasks_in_progress/total_task)*100)-((tasks_completed/total_task)*100),
            'tasks_pending': tasks_pending,
        }
    else:
        context = {
            'total_task': 0,
            'tasks_completed': 0,
            'tasks_in_progress': 0,
            'tasks_done': 0,
            'tasks_to_do': 0,
            'tasks_pending': 0,
        }
    return render(request, 'employee/profile.html', context)


# View for Updating the profile
@login_required(login_url='login')
def update_profile_page(request):
    employee = request.user
    form = EmployeeChangeForm(instance=employee)

    if request.method == 'POST':
        form = EmployeeChangeForm(request.POST, request.FILES, instance=employee)

        if form.is_valid():
            form.save()
            return redirect('profile')

    context = {'form': form}
    return render(request, 'employee/update_user.html', context)


# View for Updating the profile picture
@login_required(login_url='login')
def update_profile_picture_page(request):
    employee = EmployeeProfile.objects.get(user=request.user)
    form = EmployeeProfileForm(instance=employee)
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('profile')

    context = {'employee': employee, 'form': form}
    return render(request, 'employee/update_profile_picture.html', context)


# View for Create Task Page
@login_required(login_url='login')
def create_task_page(request):
    form = TasksForSelfForm()
    if request.method == 'POST':
        form = TasksForSelfForm(request.POST)
        if form.is_valid():
            task_form = form.save(commit=False)
            task_form.user = request.user
            task_form.assignee = request.user
            task_form.status = 'To Do'
            task_form.save()
            return redirect('create-task')

    context = {'form': form}
    return render(request, 'employee/create_task.html', context)


# View for Create Task for Employee
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Project Manager'])
def create_task_for_employee(request):
    form = TasksForm(request.user)
    if request.method == 'POST':
        form = TasksForm(request.user, request.POST)
        if form.is_valid():
            task_form = form.save(commit=False)
            task_form.assignee = request.user
            task_form.status = 'To Do'
            task_form.save()
            return redirect('create-task-for-employee')

    context = {'form': form}
    return render(request, 'employee/create_task.html', context)


# View to add project
@login_required(login_url='login')
@admin_only
def add_project(request):
    form = AddProjectForm(request.user)
    if request.method == 'POST':
        form = AddProjectForm(request.user, request.POST)
        if form.is_valid():
            name = form.cleaned_data['project_manager']
            pm = Employee.objects.get(username=name)
            pm.role = 'Project Manager'
            pm.save()
            project_form = form.save(commit=False)
            project_form.assignee = request.user
            project_form.project_manager = pm
            project_form.save()
            TeamMember.objects.create(user=pm, project=project_form)
            return redirect('project-list')
    context = {'form': form}
    return render(request, 'employee/add_project.html', context)


# View to add project
@login_required(login_url='login')
@admin_only
def delete_project(request, project_id):
    project = Project.objects.get(id=project_id)
    pm = project.project_manager
    pm.role = 'Employee'
    pm.save()
    TeamMember.objects.filter(project=project).delete()
    project.delete()
    return redirect('project-list')


# View for displaying project details to pm and employee
@login_required(login_url='login')
def project_details(request):
    project = TeamMember.objects.get(user=request.user).project
    members = TeamMember.objects.filter(project=project).exclude(user=request.user)
    context = {'project': project,
               'members': members}
    return render(request, 'employee/project_details.html', context)


# View for displaying project details to admin
@login_required(login_url='login')
def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    members = TeamMember.objects.filter(project=project).exclude(user=project.project_manager)
    context = {'project': project,
               'members': members}
    return render(request, 'employee/project_details.html', context)


# View to add members
@login_required(login_url='login')
@allowed_users(allowed_roles=['Project Manager'])
def add_members(request):
    project = TeamMember.objects.get(user=request.user).project
    members = TeamMember.objects.filter(project=project).exclude(user=request.user)
    form = AddMemberForm(request.user)
    if request.method == 'POST':
        form = AddMemberForm(request.user, request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.project = TeamMember.objects.get(user=request.user).project
            form.save()
            return redirect('project-details')
    context = {'form': form,
               'project': project,
               'members': members
               }
    return render(request, 'employee/add-members.html', context)


# details of team members
@login_required(login_url='login')
@allowed_users(allowed_roles=['Project Manager'])
def member_details(request):
    project = TeamMember.objects.get(user=request.user).project
    members = TeamMember.objects.filter(project=project).exclude(user=request.user)
    context = {'members': members}
    return render(request, 'employee/team_member_details.html', context)


# details of employees
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def employee_details(request):
    employees = Employee.objects.all().exclude(role='Admin').order_by('username')
    context = {'employees': employees}
    return render(request, 'employee/employee_details.html', context)


# View to track members progress
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Project Manager'])
def track_members_progress(request, username):
    employee = Employee.objects.get(username=username)
    tasks = employee.task_set.filter(assignee=request.user).order_by('-time_created')
    total_task = employee.task_set.filter(assignee=request.user).count()
    tasks_completed = employee.task_set.filter(status='Done', assignee=request.user).count()
    tasks_in_progress = employee.task_set.filter(status='In Progress', assignee=request.user).count()
    tasks_to_do = employee.task_set.filter(status='To Do', assignee=request.user).count()
    tasks_pending = tasks_to_do + tasks_in_progress
    if total_task != 0:
        context = {
            'employee': employee,
            'tasks': tasks,
            'total_task': total_task,
            'tasks_completed': tasks_completed,
            'tasks_in_progress': (tasks_in_progress / total_task) * 100,
            'tasks_done': (tasks_completed / total_task) * 100,
            'tasks_to_do': 100 - ((tasks_in_progress / total_task) * 100) - ((tasks_completed / total_task) * 100),
            'tasks_pending': tasks_pending,
        }
    else:
        context = {
            'employee': employee,
            'tasks': tasks,
            'total_task': 0,
            'tasks_completed': 0,
            'tasks_in_progress': 0,
            'tasks_done': 0,
            'tasks_to_do': 0,
            'tasks_pending': 0,
        }
    return render(request, 'employee/track_task.html', context)


# view to display task details
@login_required(login_url='login')
def task_details(request, task_id):
    task = request.user.task_set.get(id=task_id)
    context = {
        'task': task,
    }
    return render(request, 'employee/task_details.html', context)


# view to edit task details
@login_required(login_url='login')
def edit_task_details(request, task_id):
    task = request.user.task_set.get(id=task_id)
    form = EditTask(instance=task)
    if request.method == 'POST':
        form = EditTask(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task-details',task.id)

    context = {'task': task, 'form': form}
    return render(request, 'employee/edit_task.html', context)


# view to change task status
@login_required(login_url='login')
def change_task_status(request, task_id):
    task = request.user.task_set.get(id=task_id)
    form = ChangeTaskStatus(instance=task)
    if request.method == 'POST':
        form = ChangeTaskStatus(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task-details', task.id)

    context = {'task': task, 'form': form}
    return render(request, 'employee/change_status.html', context)


# list of projects
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def list_of_projects(request):
    projects = Project.objects.filter(assignee=request.user)
    context = {'projects': projects}
    return render(request, 'employee/projects_list.html', context)


# Logout View
@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')

