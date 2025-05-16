from django.db import models
    
class Faq(models.Model):
    question = models.TextField('سوال')
    answer = models.TextField('پاسخ')
    class Meta:
        verbose_name = "پرسش و پاسخ"
        verbose_name_plural = "پرسش و پاسخ"
        
    def __str__(self):
        return f'{self.question}'

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
    



class StaticData(models.Model):
    phone = models.CharField('تلفن ثابت', max_length=20, blank=True, null=True)
    mobile = models.CharField('همراه', max_length=20, blank=True, null=True)
    whatsapp = models.PositiveIntegerField('واتساپ', blank=True, null=True)
    instagram = models.CharField('اینستاگرام', max_length=30, blank=True, null=True)
    telegram = models.CharField('ایدی_تلگرام', max_length=30, blank=True, null=True)
    email = models.CharField('ایمیل', max_length=30, blank=True, null=True)
    twitter = models.CharField('توییتر', max_length=30, blank=True, null=True)
    address = models.TextField('ادرس', blank=True, null=True)

    
    class Meta:
        verbose_name = "مشخصات سایت"
        verbose_name_plural = "مشخصات سایت"
        

    

    
    
