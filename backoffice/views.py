from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView


from backoffice.forms import ProductModelForm

class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
class ProductCreateView(
    LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'backoffice/product_form.html'
    success_url = reverse_lazy('backoffice:product-add')
    form_class = ProductModelForm
    success_message = 'Votre produit a été ajouté'