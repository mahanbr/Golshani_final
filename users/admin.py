from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# from accounts.models import UserDocument
# class UserDocumentInline(admin.TabularInline):
#     model = UserDocument
#     extra = 0


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ( 'first_name', 'last_name' ,'phone_number', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'password', 'first_name', 'last_name')}),
        ('زمان ها', {'fields': ('last_login', 'date_joined')}),
        ('مجوز ها', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )
    search_fields = ('phone_number', 'first_name', 'last_name',)
    ordering = ('phone_number',)

    # inlines = (UserDocumentInline,)

admin.site.register(CustomUser, CustomUserAdmin)