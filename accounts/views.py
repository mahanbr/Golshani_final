from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
import requests
from .models import Account, UserDocument, Payment
from managements.models import LoanType, ReturnPeriod
from users.forms import CustomUserCreationForm
from users.models import CustomUser
from .forms import ProfileForm, ImageUploadForm
from .provinces import province_choices
from .cities import cities_choices
import json
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.core.cache import cache
from golshani.otp_generator import create_otp
from django.contrib import messages, auth
from django.contrib.auth.views import LogoutView
from golshani.extra_func import google_recaptcha

from django.views.generic.edit import FormView
from django.conf import settings


class SigninView(LoginView):
    template_name = 'accounts/signin.html'
    redirect_authenticated_user = 'index'
    success_url = 'dashboard'

    def form_valid(self, form):
        recaptcha_response = self.request.POST.get("g-recaptcha-response")
        if google_recaptcha(recaptcha_response):
            auth.login(self.request, form.get_user())
            return redirect("profile")

        # return HttpResponseRedirect(self.get_success_url())
    def form_invalid(self, form):
        print(form)
        print(form.errors)
        messages.error(self.request, 'نام کاربری یا رمزعبور غلط می باشد.')
        return super().form_invalid(form)


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            recaptcha_response = request.POST.get("recaptcha")
            if google_recaptcha(recaptcha_response):
                send_code = create_otp(form.cleaned_data["phone_number"], 'Sharansignup') #! THIS HAS TO BE CHANGED
                if send_code:
                    data_code = 200
                else:
                    data_code = 500
            else:
                data_code = 500
        else:
            data_code = 409
        return HttpResponse(json.dumps({"status": data_code}), content_type="application/json")
    return render(request, 'accounts/signup.html', {"form": CustomUserCreationForm()})


def signup_verify(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            user_code = request.POST.get('user_code')
            password = form.cleaned_data['password1']
            recaptcha_response = request.POST.get("g-recaptcha-response")
            if google_recaptcha(recaptcha_response):
                if cache.ttl(phone_number) > 0:
                    redis_code = int(cache.get(phone_number))
                    if redis_code == int(user_code):
                        cache.delete(phone_number)
                        user = CustomUser.objects.create_user(phone_number=phone_number,
                                                              password=password,
                                                              first_name=request.POST.get(
                                                                  'fname'),
                                                              last_name=request.POST.get('lname'))
                        auth.login(request, user)
                        return redirect("dashboard")
    return redirect("signup")


class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request, *args, **kwargs):
        if Account.objects.filter(user=request.user, application_date__isnull=False).exists():
            return redirect('dashboard')

        account = Account.objects.get(user=self.request.user)
        form = ProfileForm(instance=account)
        select_city = None
        if account.province:
            for key, value in province_choices.items():
                if account.province == value:
                    select_city = key
        if select_city != None:
            for city in cities_choices:
                if city['province_id'] == select_city:
                    select_city = city['cities']

        context = {
            'provinces': province_choices,
            'cities': select_city,
            'form': form,
            'loan_types': [{types.id: types.title} for types in LoanType.objects.filter(is_active=True)],
            'return_periods': [
                {'loan_type_id': period.loan_type.id,
                    'id': period.id, 'months': period.months}
                for period in ReturnPeriod.objects.all()]
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        account = Account.objects.get(user=self.request.user)
        form = ProfileForm(request.POST, instance=account)
        loan_type = request.POST.get('loan-type-select',)
        return_period = request.POST.get('return-period-select',)
        province_id = request.POST.get('id_province', 'TN')
        city_id = request.POST.get('id_city',)
        try:
            if city_id == None:
                raise ValueError
            for key, value in province_choices.items():
                if key == province_id:
                    province = value
            for city_choice in cities_choices:
                if city_choice['province_id'] == province_id:
                    for item in city_choice['cities']:
                        if item['id'] == int(city_id):
                            city = item['name']
            loan_type = get_object_or_404(
                LoanType, pk=int(loan_type), is_active=True)
            return_period = get_object_or_404(
                ReturnPeriod, pk=int(return_period), loan_type=loan_type)
        except Exception as e:
            print(e)
            messages.error(request, 'مقادیر وارد شده صحیح نمی باشند')
            return redirect('profile')

        if form.is_valid():

            new_form = form.save(commit=False)
            new_form.province = province
            new_form.city = city
            new_form.loan_type = loan_type
            new_form.return_period = return_period
            new_form.user = request.user
            new_form.status = 'upload_documents'
            new_form.save()
            messages.success(request, "با موفقیت ذخیره شد.")
        else:
            messages.error(request, form.errors.as_text())
        return redirect('profile')


class UploadDocView(FormView):
    # The template where the form is rendered
    template_name = 'accounts/upload_doc.html'
    form_class = ImageUploadForm
    success_url = reverse_lazy('pay_review')

    def dispatch(self, request, *args, **kwargs):
        account = Account.objects.get(user=self.request.user)
        if account.status != 'upload_documents':
            # messages.error(request, 'لطفا اول نسبت به تکمیل اطلاعات اقدام نمایید.')
            return redirect('dashboard')            
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
         
        cart_meli = form.cleaned_data.get('cart_meli')
        shenas_name = form.cleaned_data.get('shenas_name')
        
        if cart_meli and shenas_name:
            existing_document = UserDocument.objects.filter(user=self.request.user).first()
            
            if existing_document:
                existing_document.cart_meli = cart_meli
                existing_document.shenas_name = shenas_name
                existing_document.save()
            else:
                new_form = form.save(commit=False)
                new_form.user = self.request.user
                new_form.save()
        account = Account.objects.get(user=self.request.user)
        account.status = 'pay_fee'
        account.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form)
        # Provide additional logic for invalid forms (optional)
        return super().form_invalid(form)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'


