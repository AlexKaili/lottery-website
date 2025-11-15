from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import CustomUserCreationForm, UserProfileForm, RechargeForm
from lottery.models import UserProfile, Transaction, LotteryTicket


def register(request):
    """사용자 등록"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '등록 성공! 복권 사이트에 오신 것을 환영합니다!')
            return redirect('lottery:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    """사용자 프로필 페이지"""
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필 업데이트 성공!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    # 사용자의 복권 구매 기록 가져오기
    tickets = LotteryTicket.objects.filter(user=request.user).order_by('-purchase_time')[:10]
    
    # 거래 기록 가져오기
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
    """계정 충전"""
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = RechargeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            with transaction.atomic():
                # 사용자 잔액 업데이트
                user_profile.balance += amount
                user_profile.save()
                
                # 거래 기록 생성
                Transaction.objects.create(
                    user=request.user,
                    transaction_type='recharge',
                    amount=amount,
                    description=f'계정 충전 {amount} 원'
                )
            
            messages.success(request, f'충전 성공! {amount} 원이 충전되었습니다')
            return redirect('accounts:profile')
    else:
        form = RechargeForm()
    
    return render(request, 'accounts/recharge.html', {'form': form, 'user_profile': user_profile})