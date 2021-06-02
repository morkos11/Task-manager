"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from taskmanager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.view_tasks,name='view_tasks'),
    path('LogIn',views.log_in,name='login'),
    path('SignUp',views.signup_form_Page,name='signup'),
    path('LogOut',views.log_out,name='log_out'),
    path('Update_password',views.change_password,name='change_password'),
    path('Update_user_pic/<slug>', views.Update_user.as_view(), name='update_user'),
    path('AddTask',views.add_task,name='add_task'),
    path('delete_all',views.delete_all,name='delete_all'),
    path('deletecompleted', views.deleteCompleted, name='deletecompleted'),
    path('completed/<task_no>', views.completedTask, name='completed'),
    
    path('Reset_Password',auth_views.PasswordResetView.as_view(template_name='reset_password/password_reset.html'),name='reset_password'),
    path('Reset_Password_Sent', auth_views.PasswordResetDoneView.as_view(template_name='reset_password/password_reset_done.html'), name='password_reset_done'),
    path('Reset_Password/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='reset_password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('Reset_Password_Complete', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password/password_reset_complete.html'), name='password_reset_complete'),

]

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)