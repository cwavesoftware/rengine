from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('',
        RedirectView.as_view(url='/target/list/target', permanent=False),
    ),
    path(
        'dashboard/',
        views.index,
        name='dashboardIndex'),
    path(
        'profile/',
        views.profile,
        name='profile'),
]
