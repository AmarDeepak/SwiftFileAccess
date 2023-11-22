from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render
from django.views.generic import TemplateView

"""TODO: move this to view.py file."""
def home(request):
    return (request, 'account/login.html')

"""TODO: Create a separate app for user and move this user and user dashboard functionality there"""
def user(request):
    return render(request, 'dashboard/dashboard.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('',TemplateView.as_view(template_name='account/login.html'), name='home'),
    path('dashboard/', user, name='dashboard'),
    path("file/", include(("file.urls", "file"), namespace="file"))
]
