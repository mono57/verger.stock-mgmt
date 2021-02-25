from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView

from backoffice.models import Product, Room, Price
from backoffice.forms import DishModelForm, ProductModelForm, RoomModelForm


class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


class ProductCreateView(
        LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'backoffice/product_form.html'
    success_url = reverse_lazy('backoffice:product-add')
    form_class = ProductModelForm
    success_message = 'Votre produit a été ajouté'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context

class ProductListView(LoginRequiredMixin, ListView):
    template_name = 'backoffice/product_list.html'
    model = Product
    context_object_name = 'products'
class RoomCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'backoffice/room_form.html'
    form_class = RoomModelForm
    success_url = reverse_lazy('backoffice:room-add')
    success_message = 'La salle a été ajouté avec succès'


class RoomListView(LoginRequiredMixin, ListView):
    template_name = 'backoffice/room_list.html'
    model = Room
    context_object_name = 'rooms'


class RoomUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'backoffice/room_form.html'
    form_class = RoomModelForm
    model = Room
    success_message = 'Modification effectuée'

    def get_success_url(self) -> str:
        return reverse('backoffice:room_update', kwargs={'pk': self.get_object().pk})


class DishCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'backoffice/dish_form.html'
    form_class = DishModelForm
    success_url = reverse_lazy('backoffice:dish-add')
    success_message = 'Nouveau plat defini avec succès'

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        dish_obj = form.save()
        price_fields_names = filter(lambda val: 'price' in val, cleaned_data.keys())
        for price_field_name in price_fields_names:
            Price.objects.create(
                price=cleaned_data.get(price_field_name),
                room=get_object_or_404(Room, pk=price_field_name.split('_')[2]),
                dish=dish_obj
            )
        return super().form_valid(form)

        