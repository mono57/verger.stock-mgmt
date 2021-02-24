from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('backoffice/', include('backoffice.urls', namespace='backoffice')),
    path('', RedirectView.as_view(url='/backoffice')),
    path('login/', LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
]
