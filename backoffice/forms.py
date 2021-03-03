from django.forms import widgets
from django.utils import timezone
from django import forms
from enum import Enum
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from backoffice.models import (
    Buying, BuyingEntry, Dish, Drink, Invoice, InvoiceEntry, PartitionFormulla, Product, Room)


User = get_user_model()


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'product_type', 'category', 'partition')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'product_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'partition': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = Product.objects.filter(name=name)
        if qs.exists():
            raise forms.ValidationError('Un produit de même existe déjà !')
        return name


class RoomModelForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = Room.objects.filter(name=name)
        if qs.exists():
            raise forms.ValidationError('Cette salle existe déjà')

        return name


class AbstractSellableModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rooms = Room.objects.all()
        for room in rooms:
            field_name = 'price_room_%s' % (room.pk, )
            self.fields[field_name] = forms.IntegerField(
                label="Prix du plat dans %s" % (room.name, ),
                help_text="Prix en F CFA",
                required=False,
                widget=forms.NumberInput(attrs={
                    'class': 'form-control'
                }))


class DishModelForm(AbstractSellableModelForm):
    class Meta:
        model = Dish
        fields = ('name', 'partition')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'partition': forms.Select(attrs={'class': 'form-select'}),
        }


class BuyingModelForm(forms.ModelForm):
    class Meta:
        model = Buying
        fields = '__all__'
        widgets = {
            'total_amount': forms.NumberInput(
                attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class BuyingEntryModelForm(forms.ModelForm):
    class Meta:
        model = BuyingEntry
        fields = ('product', 'quantity', 'partition')
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'partition': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_partition(self):
        product = self.cleaned_data.get('product')
        partition = self.cleaned_data.get('partition')
        if product.is_portionable and not partition:
            raise forms.ValidationError(
                'Vous devez choisir la formule de partition a appliquée sur la quantité achetée')
        return partition


class UserCreationForm(BaseUserCreationForm):
    email = forms.EmailField(
        required=False,
        label='Adresse email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': "Nom d'utilisateur du caissier"
        }


class DrinkModelForm(AbstractSellableModelForm):
    class Meta:
        model = Drink
        fields = ('name', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class InvoiceModelForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ('room', 'date')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-select'})
        }


class InvoiceEntryDrinkModelForm(forms.ModelForm):
    choices = forms.ModelChoiceField(
        queryset=Drink.objects.all(),
        label='Choisissez la boisson',
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}))
    class Meta:
        model = InvoiceEntry
        fields = ('choices', 'quantity', )
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1})
        }
        labels = {
            'quantity': 'Nombre de bouteilles'
        }


class InvoiceEntryDishModelForm(forms.ModelForm):
    choices = forms.ModelChoiceField(
        queryset=Dish.objects.all(),
        label='Choisissez la boisson',
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}))
  
    class Meta:
        model = InvoiceEntry
        fields = ('quantity', )
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1})
        }
        labels = {
            'quantity': 'Nombre de plats'
        }