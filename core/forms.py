from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Resume, Vacancy, Response, VacancyReview
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'avatar', 'password1', 'password2')

    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.RadioSelect,
        label='Кто вы?'
    )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'avatar']


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['full_name', 'position', 'experience', 'skills']


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'description', 'requirements']


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vacancy'].widget = forms.HiddenInput()


class VacancyReviewForm(forms.ModelForm):
    class Meta:
        model = VacancyReview
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Напишите отклик на вакансию...'}),
        }
