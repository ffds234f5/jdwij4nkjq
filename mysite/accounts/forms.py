from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
        ('other', 'Другой'),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="Пол")
    custom_gender = forms.CharField(
        max_length=50,
        required=False,
        label="Укажите свой пол",
        widget=forms.TextInput(attrs={'placeholder': 'Введите свой пол'}),
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'gender', 'custom_gender']

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gender', 'custom_gender']
        widgets = {
            'gender': forms.RadioSelect(choices=UserProfile.GENDER_CHOICES),
            'custom_gender': forms.TextInput(attrs={'placeholder': 'Введите свой пол'}),
        }