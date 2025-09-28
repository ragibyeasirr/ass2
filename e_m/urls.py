"""
URL configuration for e_m project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from task.views import m,home,db,event_create,category_create,sae,sac,event_update,category_update,event_delate,category_delate,detail,rsvp,dashboard,no_permission

from user.views import sign_up, sign_in,activate_user,create_group,admin_dashboard, group_list,sign_out,assign_role,employee_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('m/',m),
    path('',home,name="home"),
    path('db/',db,name="db"),
    path('c/',event_create,name="event_create"),
    path('cc/',category_create,name="category_create"),
    #path('ccc/', participant_create,name="participant_create"),
    path('sae/', sae,name="sae"),
    path('sac/', sac,name="sac"),
    #path('sap/', sap,name="sap"),
    path('event_update/<int:id>', event_update,name="event_update"),
    path('category_update/<int:id>', category_update,name="category_update"),
    #path('participant_update/<int:id>', participant_update,name="participant_update"),
    path('event_delate/<int:id>',event_delate,name="event_delate"),
    path('category_delate/<int:id>',category_delate,name="category_delate"),
    path('no-permission/', no_permission, name='no-permission'),
    path('detail/<int:id>',detail,name="detail"),
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
     path('create-group/', create_group, name='cg'),
    path('dashboard/', admin_dashboard, name='admin-dashboard'),
    path('group-list/', group_list, name='group-list'),
    path('sign-out/', sign_out, name='logout'),
    path('dashboard/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('ppd/', employee_dashboard, name='p-dashboard'),
    path("event/<int:event_id>/rsvp/<int:user_id>/", rsvp, name="rsvp_event"),
    path('dd', dashboard, name='dashboard')
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)