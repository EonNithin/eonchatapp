from django.urls import path
from eonbot.views import home


urlpatterns = [
    path('', home, name='home'),

]