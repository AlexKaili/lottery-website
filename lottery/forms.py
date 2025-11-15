from django import forms
from .models import LotteryType, LotteryTicket
import random


class LotteryPurchaseForm(forms.Form):
    lottery_type = forms.ModelChoiceField(
        queryset=LotteryType.objects.filter(is_active=True),
        label="彩票类型",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_auto_select = forms.BooleanField(
        required=False,
        label="机选",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    selected_numbers = forms.CharField(
        max_length=200,
        required=False,
        label="选择号码（用逗号分隔）",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '例如: 1,5,12,23,35,42'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        lottery_type = cleaned_data.get('lottery_type')
        is_auto_select = cleaned_data.get('is_auto_select')
        selected_numbers = cleaned_data.get('selected_numbers')
        
        if not lottery_type:
            return cleaned_data
        
        if is_auto_select:
            # 机选号码
            numbers = random.sample(range(1, lottery_type.max_number + 1), 
                                  lottery_type.numbers_count)
            cleaned_data['selected_numbers'] = ','.join(map(str, sorted(numbers)))
        else:
            # 手动选择号码
            if not selected_numbers:
                raise forms.ValidationError("请选择号码或勾选机选")
            
            try:
                numbers = [int(x.strip()) for x in selected_numbers.split(',')]
            except ValueError:
                raise forms.ValidationError("号码格式不正确，请输入数字")
            
            if len(numbers) != lottery_type.numbers_count:
                raise forms.ValidationError(f"请选择 {lottery_type.numbers_count} 个号码")
            
            if any(num < 1 or num > lottery_type.max_number for num in numbers):
                raise forms.ValidationError(f"号码必须在 1 到 {lottery_type.max_number} 之间")
            
            if len(set(numbers)) != len(numbers):
                raise forms.ValidationError("号码不能重复")
            
            cleaned_data['selected_numbers'] = ','.join(map(str, sorted(numbers)))
        
        return cleaned_data


class NumberSelectionWidget(forms.Widget):
    """自定义号码选择组件"""
    template_name = 'lottery/widgets/number_selection.html'
    
    def __init__(self, max_number=49, numbers_count=6, *args, **kwargs):
        self.max_number = max_number
        self.numbers_count = numbers_count
        super().__init__(*args, **kwargs)
    
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['max_number'] = self.max_number
        context['numbers_count'] = self.numbers_count
        context['numbers'] = range(1, self.max_number + 1)
        if value:
            context['selected'] = [int(x) for x in value.split(',')]
        else:
            context['selected'] = []
        return context
