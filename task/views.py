from django.shortcuts import render,redirect
from django.http import HttpResponse
from task.forms import eventform, categoryform
from task.models import event, category
from django.contrib import messages
from django.db.models import Count,Q,Max,Min
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required


def m(request):
    return render(request,"main.html")
def is_manager(user):
    return user.groups.filter(name='Manager').exists()
def is_par(user):
    return user.groups.filter(name='User').exists()
def is_admin(user):
    return user.groups.filter(name='Admin').exists()
def home(request):
    all = event.objects.all()
    cate=category.objects.all()
    search = request.GET.get("search")
    date =  request.GET.get("date")
    dat =  request.GET.get("dat")
    cat =  request.GET.get("cat")
    if search:
        all = event.objects.filter(
            Q(name__icontains=search) | Q(location__icontains=search)
        )
    if date and dat and cat:
        all=event.objects.filter(
            date__range=(date,dat),category=cat
        )

    context={"all":all,"cate":cate}
    return render(request,"home.html",context)
@user_passes_test(is_manager, login_url='no-permission')
def db(request):
   
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

    comtext={"total_event": total_event,"upcoming": upcoming,"past": past,"total_par":total_par,
        "today": today
    }
    return render(request, "dashboard.html",comtext) 
@login_required
@permission_required("task.add_event", login_url='no-permission')    
def event_create(request):
    fm1 = eventform()
    
    if request.method == "POST":
        fm1 = eventform(request.POST,request.FILES)
        
        if fm1.is_valid():
           fm1.save()
           messages.success(request,"event created successfully")
           return redirect("event_create")
    context={ "fe": fm1, "title": "Create Event"}
    
    return render( request,"fm1.html",context)
@login_required
@permission_required("task.add_category", login_url='no-permission')
def category_create(request):
    fm1 = categoryform()
    
    if request.method == "POST":
        fm1 = categoryform(request.POST)
        
        if fm1.is_valid():
           fm1.save()
           messages.success(request,"category created successfully")
           return redirect("category_create")
    context={ "fe": fm1, "title": "Create category"}
    
    return render( request,"fm1.html",context)

# def participant_create(request):
#     fm1 = participantform()
    
#     if request.method == "POST":
#         fm1 = participantform(request.POST)
        
#         if fm1.is_valid():
#            fm1.save()
#            messages.success(request,"category created successfully")
#            return redirect("participant_create")
#     context={ "fe": fm1, "title": "participant category"}
    
#     return render( request,"fm1.html",context)

@login_required
@permission_required("task.change_event", login_url='no-permission')
def event_update(request,id):
    ev=event.objects.get(id=id)
    fm1 = eventform(instance=ev)
    if request.method == "POST":
        fm1 = eventform(request.POST,instance=ev)
        if fm1.is_valid():
           fm1.save()
           messages.success(request,"event updated successfully")
           return redirect("event_update", id)
    context={ "fe": fm1,"title": "Update Event"}
    
    return render( request,"fm1.html",context)
@login_required
@permission_required("task.change_category", login_url='no-permission')
def category_update(request,id):
    ev=category.objects.get(id=id)
    fm1 = categoryform(instance=ev)
    if request.method == "POST":
        fm1 = categoryform(request.POST,instance=ev)
        if fm1.is_valid():
           fm1.save()
           messages.success(request,"event updated successfully")
           return redirect("category_update", id)
    context={ "fe": fm1,"title": "Update Category"}
    
    return render( request,"fm1.html",context)

# def participant_update(request,id):
#     ev=participant.objects.get(id=id)
#     fm1 = participantform(instance=ev)
#     if request.method == "POST":
#         fm1 = participantform(request.POST,instance=ev)
#         if fm1.is_valid():
#            fm1.save()
#            messages.success(request,"event updated successfully")
#            return redirect("participant_update", id)
#     context={ "fe": fm1,"title": "Update participant"}
    
#     return render( request,"fm1.html",context)

@login_required
@permission_required("task.delete_event", login_url='no-permission')
def event_delate(request,id):
    if request.method == "POST":
        ev=event.objects.get(id=id)
        ev.participent.clear()
        ev.delete()
        messages.success(request,"event deleted  successfully")
        return redirect("sae")
    else:
        return redirect("sae")
@login_required
@permission_required("task.delete_category", login_url='no-permission')
def category_delate(request,id):
    if request.method == "POST":
        ev=category.objects.get(id=id)
        ev.delete()
        messages.success(request,"event deleted  successfully")
        return redirect("sac")
    else:
        return redirect("sac")

# def participant_delate(request,id):
#     if request.method == "POST":
#         ev=participant.objects.get(id=id)
#         ev.delete()
#         messages.success(request,"event deleted  successfully")
#         return redirect("sap")
#     else:
#         return redirect("sap")
@login_required
@permission_required("task.view_event", login_url='no-permission')
def sae(request):
    all = event.objects.all()
    context={"all":all,"title":"Delate and Update"}
    return render(request,"showe.html",context)
    
@login_required
@permission_required("task.view_category", login_url='no-permission')
def sac(request):
    all = category.objects.all()
    context={"all":all,"title":"Delate and Update"}
    return render(request,"showc.html",context)
# def sap(request):
#     all = participant.objects.all()
#     context={"all":all,"title":"Delate and Update"}
#     return render(request,"showp.html",context)
@login_required
def detail(request,id):
    e = event.objects.select_related("category").prefetch_related("participent").get(id=id)
    ec=event.objects.annotate(pc=Count("participent")).get(id=id)
    context={"e":e,"ec":ec,"title":"Event detail"}
    return render(request,"view.html",context)

@login_required
@user_passes_test(is_par, login_url='no-permission')
def rsvp(request, event_id, user_id):
    even =event.objects.get(id=event_id)
    user = User.objects.get(id=user_id)

    if user in even.participent.all():
        messages.error(request, f"{user.username} has already RSVP to {even.name}.")
    else:
        even.participent.add(user)
        messages.success(request, f"{user.username} successfully RSVP to {even.name}!")

    return redirect("p-dashboard")
def no_permission(request):
    return render(request, 'no.html')

@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('db')
    elif is_par(request.user):
        return redirect('p-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')

    return redirect('no-permission')





