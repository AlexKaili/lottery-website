from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from lottery.models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="이메일")
    phone = forms.CharField(max_length=20, required=False, label="휴대폰 번호")
    
    class Meta:
        model = User
        fields = ("username", "email", "phone", "password1", "password2")
        labels = {
            'username': '사용자명',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = "비밀번호"
        self.fields['password2'].label = "비밀번호 확인"
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # 사용자 프로필 생성
            UserProfile.objects.create(
                user=user,
                phone=self.cleaned_data.get("phone", "")
            )
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone']
        labels = {
            'phone': '휴대폰 번호',
        }
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class RechargeForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        min_value=1,
        label="충전 금액",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
