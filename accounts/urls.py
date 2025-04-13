from django.urls import path 
from .views import *

urlpatterns = [
    path('signin/', SigninView.as_view(), name='signin'),
    path('signup/', signup, name='signup'),
    path('signup_verify/', signup_verify, name='signup_verify'),
    path('reset-password/', reset_password, name='reset_password'),
	path('change-password/', change_password, name='change_password'),
    path('signout/', SignoutView.as_view(), name='signout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('document/', UploadDocView.as_view(), name='upload_doc'),
    path('pay-review/', PayReviewView.as_view(), name='pay_review'),
    path('pay-fee/', PayFeeView.as_view(), name='pay_fee'),
    path('verify/', verify , name='verify'),
	path('city-list/', city_list, name='city_list'), 
]
