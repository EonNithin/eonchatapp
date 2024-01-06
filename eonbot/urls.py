from django.urls import path
from eonbot import views
from eonbot.views import home
from eonbot.views import response_view

urlpatterns = [
    path('', home, name='home'),
    path('response/', views.response_view, name='response_view'),  # Add this line for the response view
]