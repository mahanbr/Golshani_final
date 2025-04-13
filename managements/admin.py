from django.contrib import admin
from .models import ContactUs, LoanType, Faq, ReturnPeriod

# admin.site.register(StaticData)
admin.site.register(Faq)
admin.site.register(ContactUs)


class ReturnPeriodInline(admin.StackedInline):
    model = ReturnPeriod
    extra = 0


@admin.register(LoanType)
class LoanTypeAdmin(admin.ModelAdmin):
    inlines = [ReturnPeriodInline,]