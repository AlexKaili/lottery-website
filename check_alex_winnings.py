#!/usr/bin/env python
"""
检查alex用户的中奖情况
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lottery_project.settings')
django.setup()

from django.contrib.auth.models import User
from lottery.models import LotteryTicket, UserProfile

def check_alex_winnings():
    """检查alex的中奖情况"""
    try:
        alex_user = User.objects.get(username='alex')
        alex_profile = alex_user.userprofile
        
        print("Alex用户中奖情况检查")
        print("="*40)
        print(f"用户名: {alex_user.username}")
        print(f"当前余额: {alex_profile.balance}元")
        print(f"总消费: {alex_profile.total_spent}元")
        print(f"总中奖: {alex_profile.total_won}元")
        
        # 获取所有彩票
        all_tickets = LotteryTicket.objects.filter(user=alex_user).order_by('-purchase_time')
        print(f"\n彩票总数: {all_tickets.count()}张")
        
        # 中奖彩票
        winning_tickets = all_tickets.filter(is_winning=True)
        print(f"中奖彩票: {winning_tickets.count()}张")
        
        if winning_tickets.exists():
            print("\n中奖详情:")
            for ticket in winning_tickets:
                status = "已兑奖" if ticket.is_claimed else "未兑奖"
                print(f"  彩票号码: {ticket.ticket_number}")
                print(f"  选择号码: {ticket.selected_numbers}")
                print(f"  开奖号码: {ticket.lottery_draw.winning_numbers}")
                print(f"  奖金金额: {ticket.winning_amount}元")
                print(f"  兑奖状态: {status}")
                print(f"  购买时间: {ticket.purchase_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print("-" * 30)
        
        # 未中奖彩票
        non_winning_tickets = all_tickets.filter(is_winning=False, lottery_draw__is_drawn=True)
        if non_winning_tickets.exists():
            print(f"\n未中奖彩票: {non_winning_tickets.count()}张")
            for ticket in non_winning_tickets:
                print(f"  {ticket.ticket_number} - 选号: {ticket.selected_numbers}")
        
        # 待开奖彩票
        pending_tickets = all_tickets.filter(lottery_draw__is_drawn=False)
        if pending_tickets.exists():
            print(f"\n待开奖彩票: {pending_tickets.count()}张")
            for ticket in pending_tickets:
                print(f"  {ticket.ticket_number} - 选号: {ticket.selected_numbers}")
        
        print("\n" + "="*40)
        print("登录信息:")
        print("网站: http://127.0.0.1:8000")
        print("用户名: alex")
        print("密码: alex12345")
        
    except User.DoesNotExist:
        print("用户alex不存在")

if __name__ == "__main__":
    check_alex_winnings()
