from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from user.forms import CustomRegistrationForm, CreateGroupForm,AssignRoleForm
from django.contrib import messages
from user.forms import LoginForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from task.models import event,category
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
import datetime


# Create your views here.
def is_admin(user):
    return user.groups.filter(name='Admin').exists()
def is_par(user):
    return user.groups.filter(name='User').exists()
def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(
                request, 'A Confirmation mail sent. Please check your email')
            return redirect('sign-in')

        else:
            print("Form is not valid")
    return render(request, "user/register.html", {"form": form})

def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'login.html', {'form': form})


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')
    


@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related( Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()
    total_par = User.objects.count()

    date=request.GET.get('date','all')
    t = datetime.date.today()
   
    total_event = event.objects.count()
    today = event.objects.filter(date=t)
    up= event.objects.filter(date__gt=t)
    p= event.objects.filter(date__lt=t)
    # today = event.objects.all()
    upcoming = event.objects.filter(date__gt=t).count()
    past= event.objects.filter(date__lt=t).count()
    if(date =='u'):
        today =  event.objects.filter(date__gt=t)

    elif(date =='p'):
        today =  event.objects.filter(date__lt=t)
    
    elif(date=='t'):
        today = event.objects.all()

    comtext={"total_event": total_event,"upcoming": upcoming,"past": past,"total_par":total_par,
        "today": today,"users": users
    }
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'
    # return render(request, 'admin.html', {"users": users})
    return render(request, 'admin.html',comtext )

@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')

@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created successfully")
            return redirect('cg')

    return render(request, 'create_group.html', {'form': form})

@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'group_list.html', {'groups': groups})

@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()  # Remove old roles
            user.groups.add(role)
            messages.success(request, f"User {
                             user.username} has been assigned to the {role.name} role")
            return redirect('admin-dashboard')

    return render(request, 'assign_role.html', {"form": form})


# @user_passes_test(is_par)
@login_required
@user_passes_test(is_par)
def employee_dashboard(request):
    date=request.GET.get('date','all')
    t = datetime.date.today()
    total_event = event.objects.count()
    today = event.objects.filter(date=t)
    up= event.objects.filter(date__gt=t)
    p= event.objects.filter(date__lt=t)
    total_par = User.objects.count()
    # today = event.objects.all()
    upcoming = event.objects.filter(date__gt=t).count()
    past= event.objects.filter(date__lt=t).count()
    if(date =='u'):
        today =  event.objects.filter(date__gt=t)

    elif(date =='p'):
        today =  event.objects.filter(date__lt=t)
    
    elif(date=='t'):
        today = event.objects.all()

    comtext={"total_event": total_event,"upcoming": upcoming,"past": past,"total_par": total_par,
    "today": today
    }

    return render(request, "p.html",comtext)


