from django.db import models

# from django_resized import ResizedImageField
# from pages.models import Category


# class StaticData(models.Model):
#     phone = models.CharField('تلفن ثابت', max_length=20, blank=True, null=True)
#     mobile = models.CharField('همراه', max_length=20, blank=True, null=True)
#     whatsapp = models.PositiveIntegerField('واتساپ', blank=True, null=True)
#     instagram = models.CharField('اینستاگرام', max_length=30, blank=True, null=True)
#     instagram2 = models.CharField('2 اینستاگرام', max_length=30, blank=True, null=True)
#     telegram = models.CharField('ایدی_تلگرام', max_length=30, blank=True, null=True)
#     twitter = models.CharField('توییتر', max_length=30, blank=True, null=True)
#     address = models.TextField('ادرس', blank=True, null=True)

#     alert_mobile = models.CharField('تلفن هشدار سفارش', max_length=20, blank=True, null=True)
#     alert_mobile2 = models.CharField('تلفن هشدار 2', max_length=20, blank=True, null=True)

    
#     class Meta:
#         verbose_name = "مشخصات سایت"
#         verbose_name_plural = "مشخصات سایت"
        
#     def __str__(self):
#         return f'{self.slogan_percent}% تخفیف'
    

    
    
    
class Faq(models.Model):
    question = models.TextField('سوال')
    answer = models.TextField('پاسخ')
    class Meta:
        verbose_name = "پرسش و پاسخ"
        verbose_name_plural = "پرسش و پاسخ"
        
    def __str__(self):
        return f'{self.question}'
    
    

class LoanType(models.Model):
    title = models.IntegerField('مقدار وام به تومان')
    is_active = models.BooleanField('فعال', default=False)    
    class Meta:
        verbose_name = "ایجاد وام جدید"
        verbose_name_plural = "ایجاد وام جدید"
        
    def __str__(self):
        return str(self.title)
    
    
class ReturnPeriod(models.Model):
    loan_type = models.ForeignKey(LoanType, on_delete=models.CASCADE, related_name='loan_months')
    months = models.IntegerField('ماه')
    def __str__(self):
        return str(self.months)
    
    class Meta:
        verbose_name = "دوره بازپرداخت"
        verbose_name_plural = "دوره بازپرداخت"



class ContactUs(models.Model):
    full_name = models.CharField('نام کامل', max_length=30)
    phone_number = models.CharField('شماره تماس', max_length=11)
    subject = models.CharField('موضوع', max_length=100)
    user_message = models.TextField('پیام')
    send_date =  models.DateTimeField('زمان ارسال', auto_now_add=True, blank=True, null=True)
    seen = models.BooleanField('مشاهده شد؟', default=False)
    
    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام ها"
    
    def __str__(self):
        return self.full_name
    
    
