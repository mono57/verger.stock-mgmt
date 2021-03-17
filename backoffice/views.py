from stockmgmt.mixins import AdminLoginRequiredMixin
from typing import Any, Dict
from django.db.models.query import QuerySet
from django.forms.forms import BaseForm
from django.forms.models import BaseModelForm
from django.http.response import HttpResponse
from django.utils import timezone
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

from backoffice.models import Buying, BuyingEntry, Dish, Drink, Invoice, InvoiceEntry, Portion, Product, Room, Price
from django.views.generic.edit import UpdateView
from django.http import JsonResponse
from django.contrib import messages

from backoffice.models import PartitionFormulla, Buying, BuyingEntry, PartitionFormulla, Portion, Product, Room, Price, Transfert, Dish, Drink
from backoffice.forms import (
    BuyingEntryModelForm,
    BuyingModelForm,
    DishModelForm,
    DrinkModelForm, InvoiceEntryDishModelForm, InvoiceEntryDrinkModelForm,
    InvoiceModelForm,
    ProductModelForm,
    RoomModelForm,
    UserCreationForm,
    FormulaModelForm)


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


class FormulaCreateView(
        LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'backoffice/formula_form.html'
    success_url = reverse_lazy('backoffice:formula-add')
    form_class = FormulaModelForm
    success_message = 'Votre formule a été ajouté'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formulas'] = PartitionFormulla.objects.all()
        return context


class FormulaListView(LoginRequiredMixin, ListView):
    template_name = 'backoffice/formula_list.html'
    model = PartitionFormulla
    context_object_name = 'formulas'


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


class BuyingCreateView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        buying = Buying.objects.create()
        return redirect(reverse(
            'backoffice:buying-product-add',
            kwargs={'buying_pk': buying.pk}))

    # def form_valid(self, form):
    #     obj = form.save()
    #     self.buying_pk = obj.pk
    #     return super().form_valid(form)


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
        portions = form.cleaned_data.get('portions')
        obj = form.save(commit=False)
        obj.buying = buying
        obj.save()

        product = obj.product

        if product.is_portionable:
            p, created = Portion.objects.get_or_create(product=product)

            if created:
                p.stock_store = portions
                p.product = product
            else:
                p.stock_store += portions
            p.save()

        else:
            p, created = Portion.objects.get_or_create(product=product)

            if created:
                p.stock_store = portions
                p.product = product
            else:
                p.stock_store += portions
            p.save()

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

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['room'] = self.get_invoice_object().room
        return initial

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
        context.update(
            {'add_url': reverse(
                'backoffice:invoice_entry_dish-add',
                kwargs={'invoice_pk': self.get_invoice_object().pk})})
        context.update({'add_url_text': 'Ajouter un plat à la facture'})
        return context

    def form_valid(self, form: BaseForm) -> HttpResponse:
        cleaned_data = form.cleaned_data

        invoice_obj = self.get_invoice_object()
        drink_obj = cleaned_data.get('drinks')
        quantity = cleaned_data.get('quantity')
        price = cleaned_data.get('price')

        entry = InvoiceEntry.objects.create(
            invoice=invoice_obj,
            content_object=drink_obj,
            quantity=quantity,
            price=price,
            total_price=price*quantity
        )

        invoice_obj.total_price += entry.total_price
        invoice_obj.save()

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
        context.update(
            {'add_url': reverse(
                'backoffice:invoice_entry_drink-add',
                kwargs={'invoice_pk': self.get_invoice_object().pk})})
        context.update({'add_url_text': 'Ajouter une boisson à la facture'})
        return context

    def form_valid(self, form: BaseForm) -> HttpResponse:
        cleaned_data = form.cleaned_data

        invoice_obj = self.get_invoice_object()
        dish_obj = cleaned_data.get('dishs')
        quantity = cleaned_data.get('quantity')
        price = cleaned_data.get('price')

        # invoice_entry_price = dish_obj.prices.get_price_by_room(
        #     room=invoice_obj.room)
        entry = InvoiceEntry.objects.create(
            invoice=invoice_obj,
            content_object=dish_obj,
            quantity=cleaned_data.get('quantity'),
            price=price,
            total_price=quantity*price
        )
        invoice_obj.total_price += entry.total_price
        invoice_obj.save()

        return self.get_success_url()

    def get_success_url(self) -> str:

        return redirect(reverse(
            'backoffice:invoice_entry_dish-add',
            kwargs={'invoice_pk': self.get_invoice_object().pk}))


def state_sale(request):
    return render(request,'backoffice/state_sale.html')


def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request,'backoffice/invoice_list.html', locals())

