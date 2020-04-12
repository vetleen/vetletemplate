from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email

from django.contrib import messages

class SignUpForm(forms.Form):
    username = forms.EmailField(max_length = 150, label="Email address", widget=forms.TextInput(attrs={'type':'input'}))
    password = forms.CharField(max_length = 20, label="Choose a password", widget=forms.TextInput(attrs={'type':'password'}))
    confirm_password = forms.CharField(max_length = 20, label="Confirm password", widget=forms.TextInput(attrs={'type':'password'}))

    def clean(self):
        if 'username' in self.cleaned_data:
            if User.objects.filter(username=self.cleaned_data['username']).exists():
                raise forms.ValidationError(
                    "Oh no! Someone already signed up with that email (%(taken_email)s).",
                    code='invalid',
                    params={'taken_email': self.cleaned_data['username']}
                )
            if 'password' in self.cleaned_data and 'confirm_password' in self.cleaned_data:
                if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
                    raise forms.ValidationError(
                        "The second new password you entered did not match the first. Please try again.",
                        code='invalid',
                        )
            return self.cleaned_data

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length = 20, label="Current password",widget=forms.TextInput(attrs={'type':'password', 'placeholder':'Old Password'}))
    new_password = forms.CharField(max_length = 20, label="Enter a new password",widget=forms.TextInput(attrs={'type':'password', 'placeholder':'New Password'}))
    confirm_new_password = forms.CharField(max_length = 20, label="Confirm new password", widget=forms.TextInput(attrs={'type':'password', 'placeholder':'Confirm New Password'}))

    def clean(self):
        if 'new_password' in self.cleaned_data and 'confirm_new_password' in self.cleaned_data:
            if self.cleaned_data['new_password'] != self.cleaned_data['confirm_new_password']:
                raise forms.ValidationError(
                    "The second new password you entered did not match the first. Please try again.",
                    code='invalid',
                    )
        return self.cleaned_data

class LoginForm(forms.Form):
    username = forms.EmailField(max_length = 150, label="Email address", widget=forms.TextInput(attrs={'type':'input'}))
    password = forms.CharField(max_length = 20, label="Password", widget=forms.TextInput(attrs={'type':'password'}))
    def clean(self):
        return self.cleaned_data

class EditAccountForm(forms.Form):
    username = forms.EmailField(max_length = 150, label="Email address", help_text="You email is also your username.", widget=forms.TextInput(attrs={'type':'email'}))

    def clean(self):
        if 'username' in self.cleaned_data:
            if User.objects.filter(username=self.cleaned_data['username']).exists():
                raise forms.ValidationError(
                    "Oh no! We couldn't update your email. Someone already has a user with the email %(taken_email)s.",
                    code='invalid',
                    params={'taken_email': self.cleaned_data['username']}
                )
            return self.cleaned_data
