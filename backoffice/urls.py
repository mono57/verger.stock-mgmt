from django.urls import path
from backoffice import views
app_name = 'backoffice'

urlpatterns = [
    path('', views.DashboardTemplateView.as_view(
        template_name='index.html'), name='home'),
    path('product/add/', views.ProductCreateView.as_view(), name='product-add'),
    path('product/list/', views.ProductListView.as_view(), name='product-list'),
    path('room/add/', views.RoomCreateView.as_view(), name="room-add"),
    path('room/list/', views.RoomListView.as_view(), name="room-list"),
    path('room/<int:pk>/update/', views.RoomUpdateView.as_view(), name="room-update"),
    path('dish/add/', views.DishCreateView.as_view(), name='dish-add'),
    path('buying/add/', views.BuyingCreateView.as_view(), name='buying-add'),
    path('user/add/', views.UserCreateView.as_view(), name='user-add'),
    path('user/list/', views.UserListView.as_view(), name='user-list'),
    path('restaurant/menu', views.menu_restaurant, name='menu_restaurant'),
    path('drink/add/', views.DrinkCreateView.as_view(), name='drink-add'),
    path('invoice/add/', views.InvoiceCreateView.as_view(), name='invoice-add'),
    path(
        'invoice/<int:invoice_pk>/add/dish/',
        views.InvoiceEntryDishCreateView.as_view(),
        name='invoice_entry_dish-add'),
    path(
        'invoice/<int:invoice_pk>/add/drink/',
        views.InvoiceEntryDrinkCreateView.as_view(),
        name='invoice_entry_drink-add'),
    path(
        'user/activate/deactivate/',
        views.UserActivateDeactivateView.as_view(),
        name='activate_deactivate-user'),
    path(
        'buying/<int:buying_pk>/product/add/',
        views.BuyingEntryCreateView.as_view(),
        name='buying-product-add'),
    path('product/partition/formula/',
         views.AjaxProductGetPartitionFormula.as_view(),
         name='ajax-product-get-partition-formula'),
    path('dish/room/price/', views.AjaxRoomDishPrice.as_view(),
         name='dish-room-price'),
    path('drink/room/price/', views.AjaxRoomDrinkPrice.as_view(),
         name='drink-room-price'),
    path('state-sale', views.state_sale, name='state_sale'),
    path('transfert', views.transfert_portion, name='transfert_portion'),
    path('ajax/ajax_get_max_portion_number/',
         views.ajax_get_max_portion_number,
         name='ajax_get_max_portion_number'),
]
