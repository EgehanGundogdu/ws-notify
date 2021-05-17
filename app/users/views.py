from typing import Any

from django import http
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserCreationForm


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("users:login")
    template_name = "users/register.html"

    def dispatch(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse:
        if request.user.is_authenticated:
            return redirect('/admin') #FIXME 
        return super().dispatch(request, *args, **kwargs)
