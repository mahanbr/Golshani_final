from django.contrib import admin
from .models import ContactUs, Faq, StaticData

# admin.site.register(StaticData)
admin.site.register(Faq)
admin.site.register(ContactUs)
admin.site.register(StaticData)


