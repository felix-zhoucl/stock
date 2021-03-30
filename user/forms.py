from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class createUserForm(UserCreationForm):
    error_messages = {
        'password_mismatch': ('两次输入的密码不相同'),
    }
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': '请输入邮箱', 'class': 'form-control input'}), label='邮箱')
    username = forms.CharField(max_length=20,widget=forms.TextInput(attrs={
                                 'placeholder': '请输入用户名', 'class': 'form-control input'
                                }),label='用户名'
                               )
    password1 = forms.CharField(max_length=20,
                                widget=forms.PasswordInput(attrs={'placeholder': '请输入密码', 'class': 'form-control input','type':'password'}),
                                label='请输入密码')
    password2 = forms.CharField(max_length=20,
                                widget=forms.PasswordInput(attrs={'placeholder': '请确认密码', 'class': 'form-control input','type':'password'}),
                                label='请确认密码')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
