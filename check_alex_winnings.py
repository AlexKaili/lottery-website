#!/usr/bin/env python
"""
alex 사용자의 당첨 내역 확인
"""
import os
import django

# Django 환경 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lottery_project.settings')
django.setup()

from django.contrib.auth.models import User
from lottery.models import LotteryTicket, UserProfile

def check_alex_winnings():
    """alex의 당첨 내역 확인"""
    try:
        alex_user = User.objects.get(username='alex')
        alex_profile = alex_user.userprofile
        
        print("Alex 사용자 당첨 내역 확인")
        print("="*40)
        print(f"사용자명: {alex_user.username}")
        print(f"현재 잔액: {alex_profile.balance}원")
        print(f"총 지출: {alex_profile.total_spent}원")
        print(f"총 당첨금: {alex_profile.total_won}원")
        
        # 모든 복권 조회
        all_tickets = LotteryTicket.objects.filter(user=alex_user).order_by('-purchase_time')
        print(f"\n총 복권 개수: {all_tickets.count()}장")
        
        # 당첨 복권
        winning_tickets = all_tickets.filter(is_winning=True)
        print(f"당첨 복권: {winning_tickets.count()}장")
        
        if winning_tickets.exists():
            print("\n당첨 상세 내역:")
            for ticket in winning_tickets:
                status = "지급 완료" if ticket.is_claimed else "미지급"
                print(f"  복권 번호: {ticket.ticket_number}")
                print(f"  선택 번호: {ticket.selected_numbers}")
                print(f"  추첨 번호: {ticket.lottery_draw.winning_numbers}")
                print(f"  당첨 금액: {ticket.winning_amount}원")
                print(f"  지급 상태: {status}")
                print(f"  구매 시각: {ticket.purchase_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print("-" * 30)
        
        # 미당첨 복권
        non_winning_tickets = all_tickets.filter(is_winning=False, lottery_draw__is_drawn=True)
        if non_winning_tickets.exists():
            print(f"\n미당첨 복권: {non_winning_tickets.count()}장")
            for ticket in non_winning_tickets:
                print(f"  {ticket.ticket_number} - 선택 번호: {ticket.selected_numbers}")
        
        # 추첨 대기 중인 복권
        pending_tickets = all_tickets.filter(lottery_draw__is_drawn=False)
        if pending_tickets.exists():
            print(f"\n추첨 대기 복권: {pending_tickets.count()}장")
            for ticket in pending_tickets:
                print(f"  {ticket.ticket_number} - 선택 번호: {ticket.selected_numbers}")
        
        print("\n" + "="*40)
        print("로그인 정보:")
        print("웹사이트: http://127.0.0.1:8000")
        print("사용자명: alex")
        print("비밀번호: alex12345")
        
    except User.DoesNotExist:
        print("alex 사용자가 존재하지 않습니다")

if __name__ == "__main__":
    check_alex_winnings()
