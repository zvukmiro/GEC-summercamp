from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CustomUserCreationForm
from .models import CustomUser

# from django.core.exceptions import PermissionDenied -- does not work and does not show 403.html

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registeruser/signup.html'

class CustomUserUpdate(LoginRequiredMixin, UpdateView):
    model = CustomUser
    def get_queryset(self):
        qs = super().get_queryset().filter(id=self.request.user.id)
        if qs is None:
            #raise ObjectDoesNotExist("User can only change her/his own info.")
            raise Http404("One can edit her/his own info, only.")
        else:
            return qs
    fields = ['username', 'first_name', 'last_name', 'address', 'phone']
    template_name = 'registeruser/edit_user.html'
    def get_success_url(self):
        user_id = self.request.user.id # Get user_id from request
        return reverse_lazy('parent-detail', args=[str(user_id)]) # kwargs={'id': user_id})
