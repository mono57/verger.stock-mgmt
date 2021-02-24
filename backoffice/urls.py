from django.urls import path
from backoffice.views import (
    ProductCreateView, 
    DashboardTemplateView)

app_name = 'backoffice'

urlpatterns = [
    path('', DashboardTemplateView.as_view(template_name='index.html'), name='home'),
    path('product/add/', ProductCreateView.as_view(), name='product-add'),
]