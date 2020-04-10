from django.shortcuts import render

from website.forms import ChangePasswordForm, SignUpForm, LoginForm, EditAccountForm
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

from django.contrib import messages
#from catalog.models import ...

# Create your views here.
def index(request):
    """View function for home page of site."""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))
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
            messages.success(request, 'Your password was changed.', extra_tags='alert alert-success')
            return render(request, 'you_did_something.html')

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
        messages.error(request, 'You are already signed up.', extra_tags='alert alert-warning')
        return render(request, 'you_did_something.html')

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = SignUpForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['username'], form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Welcome aboard. Check out your dashboard next?.', extra_tags='alert alert-success')
            if user is not None:
                auth.login(request, user)
            # redirect to a new URL:

            return render(request, 'you_did_something.html')

    # If this is a GET (or any other method) create the default form.
    else:
        form = SignUpForm
    context = {
        'form': form,
    }

    return render(request, 'sign_up_form.html', context)

def login_view(request):
    #is user already logged in?
    if request.user.is_authenticated:
        messages.error(request, 'You are already logged in.', extra_tags='alert alert-error')
        return render(request, 'you_did_something.html')

    #If we receive POST data
    if request.method == 'POST':
        #print("Received post request")
        # Create a form instance and populate it with data from the request (binding):
        form = LoginForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            #print("form was valid")
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #print("username was: %s and password: " % username, password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                #print("user was not none")
                auth.login(request, user)
                #print("user is: %s" % request.user)
                #print("user is authenticated?: %s" % request.user.is_authenticated)
                messages.success(request, 'You have logged in.', extra_tags='alert alert-success')
                return render(request, 'you_did_something.html')

    # If this is a GET (or any other method) create the default form.
    else:
        form = LoginForm
    context = {
        'form': form,
    }
    return render(request, 'login_form.html', context)

def logout_view(request):
    """View function showing success message after logout."""
    auth.logout(request)
    messages.success(request, 'You have logged out.', extra_tags='alert alert-success')
    return render(request, 'you_did_something.html')

@login_required
def edit_account_view(request):
    """View function for editing account"""
    if request.user.is_authenticated:
        form = EditAccountForm(initial={'username': request.user})
        #If we receive POST data
        context = {
            'form': form
        }
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request (binding):
            form = EditAccountForm(request.POST)
            context.update({'form': form})
            # Check if the form is valid:
            if form.is_valid():
                #print("form was valid")
                # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
                new_username = form.cleaned_data['username']
                request.user.username = new_username
                request.user.email = new_username
                request.user.save()
                messages.success(request, 'Your profile details was updated.', extra_tags='alert alert-success')
                return render(request, 'form_renderer.html', context)
            else:
                pass
                #create error-messaged
                #my_errors = form.errors.as_data()
                #print(my_errors)
                #my_errors = my_errors['__all__']
                #for v_error in my_errors:
                #    for error_string in v_error:
                #        messages.error(request, error_string, extra_tags='alert alert-danger')

        return render(request, 'form_renderer.html', context)
    #if user not authenticated
    else:
        #this should never occcur
        messages.error(request, "Can't edit profile when you are not logged in.", extra_tags='alert alert-danger')
        return HttpResponseRedirect(reverse('login-view'))

@login_required
def dashboard_view(request):
    """View function for the dashboard"""
    messages.info(request, 'You have reached the dashboard.', extra_tags='alert alert-info')
    messages.success(request, 'Success!.', extra_tags='alert alert-success')
    messages.warning(request, 'the dashboard is under construction', extra_tags='alert alert-warning')
    context = {
        'foo': 'bar',
    }
    return render(request, 'dashboard.html', context)
