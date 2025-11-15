from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import LotteryType, LotteryDraw, LotteryTicket, UserProfile, Transaction


class LotteryModelTests(TestCase):
    def setUp(self):
        """设置测试数据"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            balance=100.00
        )
        
        self.lottery_type = LotteryType.objects.create(
            name='测试彩票',
            description='测试用彩票',
            price=2.00,
            max_number=10,
            numbers_count=3
        )
        
        self.lottery_draw = LotteryDraw.objects.create(
            lottery_type=self.lottery_type,
            draw_number='TEST-001',
            draw_date=timezone.now() + timedelta(hours=1)
        )

    def test_lottery_type_creation(self):
        """测试彩票类型创建"""
        self.assertEqual(self.lottery_type.name, '测试彩票')
        self.assertEqual(self.lottery_type.price, 2.00)
        self.assertTrue(self.lottery_type.is_active)

    def test_lottery_draw_creation(self):
        """测试开奖期次创建"""
        self.assertEqual(self.lottery_draw.draw_number, 'TEST-001')
        self.assertFalse(self.lottery_draw.is_drawn)
        self.assertEqual(self.lottery_draw.lottery_type, self.lottery_type)

    def test_lottery_ticket_creation(self):
        """测试彩票购买"""
        ticket = LotteryTicket.objects.create(
            user=self.user,
            lottery_draw=self.lottery_draw,
            selected_numbers='1,2,3'
        )
        
        self.assertEqual(ticket.user, self.user)
        self.assertEqual(ticket.selected_numbers, '1,2,3')
        self.assertIsNotNone(ticket.ticket_number)
        self.assertFalse(ticket.is_winning)

    def test_winning_number_generation(self):
        """测试中奖号码生成"""
        self.lottery_draw.generate_winning_numbers()
        
        self.assertTrue(self.lottery_draw.is_drawn)
        self.assertIsNotNone(self.lottery_draw.winning_numbers)
        
        # 检查号码格式
        numbers = self.lottery_draw.winning_numbers.split(',')
        self.assertEqual(len(numbers), self.lottery_type.numbers_count)

    def test_winning_check(self):
        """测试中奖检查"""
        # 创建彩票
        ticket = LotteryTicket.objects.create(
            user=self.user,
            lottery_draw=self.lottery_draw,
            selected_numbers='1,2,3'
        )
        
        # 设置中奖号码
        self.lottery_draw.winning_numbers = '1,2,3'
        self.lottery_draw.is_drawn = True
        self.lottery_draw.save()
        
        # 检查中奖
        ticket.check_winning()
        
        self.assertTrue(ticket.is_winning)
        self.assertGreater(ticket.winning_amount, 0)

    def test_user_profile_creation(self):
        """测试用户资料创建"""
        self.assertEqual(self.user_profile.user, self.user)
        self.assertEqual(self.user_profile.balance, 100.00)
        self.assertEqual(self.user_profile.total_spent, 0)
        self.assertEqual(self.user_profile.total_won, 0)


class LotteryViewTests(TestCase):
    def setUp(self):
        """设置测试数据"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            balance=100.00
        )
        
        self.lottery_type = LotteryType.objects.create(
            name='测试彩票',
            description='测试用彩票',
            price=2.00,
            max_number=10,
            numbers_count=3
        )

    def test_home_page(self):
        """测试首页"""
        response = self.client.get(reverse('lottery:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '彩票网站')

    def test_lottery_list_page(self):
        """测试彩票列表页"""
        response = self.client.get(reverse('lottery:lottery_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '测试彩票')

    def test_user_registration(self):
        """测试用户注册"""
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        
        # 注册成功应该重定向
        self.assertEqual(response.status_code, 302)
        
        # 检查用户是否创建
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        """测试用户登录"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        
        # 登录成功应该重定向
        self.assertEqual(response.status_code, 302)

    def test_purchase_lottery_authenticated(self):
        """测试已登录用户购买彩票"""
        self.client.login(username='testuser', password='testpass123')
        
        # 创建开奖期次
        lottery_draw = LotteryDraw.objects.create(
            lottery_type=self.lottery_type,
            draw_number='TEST-001',
            draw_date=timezone.now() + timedelta(hours=1)
        )
        
        response = self.client.post(reverse('lottery:purchase_lottery', args=[self.lottery_type.id]), {
            'lottery_type': self.lottery_type.id,
            'selected_numbers': '1,2,3',
            'is_auto_select': False,
        })
        
        # 购买成功应该重定向
        self.assertEqual(response.status_code, 302)
        
        # 检查彩票是否创建
        self.assertTrue(LotteryTicket.objects.filter(user=self.user).exists())

    def test_purchase_lottery_unauthenticated(self):
        """测试未登录用户购买彩票"""
        response = self.client.get(reverse('lottery:purchase_lottery', args=[self.lottery_type.id]))
        
        # 应该重定向到登录页面
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_admin_dashboard_access(self):
        """测试管理后台访问"""
        # 创建管理员用户
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            is_staff=True
        )
        
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('management:admin_dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '管理后台')

    def test_admin_dashboard_access_denied(self):
        """测试普通用户访问管理后台被拒绝"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('management:admin_dashboard'))
        
        # 应该重定向到登录页面
        self.assertEqual(response.status_code, 302)


class TransactionTests(TestCase):
    def setUp(self):
        """设置测试数据"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            balance=50.00
        )

    def test_recharge_transaction(self):
        """测试充值交易"""
        # 创建充值交易
        transaction = Transaction.objects.create(
            user=self.user,
            transaction_type='recharge',
            amount=100.00,
            description='测试充值'
        )
        
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.transaction_type, 'recharge')
        self.assertEqual(transaction.amount, 100.00)

    def test_purchase_transaction(self):
        """测试购买交易"""
        transaction = Transaction.objects.create(
            user=self.user,
            transaction_type='purchase',
            amount=2.00,
            description='购买彩票'
        )
        
        self.assertEqual(transaction.transaction_type, 'purchase')
        self.assertEqual(transaction.amount, 2.00)

    def test_winning_transaction(self):
        """测试中奖交易"""
        transaction = Transaction.objects.create(
            user=self.user,
            transaction_type='winning',
            amount=20.00,
            description='中奖奖金'
        )
        
        self.assertEqual(transaction.transaction_type, 'winning')
        self.assertEqual(transaction.amount, 20.00)