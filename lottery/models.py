from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string


class LotteryType(models.Model):
    """복권 유형 모델"""
    name = models.CharField(max_length=100, verbose_name="복권 이름")
    description = models.TextField(verbose_name="설명")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="가격")
    max_number = models.IntegerField(verbose_name="최대 번호")
    numbers_count = models.IntegerField(verbose_name="선택 번호 수량")
    is_active = models.BooleanField(default=True, verbose_name="활성화 여부")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 시간")
    
    class Meta:
        verbose_name = "복권 유형"
        verbose_name_plural = "복권 유형"
    
    def __str__(self):
        return self.name


class LotteryDraw(models.Model):
    """추첨 회차 모델"""
    lottery_type = models.ForeignKey(LotteryType, on_delete=models.CASCADE, verbose_name="복권 유형")
    draw_number = models.CharField(max_length=50, verbose_name="회차 번호")
    draw_date = models.DateTimeField(verbose_name="추첨 시간")
    winning_numbers = models.CharField(max_length=200, verbose_name="당첨 번호", blank=True)
    is_drawn = models.BooleanField(default=False, verbose_name="추첨 완료 여부")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 시간")
    
    class Meta:
        verbose_name = "추첨 회차"
        verbose_name_plural = "추첨 회차"
        unique_together = ['lottery_type', 'draw_number']
    
    def __str__(self):
        return f"{self.lottery_type.name} - {self.draw_number}"
    
    def generate_winning_numbers(self):
        """당첨 번호 생성"""
        if not self.is_drawn:
            numbers = random.sample(range(1, self.lottery_type.max_number + 1), 
                                  self.lottery_type.numbers_count)
            self.winning_numbers = ','.join(map(str, sorted(numbers)))
            self.is_drawn = True
            self.save()


class LotteryTicket(models.Model):
    """복권 구매 기록 모델"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="사용자")
    lottery_draw = models.ForeignKey(LotteryDraw, on_delete=models.CASCADE, verbose_name="추첨 회차")
    ticket_number = models.CharField(max_length=50, unique=True, verbose_name="복권 번호")
    selected_numbers = models.CharField(max_length=200, verbose_name="선택한 번호")
    is_auto_select = models.BooleanField(default=False, verbose_name="자동 선택 여부")
    purchase_time = models.DateTimeField(auto_now_add=True, verbose_name="구매 시간")
    is_winning = models.BooleanField(default=False, verbose_name="당첨 여부")
    winning_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="당첨 금액")
    is_claimed = models.BooleanField(default=False, verbose_name="수령 완료 여부")
    
    class Meta:
        verbose_name = "복권"
        verbose_name_plural = "복권"
    
    def __str__(self):
        return f"{self.user.username} - {self.ticket_number}"
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = self.generate_ticket_number()
        super().save(*args, **kwargs)
    
    def generate_ticket_number(self):
        """복권 번호 생성"""
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        random_str = ''.join(random.choices(string.digits, k=4))
        return f"T{timestamp}{random_str}"
    
    def check_winning(self):
        """당첨 여부 확인"""
        if self.lottery_draw.is_drawn and not self.is_winning:
            winning_numbers = set(self.lottery_draw.winning_numbers.split(','))
            selected_numbers = set(self.selected_numbers.split(','))
            
            # 간단한 당첨 로직: 3개 이상 번호 일치 시 당첨
            matches = len(winning_numbers.intersection(selected_numbers))
            if matches >= 3:
                self.is_winning = True
                # 일치 수량에 따른 상금 계산
                base_amount = self.lottery_draw.lottery_type.price
                if matches == 3:
                    self.winning_amount = base_amount * 10
                elif matches == 4:
                    self.winning_amount = base_amount * 50
                elif matches == 5:
                    self.winning_amount = base_amount * 200
                elif matches >= 6:
                    self.winning_amount = base_amount * 1000
                self.save()


class UserProfile(models.Model):
    """사용자 확장 정보"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="사용자")
    phone = models.CharField(max_length=20, blank=True, verbose_name="휴대폰 번호")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="계정 잔액")
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="총 소비")
    total_won = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="총 당첨 금액")
    
    class Meta:
        verbose_name = "사용자 프로필"
        verbose_name_plural = "사용자 프로필"
    
    def __str__(self):
        return f"{self.user.username}의 프로필"


class Transaction(models.Model):
    """거래 기록"""
    TRANSACTION_TYPES = [
        ('recharge', '충전'),
        ('purchase', '복권 구매'),
        ('winning', '당첨 상금'),
        ('withdraw', '출금'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="사용자")
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, verbose_name="거래 유형")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="금액")
    description = models.CharField(max_length=200, verbose_name="설명")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="거래 시간")
    
    class Meta:
        verbose_name = "거래 기록"
        verbose_name_plural = "거래 기록"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_transaction_type_display()} - {self.amount}"