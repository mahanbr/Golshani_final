from django.contrib import admin
from accounts.models import Account, Payment, UserDocument



admin.site.register(Account)
admin.site.register(UserDocument)
admin.site.register(Payment)

