from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PollutionReport
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

class PollutionReportForm(forms.ModelForm):
    class Meta:
        model = PollutionReport
        fields = ['pollution_type', 'location', 'description', 'image']
        # 可以透過 widgets 幫前端表單的輸入框加上 CSS class
        widgets = {
            'pollution_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例如：台中市高美濕地岸邊'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '請詳細說明污染狀況...'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }