from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from lottery.models import LotteryType, LotteryDraw, UserProfile
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = '初始化彩票网站数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化数据...')
        
        # 创建超级用户
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@lottery.com',
                password='admin123'
            )
            UserProfile.objects.create(user=admin_user, balance=10000)
            self.stdout.write(self.style.SUCCESS('创建管理员用户: admin/admin123'))
        
        # 创建测试用户
        if not User.objects.filter(username='testuser').exists():
            test_user = User.objects.create_user(
                username='testuser',
                email='test@lottery.com',
                password='test123'
            )
            UserProfile.objects.create(user=test_user, balance=500)
            self.stdout.write(self.style.SUCCESS('创建测试用户: testuser/test123'))
        
        # 创建彩票类型
        lottery_types_data = [
            {
                'name': '双色球',
                'description': '从1-33中选择6个红球号码，从1-16中选择1个蓝球号码',
                'price': 2.00,
                'max_number': 33,
                'numbers_count': 6,
            },
            {
                'name': '大乐透',
                'description': '从1-35中选择5个前区号码，从1-12中选择2个后区号码',
                'price': 2.00,
                'max_number': 35,
                'numbers_count': 5,
            },
            {
                'name': '福彩3D',
                'description': '从000-999中选择一个3位数号码',
                'price': 2.00,
                'max_number': 10,
                'numbers_count': 3,
            },
            {
                'name': '七乐彩',
                'description': '从1-30中选择7个号码',
                'price': 2.00,
                'max_number': 30,
                'numbers_count': 7,
            },
        ]
        
        for lottery_data in lottery_types_data:
            lottery_type, created = LotteryType.objects.get_or_create(
                name=lottery_data['name'],
                defaults=lottery_data
            )
            if created:
                self.stdout.write(f'创建彩票类型: {lottery_type.name}')
                
                # 为每个彩票类型创建一个待开奖期次
                draw_number = f"{timezone.now().strftime('%Y%m%d')}-001"
                draw_date = timezone.now() + timedelta(hours=2)
                
                LotteryDraw.objects.get_or_create(
                    lottery_type=lottery_type,
                    draw_number=draw_number,
                    defaults={
                        'draw_date': draw_date,
                    }
                )
                self.stdout.write(f'创建开奖期次: {draw_number}')
        
        self.stdout.write(self.style.SUCCESS('数据初始化完成！'))
