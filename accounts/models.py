from django.db import models
from users.models import CustomUser
from django.core.validators import validate_image_file_extension
from django.utils.timezone import datetime, now
from golshani.extra_func import format_date, validate_image_file, user_directory_path

    

class Account(models.Model):
    GENDER_CHOICES = (
        ("MAN", "آقا"),
        ("WOMAN", "خانوم"),
    )
    CHTYPE_CHOICES = (
        ("PERSONAL", "حقیقی"),
        ("CORPRATE", "حقوقی"),
    )
    STATUS_CHOICES = (
        ('pending_user', 'تکمیل اطلاعات'),
        ('upload_documents', 'بارگذاری مدارک'),
        ('pay_fee', 'پرداخت فیش'),
        ('under_review', 'بررسی مدارک'),
        ('rejected', 'رد شده'),
        ('complete_payment', 'تکمیل وجه'),
        ('approved', 'تایید شده'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField('تلفن ثابت', max_length=15, null=True)
    gender = models.CharField('جنسیت', max_length=6, choices=GENDER_CHOICES, blank=True)
    chtype = models.CharField('شخصیت', max_length=10, choices=CHTYPE_CHOICES, blank=True)
    email = models.EmailField('ایمیل', blank=True)
    province = models.CharField('استان', max_length=30)
    city = models.CharField('شهر', max_length=30)
    postal_code = models.PositiveBigIntegerField('کد پستی', null=True)
    address = models.TextField('آدرس')    
    code_meli = models.CharField(max_length=20, blank=True, null=True)
    father_name = models.CharField(max_length=20, blank=True, null=True)
    jalali_birth = models.CharField(max_length=30)
    birthday = models.DateField(blank=True, null=True)    

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_user')

    @property
    def amount(self):
        if self.status == 'pay_fee':
            x = 10000000
        elif self.status == 'complete_payment':
            x = 500000000
        return x     
    
    class Meta:
        verbose_name = "درخواست وام"
        verbose_name_plural = "درخواست‌های وام"

    def __str__(self):
        return f"{self.user.username} - {self.loan_type.title} ({self.return_period.months} ماه)"

    

    
    def save(self, *args, **kwargs):
        self.birthday = format_date(self.jalali_birth)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "حساب مشتریان"

    def __str__(self):
        return self.user.get_full_name()
    
    






class UserDocument(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_doc')
    cart_meli = models.ImageField(
        upload_to=user_directory_path,
        validators=[validate_image_file_extension, validate_image_file]
    )
    shenas_name = models.ImageField(
        upload_to=user_directory_path,
        validators=[validate_image_file_extension, validate_image_file]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.user.get_full_name()
    
    class Meta:
        verbose_name = "مدرک"
        verbose_name_plural = "مدارک مشتریان"




class Payment(models.Model):
    PAYMENT_CHOICES = (
        ("FEE", "فیش"),
        ("COMPLETE", "تکمیل وجه"),
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="payments")
    amount = models.PositiveBigIntegerField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    ref_id = models.CharField(max_length=255, null=True, blank=True)
    card_hash = models.CharField(max_length=255, null=True, blank=True)
    card_number = models.CharField(max_length= 32,default="****")
    status = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)
    
    payment_type = models.CharField('علت پرداخت', max_length=10, choices=PAYMENT_CHOICES, blank=True, default='FEE')
    
    def save(self, *args, **kwargs):
        if self.amount != 10000000:
            self.payment_type = 'COMPLETE'
        super().save(*args, **kwargs)
        
        
    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = 'پرداخت ها'
        
    @property
    def humanize_time(self):
        return datetime.fromtimestamp(float(self.date))     
     


    def __str__(self):
        status = "موفق" if self.paid else "ناموفق"
        return f"پرداخت ({status}) - مبلغ: {self.amount}"