class SignoutView(LoginRequiredMixin, LogoutView):
    next_page = 'index'  # Redirect to home page after logout


def reset_password(request):
    if request.method == "POST" and request.is_ajax():
        phone = request.POST.get('phone_number', None)
        recaptcha_response = request.POST.get("recaptcha")
        if google_recaptcha(recaptcha_response):
            if phone != None:
                acc = CustomUser.objects.filter(phone_number=phone)
                if acc.count() == 1:
                    send_code = create_otp(phone, 'Sharanreset') #! THIS HAS TO BE CHANGED
                    if send_code:
                        data_code = 200
                    else:
                        data_code = 500
                else:
                    data_code = 409
                return HttpResponse(json.dumps({"status": data_code}), content_type="application/json")
    return render(request, 'accounts/reset_password.html')


def change_password(request):
    if request.method == "POST":
        recaptcha_response = request.POST.get("g-recaptcha-response")
        if google_recaptcha(recaptcha_response):
            user_code = request.POST.get('user_code', None)
            phone = request.POST.get('phone_number', None)
            pass1 = request.POST.get('id_password1', None)
            pass2 = request.POST.get('id_password2', None)
            if pass1 != None:
                if pass1 == pass2:
                    if cache.ttl(phone) > 0:
                        redis_code = int(cache.get(phone))
                        if redis_code == int(user_code):
                            cache.delete(phone)
                            user = get_object_or_404(
                                CustomUser, phone_number=phone)
                            user.set_password(str(pass1))
                            user.save()
                            auth.login(request, user)
                            return redirect("profile")
    return redirect("reset_password")


@login_required
def city_list(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and 'province_num' in request.GET:
        province_id = request.GET.get('province_num', 'TN')
        for city in cities_choices:
            if city['province_id'] == province_id:
                return HttpResponse(
                    json.dumps({"status": 200, "city": city['cities']}), content_type="application/json"
                )
    raise Http404()


class PayReviewView(LoginRequiredMixin, View):
    template_name = 'accounts/pay_review.html'
    
    def dispatch(self, request, *args, **kwargs):
        if  UserDocument.objects.filter(user=request.user, cart_meli__isnull=True, shenas_name__isnull=True).exists():
            messages.error(request, 'لطفا اول نسبت به تکمیل اطلاعات اقدام نمایید.')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if Payment.objects.filter(user=user.account, paid=True).exists():
            messages.error(request, 'این تراکنش یکبار انجام شده است.')
            return redirect('dashboard')
        return render(request, self.template_name)


class PayFeeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        amount = user.account.fee_required()
        data = {
            "merchant_id": settings.MERCHANT,
            "amount": amount*10,
            "description": f'پرداخت مبلغ {amount} جهت بررسی درخواست وام',
            "metadata": {"mobile": self.request.user.phone_number},
            "callback_url": 'http://127.0.0.1:8080/account/verify/',
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json',
                   'content-length': str(len(data))}

        try:
            response = requests.post(
                settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10)
            if response.status_code == 200:
                response = response.json()
                if response['data']['code'] == 100:
                    base_url = settings.ZP_API_STARTPAY
                    params = str(response['data']['authority'])
                    return redirect(base_url + params)
                else:
                    messages.error(
                        request, 'خطایی رخ داد، لطفا مجدد تلاش فرمایید.')
                    return redirect('dashboard')
            return redirect('pay_review')
        except requests.exceptions.Timeout:
            messages.error(
                request, 'در برقراری اتصال با درگاه مشکلی پیش آمده،لطفا در صورت تکرار به پشتیبانی اطلاع دهید')
            return redirect('dashboard')
        except requests.exceptions.ConnectionError:
            messages.error(
                request, 'در برقراری اتصال با درگاه مشکلی پیش آمده،لطفا در صورت تکرار به پشتیبانی اطلاع دهید')
            return redirect('dashboard')


@login_required
def verify(request):
    if "Authority" and "Status" in request.GET:

        status = request.GET.get("Status")
        authority = request.GET.get("Authority")
        amount = request.user.account.fee_required()
        data = {
            "merchant_id": settings.MERCHANT,
            "amount": amount*10,
            "authority": authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json',
                   'content-length': str(len(data))}
        response = requests.post(
            settings.ZP_API_VERIFY, data=data, headers=headers).json()

        if status == 'OK':
            response = response['data']
            if response['code'] == 100:
                record = Payment.objects.create(
                    user=request.user.account,
                    amount=amount,
                    ref_id=response['ref_id'],
                    card_hash=response['card_hash'],
                    card_number=response['card_pan'],
                    status=response['code'],
                    paid=True
                )
                record.save()
                # two_tokens(selected_account.user.first_name , f'SG-{selected_account.fake_id}', selected_account.user.phone_number, 'SharanOrderConfirm')  #! THIS HAS TO BE CHANGED              
                

                account = Account.objects.get(user=request.user)
                account.status = 'under_review'
                account.save()
            messages.success(request, 'پرداخت با موقیت انجام شد')
            return redirect('dashboard')
        else:
            response = response['errors']
            record = Payment.objects.create(
                user=request.user.account,
                amount=amount,
                status=response['code'],
            )
            record.save()
            messages.error(request, 'پرداخت ناموفق لطفا مجدد تلاش کنید')
            return redirect('dashboard')
