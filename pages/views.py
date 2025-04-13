from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView, FormView

from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages

from golshani.extra_func import google_recaptcha
from managements.models import Faq
from pages.forms import ContactUsForm




class IndexPage(View):
    template_name = 'pages/index_new.html'
    def get(self, request, *args, **kwargs):
        # home_data = HomeData.objects.first()
        faq_query = Faq.objects.all()

        context = {
            'faq' : faq_query,
            'form': ContactUsForm
            # 'home_data': home_data,
        }
        return render(request, self.template_name, context=context)
    
    

class ContactView(FormView):
    form_class = ContactUsForm
    success_url = reverse_lazy('index')
    template_name = 'pages/index_new.html'
    def get_success_url(self):
        return super().get_success_url() + '#contact'
    
    def form_valid(self, form):
        if form.cleaned_data['phone_number'][:2] != '09':
            messages.error(self.request, 'فرمت شماره غلط می باشد')     
            return self.form_invalid(form)
        if  'script' in form.cleaned_data['user_message']:
            messages.error(self.request, 'ای پی شما ثبت شد و در صورت تکرار برخورد قانونی صورت خواهد گرفت.')     
            return self.form_invalid(form)
        recaptcha_response = self.request.POST.get("g-recaptcha-response")
        if google_recaptcha(recaptcha_response):
            form.save()
            messages.success(self.request, "با موفقیت ثبت شد.")
            return super().form_valid(form)
        else:
            messages.error(self.request, 'لطفا مجدد تلاش نمایید.')
            return self.form_invalid(form)
    def form_invalid(self, form):
        messages.error(self.request, form.errors.as_text())     
        return redirect(self.success_url + '#contact')


def error_404_view(request, exception):
    return render(request, 'blogs/404.html')