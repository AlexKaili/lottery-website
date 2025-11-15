from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.core.paginator import Paginator
from .models import LotteryType, LotteryDraw, LotteryTicket, UserProfile, Transaction
from .forms import LotteryPurchaseForm


def home(request):
    """首页"""
    lottery_types = LotteryType.objects.filter(is_active=True)
    recent_draws = LotteryDraw.objects.filter(is_drawn=True).order_by('-draw_date')[:5]
    
    context = {
        'lottery_types': lottery_types,
        'recent_draws': recent_draws,
    }
    return render(request, 'lottery/home.html', context)


def lottery_list(request):
    """彩票列表"""
    lottery_types = LotteryType.objects.filter(is_active=True)
    return render(request, 'lottery/lottery_list.html', {'lottery_types': lottery_types})


@login_required
def purchase_lottery(request, lottery_type_id):
    """购买彩票"""
    lottery_type = get_object_or_404(LotteryType, id=lottery_type_id, is_active=True)
    
    # 获取或创建用户资料
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    # 获取当前期次
    current_draw = LotteryDraw.objects.filter(
        lottery_type=lottery_type,
        is_drawn=False
    ).first()
    
    if not current_draw:
        # 创建新期次
        draw_number = f"{timezone.now().strftime('%Y%m%d')}-001"
        current_draw = LotteryDraw.objects.create(
            lottery_type=lottery_type,
            draw_number=draw_number,
            draw_date=timezone.now() + timezone.timedelta(hours=1)
        )
    
    if request.method == 'POST':
        form = LotteryPurchaseForm(request.POST)
        if form.is_valid():
            # 检查余额
            if user_profile.balance < lottery_type.price:
                messages.error(request, '余额不足，请先充值！')
                return redirect('accounts:recharge')
            
            with transaction.atomic():
                # 创建彩票
                ticket = LotteryTicket.objects.create(
                    user=request.user,
                    lottery_draw=current_draw,
                    selected_numbers=form.cleaned_data['selected_numbers'],
                    is_auto_select=form.cleaned_data['is_auto_select']
                )
                
                # 扣除余额
                user_profile.balance -= lottery_type.price
                user_profile.total_spent += lottery_type.price
                user_profile.save()
                
                # 创建交易记录
                Transaction.objects.create(
                    user=request.user,
                    transaction_type='purchase',
                    amount=lottery_type.price,
                    description=f'购买彩票 {lottery_type.name} - {ticket.ticket_number}'
                )
            
            messages.success(request, f'购买成功！彩票号码：{ticket.ticket_number}')
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
    """我的彩票"""
    tickets_list = LotteryTicket.objects.filter(user=request.user).order_by('-purchase_time')
    
    paginator = Paginator(tickets_list, 10)
    page_number = request.GET.get('page')
    tickets = paginator.get_page(page_number)
    
    return render(request, 'lottery/my_tickets.html', {'tickets': tickets})


def draw_results(request):
    """开奖结果"""
    draws_list = LotteryDraw.objects.filter(is_drawn=True).order_by('-draw_date')
    
    paginator = Paginator(draws_list, 10)
    page_number = request.GET.get('page')
    draws = paginator.get_page(page_number)
    
    return render(request, 'lottery/draw_results.html', {'draws': draws})


def lottery_detail(request, lottery_type_id):
    """彩票详情"""
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
    """检查中奖"""
    # 检查用户所有未检查的彩票
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
        messages.success(request, f'恭喜！您有 {len(winning_tickets)} 张彩票中奖，总奖金 {total_winnings} 元！')
    else:
        messages.info(request, '很遗憾，暂时没有中奖彩票。')
    
    return render(request, 'lottery/check_winnings.html', {
        'winning_tickets': winning_tickets,
        'total_winnings': total_winnings
    })


@login_required
def claim_prize(request, ticket_id):
    """兑奖"""
    ticket = get_object_or_404(LotteryTicket, id=ticket_id, user=request.user, is_winning=True)
    
    if ticket.is_claimed:
        messages.warning(request, '该彩票已经兑奖！')
        return redirect('lottery:my_tickets')
    
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    with transaction.atomic():
        # 更新用户余额
        user_profile.balance += ticket.winning_amount
        user_profile.total_won += ticket.winning_amount
        user_profile.save()
        
        # 标记为已兑奖
        ticket.is_claimed = True
        ticket.save()
        
        # 创建交易记录
        Transaction.objects.create(
            user=request.user,
            transaction_type='winning',
            amount=ticket.winning_amount,
            description=f'兑奖 {ticket.ticket_number} - {ticket.winning_amount} 元'
        )
    
    messages.success(request, f'兑奖成功！获得奖金 {ticket.winning_amount} 元')
    return redirect('lottery:my_tickets')