#!/usr/bin/env python
"""
당첨 테스트 스크립트 - alex 사용자에게 당첨 복권 생성
"""
import os
import django

# Django 환경 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lottery_project.settings')
django.setup()

from django.contrib.auth.models import User
from lottery.models import LotteryType, LotteryDraw, LotteryTicket, UserProfile, Transaction
from django.utils import timezone
from datetime import timedelta

def create_winning_test():
    """당첨 테스트 생성"""
    print("당첨 테스트 생성 시작...")

    # 1. alex 사용자 조회 또는 생성
    try:
        alex_user = User.objects.get(username='alex')
        print(f"[OK] 사용자 찾음: {alex_user.username}")
    except User.DoesNotExist:
        alex_user = User.objects.create_user(
            username='alex',
            email='alex@example.com',
            password='alex12345'
        )
        print(f"[OK] 사용자 생성: {alex_user.username}")

    # 2. alex 프로필 조회 또는 생성
    try:
        alex_profile = alex_user.userprofile
    except UserProfile.DoesNotExist:
        alex_profile = UserProfile.objects.create(
            user=alex_user,
            balance=1000.00  # 충분한 잔액 설정
        )

    # 충분한 잔액인지 확인
    if alex_profile.balance < 100:
        alex_profile.balance = 1000.00
        alex_profile.save()

    print(f"[OK] 사용자 잔액: {alex_profile.balance}원")

    # 3. 로또 타입 가져오기
    lottery_type = LotteryType.objects.first()
    if not lottery_type:
        print("[FAIL] 로또 타입을 찾을 수 없습니다")
        return

    print(f"[OK] 로또 타입: {lottery_type.name}")

    # 4. 테스트용 추첨 회차 생성
    draw_number = f"TEST-{timezone.now().strftime('%Y%m%d%H%M%S')}"
    test_draw = LotteryDraw.objects.create(
        lottery_type=lottery_type,
        draw_number=draw_number,
        draw_date=timezone.now() + timedelta(minutes=1)  # 1분 뒤 추첨
    )
    print(f"[OK] 테스트 회차 생성: {test_draw.draw_number}")

    # 5. alex가 여러 장 복권을 구매 (한 장은 당첨 번호로 설정)
    winning_numbers = "1,2,3,4,5,6"  # 당첨 번호 지정

    # 당첨 복권 구매
    winning_ticket = LotteryTicket.objects.create(
        user=alex_user,
        lottery_draw=test_draw,
        selected_numbers=winning_numbers,
        is_auto_select=False
    )

    # 꽝 복권들 구매
    other_tickets = []
    for i, numbers in enumerate(["7,8,9,10,11,12", "13,14,15,16,17,18", "19,20,21,22,23,24"]):
        ticket = LotteryTicket.objects.create(
            user=alex_user,
            lottery_draw=test_draw,
            selected_numbers=numbers,
            is_auto_select=False
        )
        other_tickets.append(ticket)

    # 구매 비용 차감
    total_cost = float(lottery_type.price) * 4  # 복권 4장
    alex_profile.balance = float(alex_profile.balance) - total_cost
    alex_profile.total_spent = float(alex_profile.total_spent) + total_cost
    alex_profile.save()

    # 구매 트랜잭션 기록 생성
    Transaction.objects.create(
        user=alex_user,
        transaction_type='purchase',
        amount=total_cost,
        description=f'테스트 복권 구매 - 총 4장'
    )

    print(f"[OK] alex에게 4장의 복권이 구매되었습니다")
    print(f"   당첨 복권 번호: {winning_ticket.ticket_number} (선택 번호: {winning_numbers})")
    for i, ticket in enumerate(other_tickets):
        print(f"   일반 복권{i+1}: {ticket.ticket_number} (선택 번호: {ticket.selected_numbers})")

    # 6. 추첨 실행 - 당첨 번호를 alex의 번호로 설정
    test_draw.winning_numbers = winning_numbers
    test_draw.is_drawn = True
    test_draw.save()

    print(f"[OK] 추첨 완료, 당첨 번호: {winning_numbers}")

    # 7. 전체 복권 당첨 여부 확인
    all_tickets = LotteryTicket.objects.filter(lottery_draw=test_draw)
    winning_count = 0

    for ticket in all_tickets:
        ticket.check_winning()
        if ticket.is_winning:
            winning_count += 1
            print(f"[WIN] 당첨 복권: {ticket.ticket_number} - 상금: {ticket.winning_amount}원")

    print(f"[OK] 당첨 확인 완료, 총 {winning_count}장의 복권이 당첨되었습니다")

    # 8. 테스트 결과 출력
    print("\n" + "="*50)
    print("당첨 테스트 생성 완료!")
    print("="*50)
    print(f"사용자명: alex")
    print(f"비밀번호: alex12345")
    print(f"테스트 회차: {test_draw.draw_number}")
    print(f"당첨 번호: {winning_numbers}")
    print(f"당첨 복권: {winning_ticket.ticket_number}")
    print(f"상금: {winning_ticket.winning_amount}원")
    print("\n테스트 절차:")
    print("1. alex 계정으로 웹사이트 로그인")
    print("2. '내 복권' 메뉴에서 구매 내역 확인")
    print("3. '당첨 확인' 메뉴에서 당첨 결과 확인")
    print("4. '상금 받기' 클릭해서 상금 수령")
    print(f"\n웹사이트 주소: http://127.0.0.1:8000")

if __name__ == "__main__":
    create_winning_test()
