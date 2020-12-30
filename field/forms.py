from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    conform_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', "email")

    field_order = ['username', 'email', 'password', 'conform_password']

    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) >= 8:

            return password
        else:
            raise forms.ValidationError(
                " password should conatin min 8  character ")

    def clean_conform_password(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("conform_password")
        if password != password2:
            raise forms.ValidationError("passwords are not matching")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
