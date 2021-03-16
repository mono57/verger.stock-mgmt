from django.urls import path
from backoffice.views import (
    AjaxRoomDishPrice, AjaxRoomDrinkPrice, BuyingCreateView, BuyingEntryCreateView,
    DishCreateView, DrinkCreateView, InvoiceCreateView,
    InvoiceEntryDishCreateView,
    InvoiceEntryDrinkCreateView, ProductCreateView,
    DashboardTemplateView, ProductListView,
    RoomCreateView, RoomListView, RoomUpdateView,
    UserActivateDeactivateView, UserCreateView,
    UserListView, state_sale, AjaxProductGetPartitionFormula,
    transfert_portion, ajax_get_max_portion_number)

app_name = 'backoffice'

urlpatterns = [
    path('', DashboardTemplateView.as_view(
        template_name='index.html'), name='home'),
    path('product/add/', ProductCreateView.as_view(), name='product-add'),
    path('product/list/', ProductListView.as_view(), name='product-list'),
    path('room/add/', RoomCreateView.as_view(), name="room-add"),
    path('room/list/', RoomListView.as_view(), name="room-list"),
    path('room/<int:pk>/update/', RoomUpdateView.as_view(), name="room-update"),
    path('dish/add/', DishCreateView.as_view(), name='dish-add'),
    path('buying/add/', BuyingCreateView.as_view(), name='buying-add'),
    path('user/add/', UserCreateView.as_view(), name='user-add'),
    path('user/list/', UserListView.as_view(), name='user-list'),
    path('drink/add/', DrinkCreateView.as_view(), name='drink-add'),
    path('invoice/add/', InvoiceCreateView.as_view(), name='invoice-add'),
    path(
        'invoice/<int:invoice_pk>/add/dish/',
        InvoiceEntryDishCreateView.as_view(),
        name='invoice_entry_dish-add'),
    path(
        'invoice/<int:invoice_pk>/add/drink/',
        InvoiceEntryDrinkCreateView.as_view(),
        name='invoice_entry_drink-add'),
    path(
        'user/activate/deactivate/',
        UserActivateDeactivateView.as_view(),
        name='activate_deactivate-user'),
    path(
        'buying/<int:buying_pk>/product/add/',
        BuyingEntryCreateView.as_view(),
        name='buying-product-add'),
    path('product/partition/formula/',
         AjaxProductGetPartitionFormula.as_view(),
         name='ajax-product-get-partition-formula'),
    path('dish/room/price/', AjaxRoomDishPrice.as_view(),
         name='dish-room-price'),
    path('drink/room/price/', AjaxRoomDrinkPrice.as_view(),
         name='drink-room-price'),
    path('state-sale', state_sale, name='state_sale'),
    path('transfert', transfert_portion, name='transfert_portion'),
    path('ajax/ajax_get_max_portion_number/',
         ajax_get_max_portion_number,
         name='ajax_get_max_portion_number'),
]
