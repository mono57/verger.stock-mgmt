from stockmgmt.mixins import AdminLoginRequiredMixin
from typing import Any, Dict
from django.db.models.query import QuerySet
from django.forms.forms import BaseForm
from django.forms.models import BaseModelForm
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls.conf import path
from django.views.generic.base import TemplateView, View
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, UpdateView

from backoffice.models import Buying, BuyingEntry, Drink, Invoice, InvoiceEntry, Portion, Product, Room, Price
from backoffice.forms import (
    BuyingEntryModelForm,
    BuyingModelForm,
    DishModelForm,
    DrinkModelForm, InvoiceEntryDishModelForm, InvoiceEntryDrinkModelForm,
    InvoiceModelForm,
    ProductModelForm,
    RoomModelForm,
    UserCreationForm)


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


class AbstractSellableCreateView(
        LoginRequiredMixin,
        SuccessMessageMixin,
        CreateView):
    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        obj = form.save()
        price_fields_names = filter(
            lambda val: 'price' in val, cleaned_data.keys())
        for price_field_name in price_fields_names:
            Price.objects.create(
                price=cleaned_data.get(price_field_name),
                room=get_object_or_404(
                    Room, pk=price_field_name.split('_')[2]),
                content_object=obj
            )
        return super().form_valid(form)


class DishCreateView(AbstractSellableCreateView):
    template_name = 'backoffice/dish_form.html'
    form_class = DishModelForm
    success_url = reverse_lazy('backoffice:dish-add')
    success_message = 'Nouveau plat defini avec succès'


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
        return super().get_queryset().filter(
            is_superuser=False
        ).order_by('-date_joined')


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


class DrinkCreateView(AbstractSellableCreateView):
    template_name = 'backoffice/drink_form.html'
    form_class = DrinkModelForm
    success_message = 'Boisson ajoutée avec succès'
    success_url = reverse_lazy('backoffice:drink-add')


class InvoiceCreateView(
        LoginRequiredMixin,
        CreateView):
    template_name = 'backoffice/invoice_form.html'
    form_class = InvoiceModelForm

    def get_success_url(self) -> str:
        return reverse(
            self.success_url,
            kwargs={'invoice_pk': self.invoice_pk})

    def post(self, request, *args, **kwargs):
        self.success_url = 'backoffice:invoice_entry_dish-add'\
            if request.POST.get('_add_dish') is not None \
            else 'backoffice:invoice_entry_drink-add'

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.paymaster = self.request.user
        obj.save()
        self.invoice_pk = obj.pk
        return super().form_valid(form)


class AbstractInvoiceEntryCreateView(
        LoginRequiredMixin,
        SuccessMessageMixin,
        FormView):
    template_name = 'backoffice/invoice-entry_form.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {'invoice': self.get_invoice_object()})
        return context

    def get_invoice_object(self):
        return get_object_or_404(
            Invoice,
            pk=self.kwargs.get('invoice_pk'))


class InvoiceEntryDrinkCreateView(AbstractInvoiceEntryCreateView):
    success_message = 'Boisson ajoutée'
    form_class = InvoiceEntryDrinkModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'btn_text': 'Ajouter la boisson'})
        return context

    def form_valid(self, form: BaseForm) -> HttpResponse:
        cleaned_data = form.cleaned_data

        invoice_obj = self.get_invoice_object()
        drink_obj = cleaned_data.get('choices')

        invoice_entry_price = drink_obj.prices.get_price_by_room(
            room=invoice_obj.room)

        InvoiceEntry.objects.create(
            invoice=invoice_obj,
            content_object=drink_obj,
            quantity=cleaned_data.get('quantity'),
            price=invoice_entry_price
        )

        return self.get_success_url()

    def get_success_url(self) -> str:
        return redirect(reverse(
            'backoffice:invoice_entry_drink-add',
            kwargs={'invoice_pk': self.get_invoice_object().pk}))


class InvoiceEntryDishCreateView(AbstractInvoiceEntryCreateView):
    success_message = 'Plat ajouté'
    form_class = InvoiceEntryDishModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'btn_text': 'Ajouter le plat'})
        return context

    def form_valid(self, form: BaseForm) -> HttpResponse:
        cleaned_data = form.cleaned_data

        invoice_obj = self.get_invoice_object()
        dish_obj = cleaned_data.get('choices')

        invoice_entry_price = dish_obj.prices.get_price_by_room(
            room=invoice_obj.room)

        InvoiceEntry.objects.create(
            invoice=invoice_obj,
            content_object=dish_obj,
            quantity=cleaned_data.get('quantity'),
            price=invoice_entry_price.price
        )

        return self.get_success_url()

    def get_success_url(self) -> str:

        return redirect(reverse(
            'backoffice:invoice_entry_dish-add',
            kwargs={'invoice_pk': self.get_invoice_object().pk}))


def state_sale(request):

    return render(request, 'backoffice/state_sale.html')
