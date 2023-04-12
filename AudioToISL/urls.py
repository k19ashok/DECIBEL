from django.urls import path
from AudioToISL.views import home, getSigns
urlpatterns = [
    path('', home, name="home"),
    path('getSigns',getSigns, name="getSigns")
]