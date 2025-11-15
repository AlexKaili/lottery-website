from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from lottery.models import LotteryType, LotteryDraw, LotteryTicket, Transaction, UserProfile
from django.contrib.auth.models import User


@staff_member_required
def admin_dashboard(request):
    """管理员仪表板"""
    # 统计数据
    total_users = User.objects.count()
    total_tickets = LotteryTicket.objects.count()
    total_sales = Transaction.objects.filter(transaction_type='purchase').aggregate(
        total=Sum('amount'))['total'] or 0
    total_winnings = Transaction.objects.filter(transaction_type='winning').aggregate(
        total=Sum('amount'))['total'] or 0
    
    # 最近的彩票销售
    recent_tickets = LotteryTicket.objects.order_by('-purchase_time')[:10]
    
    # 待开奖的期次
    pending_draws = LotteryDraw.objects.filter(is_drawn=False).order_by('draw_date')
    
    context = {
        'total_users': total_users,
        'total_tickets': total_tickets,
        'total_sales': total_sales,
        'total_winnings': total_winnings,
        'recent_tickets': recent_tickets,
        'pending_draws': pending_draws,
    }
    return render(request, 'management/dashboard.html', context)


@staff_member_required
def sales_report(request):
    """销售报告"""
    # 按彩票类型统计销售
    lottery_sales = {}
    for lottery_type in LotteryType.objects.all():
        tickets = LotteryTicket.objects.filter(lottery_draw__lottery_type=lottery_type)
        total_tickets = tickets.count()
        total_amount = total_tickets * lottery_type.price
        
        lottery_sales[lottery_type.name] = {
            'tickets': total_tickets,
            'amount': total_amount,
        }
    
    # 按日期统计销售
    from django.db.models import Q
    from datetime import datetime, timedelta
    
    today = timezone.now().date()
    last_7_days = today - timedelta(days=7)
    last_30_days = today - timedelta(days=30)
    
    daily_sales = {}
    for i in range(7):
        date = today - timedelta(days=i)
        tickets = LotteryTicket.objects.filter(purchase_time__date=date)
        daily_sales[date.strftime('%Y-%m-%d')] = {
            'tickets': tickets.count(),
            'amount': sum(ticket.lottery_draw.lottery_type.price for ticket in tickets)
        }
    
    context = {
        'lottery_sales': lottery_sales,
        'daily_sales': daily_sales,
    }
    return render(request, 'management/sales_report.html', context)


@staff_member_required
def draw_management(request):
    """开奖管理"""
    draws = LotteryDraw.objects.order_by('-draw_date')
    return render(request, 'management/draw_management.html', {'draws': draws})


@staff_member_required
def conduct_draw(request, draw_id):
    """执行开奖"""
    draw = get_object_or_404(LotteryDraw, id=draw_id, is_drawn=False)
    
    if request.method == 'POST':
        # 生成中奖号码
        draw.generate_winning_numbers()
        
        # 检查所有相关彩票的中奖情况
        tickets = LotteryTicket.objects.filter(lottery_draw=draw)
        winning_count = 0
        
        for ticket in tickets:
            ticket.check_winning()
            if ticket.is_winning:
                winning_count += 1
        
        messages.success(request, f'开奖完成！中奖号码：{draw.winning_numbers}，共有 {winning_count} 张彩票中奖')
        return redirect('management:draw_management')
    
    # 获取该期次的彩票数量
    ticket_count = LotteryTicket.objects.filter(lottery_draw=draw).count()
    
    context = {
        'draw': draw,
        'ticket_count': ticket_count,
    }
    return render(request, 'management/conduct_draw.html', context)


@staff_member_required
def user_management(request):
    """用户管理"""
    users = User.objects.all().order_by('-date_joined')
    
    # 用户统计
    user_stats = []
    for user in users:
        try:
            profile = user.userprofile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
        
        tickets_count = LotteryTicket.objects.filter(user=user).count()
        winning_tickets = LotteryTicket.objects.filter(user=user, is_winning=True).count()
        
        user_stats.append({
            'user': user,
            'profile': profile,
            'tickets_count': tickets_count,
            'winning_tickets': winning_tickets,
        })
    
    return render(request, 'management/user_management.html', {'user_stats': user_stats})


@staff_member_required
def lottery_type_management(request):
    """彩票类型管理"""
    lottery_types = LotteryType.objects.all()
    return render(request, 'management/lottery_type_management.html', {'lottery_types': lottery_types})


@staff_member_required
def create_draw(request):
    """创建新期次"""
    if request.method == 'POST':
        lottery_type_id = request.POST.get('lottery_type')
        draw_date = request.POST.get('draw_date')
        
        lottery_type = get_object_or_404(LotteryType, id=lottery_type_id)
        
        # 生成期次号
        today = timezone.now().strftime('%Y%m%d')
        existing_draws = LotteryDraw.objects.filter(
            lottery_type=lottery_type,
            draw_number__startswith=today
        ).count()
        draw_number = f"{today}-{existing_draws + 1:03d}"
        
        draw = LotteryDraw.objects.create(
            lottery_type=lottery_type,
            draw_number=draw_number,
            draw_date=draw_date
        )
        
        messages.success(request, f'新期次创建成功：{draw_number}')
        return redirect('management:draw_management')
    
    lottery_types = LotteryType.objects.filter(is_active=True)
    return render(request, 'management/create_draw.html', {'lottery_types': lottery_types})