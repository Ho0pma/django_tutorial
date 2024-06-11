from  django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    # раскоментить если хотим свои стили
    # username = forms.CharField(
    #     label='Логин',
    #     widget=forms.TextInput(attrs={'class': 'form-input'})
    # )
    # password = forms.CharField(
    #     label='Пароль',
    #     widget=forms.PasswordInput(attrs={'class': 'form-input'})
    # )

    # связка с моделью
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']