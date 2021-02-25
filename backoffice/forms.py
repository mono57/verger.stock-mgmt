from django import forms
from django.forms import widgets

from backoffice.models import Dish, Product, Room

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'partition')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
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

class DishModelForm(forms.ModelForm):

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
            # self.initial[field_name] = 0
    class Meta:
        model = Dish
        fields = ('name', 'partition')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'partition': forms.Select(attrs={'class': 'form-control'}),
        }

    # def clean_partition(self):
    #     partition = self.cleaned_data.get('partition')
    #     if partition is None:
    #         raise forms.ValidationError('Renseigner une formule de partiton')
    #     return partition