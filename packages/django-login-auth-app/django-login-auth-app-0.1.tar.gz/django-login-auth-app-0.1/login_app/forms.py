from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="", max_length=50, widget=forms.TextInput(attrs={"placeholder": "Username", "name": "login-username"}))
    password = forms.CharField(label="", max_length=50, widget=forms.PasswordInput(attrs={"placeholder": "Password", "name": "login-password"}))
    

class SignupForm(forms.Form):
    username = forms.CharField(label="", max_length=50, widget=forms.TextInput(attrs={"placeholder": "Username", "name": "signup-username"}))
    email = forms.EmailField(label="", max_length=50, widget=forms.TextInput(attrs={"placeholder": "email", "name": "signup-email"}))
    password = forms.CharField(label="", max_length=50, widget=forms.PasswordInput(attrs={"placeholder": "Password", "name": "signup-password"}))
    password2 = forms.CharField(label="", max_length=50, widget=forms.PasswordInput(attrs={"placeholder": "Repeat Password", "name": "signup-password2"}))
    