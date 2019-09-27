from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from registeruser.models import CustomUser

from .models import CampPrice, CampTheme, CampWeek, Child


# Create your views here.
def index(request):
    campthemes = CampTheme.objects.all()
    context = {
        'camps': campthemes,
    }
    return render(request, 'camplist/index.html', context=context)

# Create generic views List and Detail
class CampThemeListView(generic.ListView):
    model = CampTheme

class CampThemeDetailView(generic.DetailView):
    model = CampTheme

# ChildDetailView
@login_required
def child_detail(request, pk):
    try:
        child = Child.objects.get(pk=pk)
        if child.parent==request.user:
            context = {
                'child': child,
            }
            return render(request, 'camplist/child_detail.html', context)
        else:
            message = 'Parents can only view their own children info.'
            context = {
                'message': message,
            }
            return render(request, 'camplist/error.html', context)
    except ObjectDoesNotExist:
        message="No child with id given."
        context = {
            'message':message,
        }
        return render(request, 'camplist/error.html', context)

class ParentDetailView(LoginRequiredMixin,generic.DetailView):
    model = get_user_model()
    def get_queryset(self):
        qs = super().get_queryset().filter(id=self.request.user.id)
        if qs is None:
            raise Http404("user ID not matching with that of the logged user.")
        else:
            return qs

class ChildCreate(LoginRequiredMixin, CreateView):
    model = Child
    parent = get_user_model()
    fields = ['first_name', 'last_name', 'dob', 'grade_in_fall', 'camps']
    template_name = 'camplist/add_child.html'

    def unique_name(self, *args, **kwargs):
        # does not work at all
        first_name = self.cleaned_data.get('first_name')

        qs = self.parent.children.filter(first_name__iexact=first_name)
        if qs.exists():
            raise forms.ValidationError("Each child has to have unique first name.")
        return first_name

    def form_valid(self, form):
        form.instance.parent = self.request.user
        return super(ChildCreate, self).form_valid(form)


class ChildUpdate(LoginRequiredMixin, UpdateView):
    model = Child
    def get_queryset(self):
        return Child.objects.filter(parent=self.request.user)
    fields = ['first_name', 'last_name', 'dob', 'grade_in_fall', 'camps']
    template_name = 'camplist/edit_child.html'


class ChildDelete(LoginRequiredMixin, DeleteView):
    model = Child
    def get_queryset(self):
        return Child.objects.filter(parent=self.request.user)
    success_url = reverse_lazy('camps')

# reverse('renew-book-librarian', kwargs={'pk':self.test_bookinstance1.pk,}), {'renewal_date':valid_date_in_future})
