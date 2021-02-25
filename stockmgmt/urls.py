from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import RedirectView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('backoffice/', include('backoffice.urls', namespace='backoffice')),
    path('', RedirectView.as_view(url='/backoffice')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('passwords/change/', PasswordChangeView.as_view(), name='password_change_view'),
    path('passwords/change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('admin/', admin.site.urls),
]
