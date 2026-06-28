from django import forms
from django.contrib.auth import authenticate
from .models import CustomUser
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if not user:
            raise ValidationError("The password or username is incorrect!")
        
        cleaned_data['user'] = user
        
        return cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError('Parollar bir xil ems')
        return cleaned_data



    def clean_username(self):
        username = self.cleaned_data.get("username")

        if len(username) < 5:
            raise ValidationError("Usarname 8 ta harfdan kam bo'lmasin")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")

        if len(first_name) < 6:
            raise ValidationError("Ismingiz kamida 6 ta harfdan iborat bo'lsin")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")

        if len(last_name) < 7:
            raise ValidationError("Familyangiz kamida 7 harfdan iborat bo'lsin")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if len(email) < 15:
            raise ValidationError("Elektron manzilingiz kamida 10 ta harfdan iborat bo'lsin")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")

        if len(phone_number) < 9:
            raise ValidationError("Telefon raqamingiz 9 ta raqamdan iborat bo'lsin")
        return phone_number



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name','email', 'profile_img', 'age', 'phone_number' ]
