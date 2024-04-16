from django.urls import path
from . import views

urlpatterns = [
    path("",views.fetch_past_data,name='root'),
]
