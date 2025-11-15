from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string


class LotteryType(models.Model):
    """彩票类型模型"""
    name = models.CharField(max_length=100, verbose_name="彩票名称")
    description = models.TextField(verbose_name="描述")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    max_number = models.IntegerField(verbose_name="最大号码")
    numbers_count = models.IntegerField(verbose_name="选择号码数量")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
        verbose_name = "彩票类型"
        verbose_name_plural = "彩票类型"
    
    def __str__(self):
        return self.name


class LotteryDraw(models.Model):
    """开奖期次模型"""
    lottery_type = models.ForeignKey(LotteryType, on_delete=models.CASCADE, verbose_name="彩票类型")
    draw_number = models.CharField(max_length=50, verbose_name="期次号")
    draw_date = models.DateTimeField(verbose_name="开奖时间")
    winning_numbers = models.CharField(max_length=200, verbose_name="中奖号码", blank=True)
    is_drawn = models.BooleanField(default=False, verbose_name="是否已开奖")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
        verbose_name = "开奖期次"
        verbose_name_plural = "开奖期次"
        unique_together = ['lottery_type', 'draw_number']
    
    def __str__(self):
        return f"{self.lottery_type.name} - {self.draw_number}"
    
    def generate_winning_numbers(self):
        """生成中奖号码"""
        if not self.is_drawn:
            numbers = random.sample(range(1, self.lottery_type.max_number + 1), 
                                  self.lottery_type.numbers_count)
            self.winning_numbers = ','.join(map(str, sorted(numbers)))
            self.is_drawn = True
            self.save()


class LotteryTicket(models.Model):
    """彩票购买记录模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    lottery_draw = models.ForeignKey(LotteryDraw, on_delete=models.CASCADE, verbose_name="开奖期次")
    ticket_number = models.CharField(max_length=50, unique=True, verbose_name="彩票号码")
    selected_numbers = models.CharField(max_length=200, verbose_name="选择的号码")
    is_auto_select = models.BooleanField(default=False, verbose_name="是否机选")
    purchase_time = models.DateTimeField(auto_now_add=True, verbose_name="购买时间")
    is_winning = models.BooleanField(default=False, verbose_name="是否中奖")
    winning_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="中奖金额")
    is_claimed = models.BooleanField(default=False, verbose_name="是否已兑奖")
    
    class Meta:
        verbose_name = "彩票"
        verbose_name_plural = "彩票"
    
    def __str__(self):
        return f"{self.user.username} - {self.ticket_number}"
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = self.generate_ticket_number()
        super().save(*args, **kwargs)
    
    def generate_ticket_number(self):
        """生成彩票号码"""
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        random_str = ''.join(random.choices(string.digits, k=4))
        return f"T{timestamp}{random_str}"
    
    def check_winning(self):
        """检查是否中奖"""
        if self.lottery_draw.is_drawn and not self.is_winning:
            winning_numbers = set(self.lottery_draw.winning_numbers.split(','))
            selected_numbers = set(self.selected_numbers.split(','))
            
            # 简单的中奖逻辑：匹配3个或以上号码即中奖
            matches = len(winning_numbers.intersection(selected_numbers))
            if matches >= 3:
                self.is_winning = True
                # 根据匹配数量计算奖金
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
    """用户扩展信息"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用户")
    phone = models.CharField(max_length=20, blank=True, verbose_name="手机号")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="账户余额")
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="总消费")
    total_won = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="总中奖金额")
    
    class Meta:
        verbose_name = "用户资料"
        verbose_name_plural = "用户资料"
    
    def __str__(self):
        return f"{self.user.username}的资料"


class Transaction(models.Model):
    """交易记录"""
    TRANSACTION_TYPES = [
        ('recharge', '充值'),
        ('purchase', '购买彩票'),
        ('winning', '中奖奖金'),
        ('withdraw', '提现'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, verbose_name="交易类型")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="金额")
    description = models.CharField(max_length=200, verbose_name="描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="交易时间")
    
    class Meta:
        verbose_name = "交易记录"
        verbose_name_plural = "交易记录"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_transaction_type_display()} - {self.amount}"