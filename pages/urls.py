from django.urls import path, re_path 
from .views import *

urlpatterns = [
    path('', IndexPage.as_view(), name='index'), 
    path('contact-us/', ContactView.as_view(), name='contact'),
    
]
