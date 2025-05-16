from django.urls import path 
from .views import *

urlpatterns = [
    path('', ManagerIndex.as_view(), name='manager_index'), 
	path('review-messages',  ReviewMessages.as_view(), name='review_messages'),
	path('review-users', ReviewUsers.as_view(), name='review_users'),
	path('review-payments', ReviewPaymentsView.as_view(), name='review_payments'),
	path('payment/check/<int:pk>', PaymentCheckView.as_view(), name='payment_check'),
	path('user-payment/check/<int:pk>', UserPaymentCheckView.as_view(), name='user_payment_check'),
	path('user-info/check/<int:pk>', UserInfoView.as_view(), name='user_info'),
	path('unapproved-users',  UnapprovedUsersView.as_view(), name='unapproved_users'),
	path('filled-users',  FilledUsersView.as_view(), name='filled_users'),
	path('user-update',  UserUpdateView.as_view(), name='user_update'),
]
