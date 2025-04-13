from django.utils.timezone import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, ListView, View
from django.contrib import messages
from accounts.models import Account, Payment
from accounts.permissions import SuperUserRequiredMixin
from golshani.otp_generator import two_tokens
from .models import ContactUs
from django.db.models import Sum
from django.db.models import Q
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from golshani.extra_func import format_date


class ManagerIndex(SuperUserRequiredMixin, TemplateView):
    template_name = 'managements/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["unapproved_users"] = Account.objects.filter(status='under_review').count()
        context["total_users"] = Account.objects.all().count()
        context["payments"] = Payment.objects.all().count()
        context["unreads"] = ContactUs.objects.filter(seen=False).count()
        return context
 
 

class ReviewMessages(SuperUserRequiredMixin, View):
    template_name= 'managements/messages.html'
    def get(self, request, *args, **kwargs):
        messages_query = ContactUs.objects.all().order_by('-send_date')
        context = {
            'messages' : messages_query 
            }
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        messages_query = ContactUs.objects.all().order_by('-send_date')
        msg_id = request.POST.get('msg_id', None)
        if msg_id != None:
            msg = messages_query.get(id=msg_id)
            msg.seen = True
            msg.save(update_fields=['seen'])   
            messages.success(request, "با موفقیت ثبت شد.")     
        return redirect('review_messages')
    
    
    
class UnapprovedUsersView(SuperUserRequiredMixin, ListView):
    model = Account
    template_name = "managements/unapproved_users.html"
    context_object_name = 'accounts'
    def get_queryset(self):
        return Account.objects.filter(status='under_review')
    
    
class UserUpdateView(SuperUserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id', None)
        if user_id != None:
            user_id = user_id.split('-') 
            selected_account = Account.objects.get(id=user_id[1])
            if user_id[0] == 'accept':
                selected_account.status = 'approved'
                # two_tokens(selected_account.user.first_name , f'SG-{selected_account.fake_id}', selected_account.user.phone_number, 'SharanOrderConfirm')  #! THIS HAS TO BE CHANGED              
            elif user_id[0] == 'deny':
                # two_tokens(selected_account.user.first_name , f'SG-{selected_account.fake_id}', selected_account.user.phone_number, 'SharanOrderConfirm')                #! THIS HAS TO BE CHANGED
                selected_account.status = 'rejected'
            selected_account.save(update_fields=['status'])   
            messages.success(request, "با موفقیت ثبت شد.")
        return redirect(self.request.META.get('HTTP_REFERER', '/'))
          
                
    



     
                
class ReviewPaymentsView(SuperUserRequiredMixin, View):
    template_name= 'managements/payments_review.html'
    def get(self, request, *args, **kwargs):

    
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)
        query = self.request.GET.get('query', None)
        amount = self.request.GET.get('amount', None)
        success = self.request.GET.get('success', None)
 
        payments_query = Payment.objects.select_related('user__user',).order_by('-date')
        if start_date and end_date:
            end_date = str(format_date(end_date))
            start_date = str(format_date(start_date))
            end_date = make_aware(datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1))
            payments_query = payments_query.filter(date__range=[start_date, end_date])
        elif start_date:
            start_date = str(format_date(start_date))
            payments_query = payments_query.filter(date__gte=start_date)
        elif end_date:
            end_date = str(format_date(end_date))
            end_date = make_aware(datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1))
            payments_query = payments_query.filter(date__lte=end_date)
        if query:
            payments_query = payments_query.filter(Q(user__user__first_name__icontains=query) | Q(user__user__last_name__icontains=query))

        # Filter by amount if provided
        if amount:
            payments_query = payments_query.filter(amount=amount)
        
        if success:
            payments_query = payments_query.filter(paid=True)
        
        
        total_amount = payments_query.filter(paid=True).aggregate(Sum('amount'))['amount__sum']

        context = {
            'payments' : payments_query,
            'total_amount' : total_amount
        }
        return render(request, self.template_name, context)

    
    
    
    
class UserInfoView(SuperUserRequiredMixin, View):
    template_name= 'managements/user_info.html'
    
    def get(self, request, *args, **kwargs):
 

        account = get_object_or_404(Account, pk=self.kwargs['pk'])
        
        context = {
            'user': account
        }
        return render(request, self.template_name, context)
    
    
    
class PaymentCheckView(SuperUserRequiredMixin, View):
    template_name= 'managements/single_payment.html'
    
    def get(self, request, *args, **kwargs):
        payment = Payment.objects.filter(pk=self.kwargs['pk'])
        context = {
            'payments': payment
        }
        return render(request, self.template_name, context)
    
class UserPaymentCheckView(SuperUserRequiredMixin, View):
    template_name= 'managements/single_payment.html'
    
    def get(self, request, *args, **kwargs):
        payment = Account.objects.get(pk=self.kwargs['pk']).payments.order_by('-paid')
        context = {
            'payments': payment
        }
        return render(request, self.template_name, context)

    
    

class ReviewUsers(SuperUserRequiredMixin, ListView):
    model = Account
    template_name = 'managements/review_users.html'
    context_object_name = 'accounts'
    def get_queryset(self):
        return Account.objects.select_related('user',)






class ReviewUsers(SuperUserRequiredMixin, View):
    template_name = 'managements/review_users.html'
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query', None)
        phone = self.request.GET.get('amount', None)
        account_query = Account.objects.select_related('user')
 

        if query:
            account_query = account_query.filter(Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query))

        # Filter by amount if provided
        if phone:
            account_query = account_query.filter(user__first_name__icontains=phone)
        
        for account in account_query:
            account.successful_payments = account.payments.filter(paid=True).exists()

        context = {
            'accounts' : account_query,
        }
        return render(request, self.template_name, context)

   