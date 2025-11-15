#!/usr/bin/env python
"""
中奖测试脚本 - 为用户alex创建中奖彩票
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lottery_project.settings')
django.setup()

from django.contrib.auth.models import User
from lottery.models import LotteryType, LotteryDraw, LotteryTicket, UserProfile, Transaction
from django.utils import timezone
from datetime import timedelta

def create_winning_test():
    """创建中奖测试"""
    print("开始创建中奖测试...")
    
    # 1. 获取或创建用户alex
    try:
        alex_user = User.objects.get(username='alex')
        print(f"[OK] 找到用户: {alex_user.username}")
    except User.DoesNotExist:
        alex_user = User.objects.create_user(
            username='alex',
            email='alex@example.com',
            password='alex12345'
        )
        print(f"[OK] 创建用户: {alex_user.username}")
    
    # 2. 获取或创建用户资料
    try:
        alex_profile = alex_user.userprofile
    except UserProfile.DoesNotExist:
        alex_profile = UserProfile.objects.create(
            user=alex_user,
            balance=1000.00  # 给足够的余额
        )
    
    # 确保有足够余额
    if alex_profile.balance < 100:
        alex_profile.balance = 1000.00
        alex_profile.save()
    
    print(f"[OK] 用户余额: {alex_profile.balance}元")
    
    # 3. 获取彩票类型
    lottery_type = LotteryType.objects.first()
    if not lottery_type:
        print("[FAIL] 没有找到彩票类型")
        return
    
    print(f"[OK] 彩票类型: {lottery_type.name}")
    
    # 4. 创建一个新的开奖期次
    draw_number = f"TEST-{timezone.now().strftime('%Y%m%d%H%M%S')}"
    test_draw = LotteryDraw.objects.create(
        lottery_type=lottery_type,
        draw_number=draw_number,
        draw_date=timezone.now() + timedelta(minutes=1)  # 1分钟后开奖
    )
    print(f"[OK] 创建测试期次: {test_draw.draw_number}")
    
    # 5. 为alex购买几张彩票，其中一张设置为中奖号码
    winning_numbers = "1,2,3,4,5,6"  # 设定中奖号码
    
    # 购买中奖彩票
    winning_ticket = LotteryTicket.objects.create(
        user=alex_user,
        lottery_draw=test_draw,
        selected_numbers=winning_numbers,
        is_auto_select=False
    )
    
    # 购买几张不中奖的彩票
    other_tickets = []
    for i, numbers in enumerate(["7,8,9,10,11,12", "13,14,15,16,17,18", "19,20,21,22,23,24"]):
        ticket = LotteryTicket.objects.create(
            user=alex_user,
            lottery_draw=test_draw,
            selected_numbers=numbers,
            is_auto_select=False
        )
        other_tickets.append(ticket)
    
    # 扣除购买费用
    total_cost = float(lottery_type.price) * 4  # 4张彩票
    alex_profile.balance = float(alex_profile.balance) - total_cost
    alex_profile.total_spent = float(alex_profile.total_spent) + total_cost
    alex_profile.save()
    
    # 创建购买交易记录
    Transaction.objects.create(
        user=alex_user,
        transaction_type='purchase',
        amount=total_cost,
        description=f'测试购买彩票 - 共4张'
    )
    
    print(f"[OK] 为alex购买了4张彩票")
    print(f"   中奖彩票号码: {winning_ticket.ticket_number} (选号: {winning_numbers})")
    for i, ticket in enumerate(other_tickets):
        print(f"   普通彩票{i+1}: {ticket.ticket_number} (选号: {ticket.selected_numbers})")
    
    # 6. 执行开奖 - 设置中奖号码为alex的选号
    test_draw.winning_numbers = winning_numbers
    test_draw.is_drawn = True
    test_draw.save()
    
    print(f"[OK] 开奖完成，中奖号码: {winning_numbers}")
    
    # 7. 检查所有彩票的中奖情况
    all_tickets = LotteryTicket.objects.filter(lottery_draw=test_draw)
    winning_count = 0
    
    for ticket in all_tickets:
        ticket.check_winning()
        if ticket.is_winning:
            winning_count += 1
            print(f"[WIN] 中奖彩票: {ticket.ticket_number} - 奖金: {ticket.winning_amount}元")
    
    print(f"[OK] 中奖检测完成，共有 {winning_count} 张彩票中奖")
    
    # 8. 显示测试结果
    print("\n" + "="*50)
    print("中奖测试创建完成！")
    print("="*50)
    print(f"用户名: alex")
    print(f"密码: alex12345")
    print(f"测试期次: {test_draw.draw_number}")
    print(f"中奖号码: {winning_numbers}")
    print(f"中奖彩票: {winning_ticket.ticket_number}")
    print(f"奖金金额: {winning_ticket.winning_amount}元")
    print("\n测试步骤:")
    print("1. 使用alex账户登录网站")
    print("2. 访问'我的彩票'查看购买记录")
    print("3. 访问'检查中奖'查看中奖情况")
    print("4. 点击'立即兑奖'领取奖金")
    print(f"\n网站地址: http://127.0.0.1:8000")

if __name__ == "__main__":
    create_winning_test()
