from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import CustomUserCreationForm, UserProfileForm, RechargeForm
from lottery.models import UserProfile, Transaction, LotteryTicket


def register(request):
    """用户注册"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '注册成功！欢迎加入彩票网站！')
            return redirect('lottery:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    """用户资料页面"""
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, '资料更新成功！')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    # 获取用户的彩票购买记录
    tickets = LotteryTicket.objects.filter(user=request.user).order_by('-purchase_time')[:10]
    
    # 获取交易记录
    transactions = Transaction.objects.filter(user=request.user)[:10]
    
    context = {
        'form': form,
        'user_profile': user_profile,
        'tickets': tickets,
        'transactions': transactions,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def recharge(request):
    """账户充值"""
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = RechargeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            with transaction.atomic():
                # 更新用户余额
                user_profile.balance += amount
                user_profile.save()
                
                # 创建交易记录
                Transaction.objects.create(
                    user=request.user,
                    transaction_type='recharge',
                    amount=amount,
                    description=f'账户充值 {amount} 元'
                )
            
            messages.success(request, f'充值成功！已充值 {amount} 元')
            return redirect('accounts:profile')
    else:
        form = RechargeForm()
    
    return render(request, 'accounts/recharge.html', {'form': form, 'user_profile': user_profile})