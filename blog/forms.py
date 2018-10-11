from django import forms
from .models import *
from django.contrib.auth.models import User

class PostCreateForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=(
            'title',
            'body',
            'status',
        )

class UserLoginForm(forms.Form):
        username=forms.CharField(label="")
        password=forms.CharField(label="",widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):

    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'enter password here....'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'confirm password....'}))

    class Meta:
        model=User
        fields=(
            'username',
            'first_name',
            'last_name',
            'email',
        )

    def clean_confirm_password(self):
        print('clean_confirm_password')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            print('password missmatch')
            raise forms.ValidationError("password missmatch")

        return confirm_password


class UserEditForm(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    email=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=(
            'dob',
            'photo',
        )

class PostEditForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=(
            'title',
            'body',
            'status',
        )

class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'write your comment here!!!', 'rows':'4', 'cols':'50'}))
    class Meta:
        model = Comments
        fields = ('content',)