def menu_restaurant(request):
    dishs = Dish.objects.all()
    drinks = Drink.objects.all()
    return render(request,'backoffice/menu_restaurant.html', locals())


def transfert_portion(request):
    if request.method == 'POST':

        portion_id = request.POST['portion']
        quantity = request.POST['quantity']
        if int(portion_id) > 0:
            portion = Portion.objects.get(id=int(portion_id))
            if portion.stock_store >= int(quantity):
                portion.stock_store -= int(quantity)
                portion.store += int(quantity)
                portion.save()
                Transfert(portion=portion, quantity=int(quantity)).save()
            else:
                messages.error(
                    request, f"Erreur: la quantité à transférer est supérieure à ce qui est en stock!")
            messages.success(request, f"Transfert réussi!")
        else:
            messages.error(
                request, f"Erreur: Veuillez choisir une bonne formule")

    products = Product.objects.all()
    portions = Portion.objects.all()

    return render(request, 'backoffice/transfert_portion.html', {
        "portions": portions,
    })


class AjaxProductGetPartitionFormula(View):
    def get(self, request, *args, **kwargs):

        product_pk = int(request.GET.get('product_pk'))
        qs = Product.objects.filter(pk=product_pk)

        if not qs.exists():
            return JsonResponse({'ok': False})

        formula = qs.first().partition

        if not formula:
            return self.response('Le produit n\'a pas de formule de partition')

        return self.response('{} quantité donne {} portions'.format(formula.input, formula.output))

    def response(self, message):
        return JsonResponse({'message': message})


class AjaxRoomDishPrice(View):
    def get(self, request, *args, **kwargs):
        dish_pk = int(request.GET.get('dish_pk'))
        room_name = request.GET.get('room')

        dish_qs = Dish.objects.filter(pk=dish_pk)
        room_qs = Room.objects.filter(name=room_name)
        if dish_qs.exists() and room_qs.exists():
            dish_obj, room_obj = dish_qs.first(), room_qs.first()

            price_obj = dish_obj.prices.get_price_by_room(room=room_obj)

            return JsonResponse({'price': price_obj.price}) if price_obj is not None else JsonResponse({'price': 0})

        return JsonResponse({})

class AjaxRoomDrinkPrice(View):
    def get(self, request, *args, **kwargs):
        drink_pk = int(request.GET.get('drink_pk'))
        room_name = request.GET.get('room')

        drink_qs = Drink.objects.filter(pk=drink_pk)
        room_qs = Room.objects.filter(name=room_name)
        if drink_qs.exists() and room_qs.exists():
            drink_obj, room_obj = drink_qs.first(), room_qs.first()

            price_obj = drink_obj.prices.get_price_by_room(room=room_obj)

            return JsonResponse({'price': price_obj.price}) if price_obj is not None else JsonResponse({'price': 0})

        return JsonResponse({})


def ajax_get_max_portion_number(request):
    portion_id = request.GET.get('portion_id', 'None')
    # print("Partition id:", portion_id)
    data = {}
    if portion_id.isdigit():
        try:
            portion = Portion.objects.get(id=int(portion_id))
            stock_store = portion.stock_store
            data = {
                'finded': True,
                'stock_store': stock_store
            }
        except Exception:
            data = {
                'finded': False,
            }
    else:
        data = {
            'finded': False
        }
    return JsonResponse(data)
