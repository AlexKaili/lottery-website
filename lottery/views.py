from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.core.paginator import Paginator
from .models import LotteryType, LotteryDraw, LotteryTicket, UserProfile, Transaction
from .forms import LotteryPurchaseForm


def home(request):
    """홈페이지"""
    lottery_types = LotteryType.objects.filter(is_active=True)
    recent_draws = LotteryDraw.objects.filter(is_drawn=True).order_by('-draw_date')[:5]
    
    context = {
        'lottery_types': lottery_types,
        'recent_draws': recent_draws,
    }
    return render(request, 'lottery/home.html', context)


def lottery_list(request):
    """복권 목록"""
    lottery_types = LotteryType.objects.filter(is_active=True)
    return render(request, 'lottery/lottery_list.html', {'lottery_types': lottery_types})


@login_required
def purchase_lottery(request, lottery_type_id):
    """복권 구매"""
    lottery_type = get_object_or_404(LotteryType, id=lottery_type_id, is_active=True)
    
    # 사용자 프로필 가져오기 또는 생성
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    # 현재 회차 가져오기
    current_draw = LotteryDraw.objects.filter(
        lottery_type=lottery_type,
        is_drawn=False
    ).first()
    
    if not current_draw:
        # 새로운 회차 생성
        draw_number = f"{timezone.now().strftime('%Y%m%d')}-001"
        current_draw = LotteryDraw.objects.create(
            lottery_type=lottery_type,
            draw_number=draw_number,
            draw_date=timezone.now() + timezone.timedelta(hours=1)
        )
    
    if request.method == 'POST':
        form = LotteryPurchaseForm(request.POST)
        if form.is_valid():
            # 잔액 확인
            if user_profile.balance < lottery_type.price:
                messages.error(request, '잔액이 부족합니다. 먼저 충전해주세요!')
                return redirect('accounts:recharge')
            
            with transaction.atomic():
                # 복권 생성
                ticket = LotteryTicket.objects.create(
                    user=request.user,
                    lottery_draw=current_draw,
                    selected_numbers=form.cleaned_data['selected_numbers'],
                    is_auto_select=form.cleaned_data['is_auto_select']
                )
                
                # 잔액 차감
                user_profile.balance -= lottery_type.price
                user_profile.total_spent += lottery_type.price
                user_profile.save()
                
                # 거래 기록 생성
                Transaction.objects.create(
                    user=request.user,
                    transaction_type='purchase',
                    amount=lottery_type.price,
                    description=f'{lottery_type.name} 복권 구매 - {ticket.ticket_number}'
                )
            
            messages.success(request, f'구매 성공! 복권 번호: {ticket.ticket_number}')
            return redirect('lottery:my_tickets')
    else:
        form = LotteryPurchaseForm(initial={'lottery_type': lottery_type})
    
    context = {
        'form': form,
        'lottery_type': lottery_type,
        'current_draw': current_draw,
        'user_profile': user_profile,
    }
    return render(request, 'lottery/purchase.html', context)


@login_required
def my_tickets(request):
    """내 복권"""
    tickets_list = LotteryTicket.objects.filter(user=request.user).order_by('-purchase_time')
    
    paginator = Paginator(tickets_list, 10)
    page_number = request.GET.get('page')
    tickets = paginator.get_page(page_number)
    
    return render(request, 'lottery/my_tickets.html', {'tickets': tickets})


def draw_results(request):
    """추첨 결과"""
    draws_list = LotteryDraw.objects.filter(is_drawn=True).order_by('-draw_date')
    
    paginator = Paginator(draws_list, 10)
    page_number = request.GET.get('page')
    draws = paginator.get_page(page_number)
    
    return render(request, 'lottery/draw_results.html', {'draws': draws})


def lottery_detail(request, lottery_type_id):
    """복권 상세"""
    lottery_type = get_object_or_404(LotteryType, id=lottery_type_id)
    recent_draws = LotteryDraw.objects.filter(
        lottery_type=lottery_type,
        is_drawn=True
    ).order_by('-draw_date')[:10]
    
    context = {
        'lottery_type': lottery_type,
        'recent_draws': recent_draws,
    }
    return render(request, 'lottery/lottery_detail.html', context)


@login_required
def check_winnings(request):
    """당첨 확인"""
    # 사용자의 아직 확인하지 않은 복권을 확인
    tickets = LotteryTicket.objects.filter(
        user=request.user,
        lottery_draw__is_drawn=True,
        is_winning=False
    )
    
    winning_tickets = []
    total_winnings = 0
    
    for ticket in tickets:
        ticket.check_winning()
        if ticket.is_winning:
            winning_tickets.append(ticket)
            total_winnings += ticket.winning_amount
    
    if winning_tickets:
        messages.success(request, f'축하합니다! {len(winning_tickets)}장의 복권이 당첨되었고, 총 상금은 {total_winnings}원입니다!')
    else:
        messages.info(request, '아쉽게도 이번에는 당첨된 복권이 없습니다.')
    
    return render(request, 'lottery/check_winnings.html', {
        'winning_tickets': winning_tickets,
        'total_winnings': total_winnings
    })


@login_required
def claim_prize(request, ticket_id):
    """상금 수령"""
    ticket = get_object_or_404(LotteryTicket, id=ticket_id, user=request.user, is_winning=True)
    
    if ticket.is_claimed:
        messages.warning(request, '이 복권은 이미 상금이 수령되었습니다!')
        return redirect('lottery:my_tickets')
    
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    with transaction.atomic():
        # 사용자 잔액 업데이트
        user_profile.balance += ticket.winning_amount
        user_profile.total_won += ticket.winning_amount
        user_profile.save()
        
        # 상금 수령 처리
        ticket.is_claimed = True
        ticket.save()
        
        # 거래 기록 생성
        Transaction.objects.create(
            user=request.user,
            transaction_type='winning',
            amount=ticket.winning_amount,
            description=f'상금 수령 {ticket.ticket_number} - {ticket.winning_amount}원'
        )
    
    messages.success(request, f'상금 수령이 완료되었습니다! 당첨금 {ticket.winning_amount}원이 지급되었습니다.')
    return redirect('lottery:my_tickets')