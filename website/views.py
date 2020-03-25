from django.shortcuts import render

from website.forms import ChangePasswordForm, SignUpForm
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from django.urls import reverse
from django.urls import reverse_lazy

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, login

#from catalog.models import ...

# Create your views here.
def index(request):
    """View function for home page of site."""

    context = {
        'foo': 'bar',
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

@login_required
def change_password(request):
    """View function for changing ones password."""
    user = request.user

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = ChangePasswordForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            update_session_auth_hash(request, request.user)
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('password_change_done'))

    # If this is a GET (or any other method) create the default form.
    else:

        form = ChangePasswordForm

    context = {
        'form': form,
    }

    return render(request, 'password_change_form.html', context)

def sign_up(request):
    """View function for signing up."""
    #logged in users are redirected
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('sign-up-complete'))

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = SignUpForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['username'], form.cleaned_data['password'])
            user.save()
            if user is not None:
                login(request, user)
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('sign-up-complete'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = SignUpForm
    context = {
        'form': form,
    }

    return render(request, 'sign_up_form.html', context)

def sign_up_complete(request):
    """View function showing success message after signup."""

    context = {
        'foo': 'bar',
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'sign_up_complete.html', context=context)
