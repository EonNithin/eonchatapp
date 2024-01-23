from django.urls import path
from eonbot import views
from eonbot.views import home
from eonbot.views import response_view

from django.urls import include, path, re_path
from django.views.static import serve
from eonchatapp import settings


urlpatterns = [
    path('', home, name='home'),
    path('response/', views.response_view, name='response_view'),  # Add this line for the response view
]
