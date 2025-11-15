from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from lottery.models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="邮箱")
    phone = forms.CharField(max_length=20, required=False, label="手机号")
    
    class Meta:
        model = User
        fields = ("username", "email", "phone", "password1", "password2")
        labels = {
            'username': '用户名',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = "密码"
        self.fields['password2'].label = "确认密码"
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # 创建用户资料
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
            'phone': '手机号',
        }
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class RechargeForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        min_value=1,
        label="充值金额",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
