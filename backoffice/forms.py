from django import forms
from django.forms import widgets

from backoffice.models import Product

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