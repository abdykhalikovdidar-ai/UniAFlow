from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# --- ФОРМА ОБНОВЛЕНИЯ ДАННЫХ ПОЛЬЗОВАТЕЛЯ ---
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label="Имя", required=False)
    last_name = forms.CharField(label="Фамилия", required=False)
    email = forms.EmailField(label="Email", required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

# --- ФОРМА ОБНОВЛЕНИЯ ПРОФИЛЯ (ВСЕ НОВЫЕ ПОЛЯ) ---
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        # ЗАМЕНИЛИ 'avatar' на 'image' И ДОБАВИЛИ НОВЫЕ ПОЛЯ:
        fields = [
            'image', 'bio', 'phone_number', 'gender', 'course', 'group_name',
            'birth_date', 'language', 'academic_year', 'study_duration', 'education_level'
        ]
        # Добавляем календарь для даты рождения
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем все поля профиля необязательными для заполнения
        for field in self.fields:
            self.fields[field].required = False

# --- ФОРМА РЕГИСТРАЦИИ ---
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Электронная почта")
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES, 
        label="Кто вы?", 
        initial='student', 
        widget=forms.RadioSelect()
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Логин"
        self.fields['email'].label = "Почта"
        for field in self.fields:
            self.fields[field].help_text = None

    def save(self, commit=True):
        user = super().save(commit=commit)
        selected_role = self.cleaned_data.get('role')
        # Создаем профиль сразу после регистрации
        Profile.objects.update_or_create(user=user, defaults={'role': selected_role})
        return user