from django.urls import path
from .views import search_anime
from django.views.generic import TemplateView

urlpatterns = [
    path('search/<str:q>/',search_anime),
    path('',TemplateView.as_view(template_name='home.html')),
]