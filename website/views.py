from django.shortcuts import render

from website.forms import ChangePasswordForm, SignUpForm, LoginForm
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from django.urls import reverse
from django.urls import reverse_lazy

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib import auth
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

def password_change_done(request):
    """View function showing success message after login."""
    context = {
        'foo': 'bar',
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'password_change_done.html', context=context)

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
                auth.login(request, user)
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

def login_view(request):
    #is user already logged in?
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login-complete'))
        print("user was already logged in")

    #If we receive POST data
    if request.method == 'POST':
        print("Received post request")
        # Create a form instance and populate it with data from the request (binding):
        form = LoginForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            print("form was valid")
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print("username was: %s and password: " % username, password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("user was not none")
                auth.login(request, user)
                print("user is: %s" % request.user)
                print("user is authenticated?: %s" % request.user.is_authenticated)
                return HttpResponseRedirect(reverse('login-complete'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = LoginForm
    context = {
        'form': form,
    }
    return render(request, 'login_form.html', context)

def login_complete(request):
    print("IN login_complete_view: user is authenticated?: %s" % request.user.is_authenticated)
    """View function showing success message after login."""
    context = {
        'foo': 'bar',
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'login_complete.html', context=context)

def logout_view(request):
    """View function showing success message after logout."""
    auth.logout(request)
    context = {
        'foo': 'bar',
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'logout_complete.html', context=context)
