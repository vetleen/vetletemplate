from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.Form):
    username = forms.EmailField(max_length = 150, label="Email", widget=forms.TextInput(attrs={'type':'input'}))
    password = forms.CharField(max_length = 20, label="Password", widget=forms.TextInput(attrs={'type':'password'}))
    confirm_password = forms.CharField(max_length = 20, label="Confrim password", widget=forms.TextInput(attrs={'type':'password'}))

    def clean(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError(u'Oh no! Someone already signed up with that email ("%s").' % self.cleaned_data['username'])

        if 'password' in self.cleaned_data and 'confirm_password' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
                raise forms.ValidationError("The second password you entered did not match the first. Please try again.")

        return self.cleaned_data



class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'type':'password', 'placeholder':'Old Password'}))
    new_password = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'type':'password', 'placeholder':'New Password'}))
    confirm_new_password = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'type':'password', 'placeholder':'Confirm New Password'}))


    def clean(self):
        if 'new_password' in self.cleaned_data and 'confirm_new_password' in self.cleaned_data:
            if self.cleaned_data['new_password'] != self.cleaned_data['confirm_new_password']:
                raise forms.ValidationError("The second new password you entered did not match the first. Please try again.")
        return self.cleaned_data
