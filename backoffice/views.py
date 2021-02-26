from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic.base import TemplateView, View
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView

from backoffice.models import Buying, BuyingEntry, Portion, Product, Room, Price
from backoffice.forms import (
    BuyingEntryModelForm,
    BuyingModelForm,
    DishModelForm, ProductModelForm, RoomModelForm, UserCreationForm)


User = get_user_model()


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
        price_fields_names = filter(
            lambda val: 'price' in val, cleaned_data.keys())
        for price_field_name in price_fields_names:
            Price.objects.create(
                price=cleaned_data.get(price_field_name),
                room=get_object_or_404(
                    Room, pk=price_field_name.split('_')[2]),
                dish=dish_obj
            )
        return super().form_valid(form)


class BuyingCreateView(LoginRequiredMixin, CreateView):
    template_name = 'backoffice/buying_form.html'
    form_class = BuyingModelForm

    def get_success_url(self) -> str:
        return reverse(
            'backoffice:buying-product-add',
            kwargs={'buying_pk': self.buying_pk})

    def form_valid(self, form):
        obj = form.save()
        self.buying_pk = obj.pk
        return super().form_valid(form)


class BuyingEntryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'backoffice/buying-entry_form.html'
    form_class = BuyingEntryModelForm
    success_message = 'Produit ajouté'

    def get_success_url(self) -> str:
        return reverse(
            'backoffice:buying-product-add',
            kwargs={'buying_pk': self.kwargs.get('buying_pk')})

    def get_buying_object(self):
        return get_object_or_404(
            Buying,
            pk=self.kwargs.get('buying_pk'))

    def form_valid(self, form):
        buying = self.get_buying_object()
        obj = form.save(commit=False)
        obj.buying = buying
        obj.save()

        if obj.product.is_portionable:
            partition = obj.partition
            stock = partition.compute_stock_quantity(obj.quantity)
            Portion.objects.create(
                stock_store=stock,
                partition=partition)
        else:
            stock = obj.quantity
            Portion.objects.create(
                stock_store=stock)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buying'] = self.get_buying_object()
        return context


class UserCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'backoffice/user_form.html'
    form_class = UserCreationForm
    success_message = 'Caissier crée avec succès'
    success_url = reverse_lazy('backoffice:user-list')


class UserListView(LoginRequiredMixin, ListView):
    template_name = 'backoffice/user_list.html'
    context_object_name = 'users'
    model = User

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_superuser=False).order_by('-date_joined')


class UserActivateDeactivateView(LoginRequiredMixin, View):

    def get_success_message(self, name, action):
        template = 'Le caissier {} a été {} avec succès'.format(name,
            "désactive" if action == 'deactivate' else 'activé')
        messages.info(self.request, template)

    def get(self, *args, **kwargs):
        username = self.request.GET.get('username')
        action = self.request.GET.get('action')
        user = get_object_or_404(User, username=username)
        user.is_active = False if action == 'deactivate' else True
        user.save()

        self.get_success_message(name=user, action=action)
        return redirect('backoffice:user-list')
