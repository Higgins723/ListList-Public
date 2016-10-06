from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic.base import TemplateView, TemplateResponseMixin, ContextMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, ModelFormMixin
from django.views.generic.list import ListView

from .forms import ContactForm
from .models import Contact

# Create your views here.
class ContactCreateView(SuccessMessageMixin, CreateView):
    template_name = "contact/contact.html"
    form_class = ContactForm
    success_message = "Thank you %(email)s, for reaching out we will be in touch soon."

    def form_valid(self, form):
        form_valid = super(ContactCreateView, self).form_valid(form)
        return form_valid

    def get_context_data(self, *args, **kwargs):
        context = super(ContactCreateView, self).get_context_data(*args, **kwargs)
        context["title"] = "Contact Us"
        return context

    def get_success_url(self):
        return reverse("contact")