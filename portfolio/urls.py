# portfolio/urls.py

from django.urls import path
from .views import portfolio_view
from .views import portfolio_view, track_click # Add track_click here

urlpatterns = [
    path('', portfolio_view, name='portfolio'),
    path('track_click/', track_click, name='track_click'),
]