from django.urls import path
from backoffice.views import (
    BuyingCreateView, BuyingEntryCreateView, DishCreateView, ProductCreateView, 
    DashboardTemplateView, ProductListView, 
    RoomCreateView, RoomListView, RoomUpdateView)

app_name = 'backoffice'

urlpatterns = [
    path('', DashboardTemplateView.as_view(template_name='index.html'), name='home'),
    path('product/add/', ProductCreateView.as_view(), name='product-add'),
    path('product/list/', ProductListView.as_view(), name='product-list'),
    path('room/add/', RoomCreateView.as_view(), name="room-add"),
    path('room/list/', RoomListView.as_view(), name="room-list"),
    path('room/<int:pk>/update/', RoomUpdateView.as_view(), name="room-update"),
    path('dish/add/', DishCreateView.as_view(), name='dish-add'),
    path('buying/add/', BuyingCreateView.as_view(), name='buying-add'),
    path(
        'buying/<int:buying_pk>/product/add/', 
        BuyingEntryCreateView.as_view(), 
        name='buying-product-add'),
]