from typing import Any
from django import http
from django.contrib.auth.mixins import AccessMixin
from django.http.response import HttpResponse
from django.contrib import messages


class AdminLoginRequiredMixin(AccessMixin):
    def dispatch(self,
                 request,
                 *args,
                 **kwargs):
        if not request.user.is_superuser:
            messages.error(request, "Vous n'avez pas le droit d'y accéder")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
