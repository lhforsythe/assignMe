"""
URL configuration for assignMe project.

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
from django.urls import path, include
from index.views import view
from main.views import landing
from main.views import main
from main.views import refresh
from main.views import filter
from main.views import completed
from main.views import toggleView
from main.views import addAssignment
urlpatterns = [
    path("", view, name="index_view"),  # index
    path("accounts/", include("allauth.urls")),
    path("accounts/setup/", landing, name="landing_view"),
    path("accounts/dashboard/", main, name="main_view"),
    path("accounts/refresh/", refresh, name="refresh_view"),
    path("accounts/dashboard/filter", filter, name="filter_view"),
    path("accounts/dashboard/completed/", completed, name="completed_view"),
    path("accounts/dashboard/toggleView", toggleView, name="toggle_view"),
    path("accounts/dashboard/addAssignment", addAssignment, name="add_assignment"),
]

