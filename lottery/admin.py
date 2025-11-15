from django.contrib import admin
from .models import LotteryType, LotteryDraw, LotteryTicket, UserProfile, Transaction


@admin.register(LotteryType)
class LotteryTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'max_number', 'numbers_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    ordering = ['-created_at']


@admin.register(LotteryDraw)
class LotteryDrawAdmin(admin.ModelAdmin):
    list_display = ['lottery_type', 'draw_number', 'draw_date', 'is_drawn', 'winning_numbers']
    list_filter = ['lottery_type', 'is_drawn', 'draw_date']
    search_fields = ['draw_number']
    ordering = ['-draw_date']
    readonly_fields = ['winning_numbers']


@admin.register(LotteryTicket)
class LotteryTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'user', 'lottery_draw', 'selected_numbers', 'is_winning', 'winning_amount', 'purchase_time']
    list_filter = ['lottery_draw__lottery_type', 'is_winning', 'is_claimed', 'purchase_time']
    search_fields = ['ticket_number', 'user__username']
    ordering = ['-purchase_time']
    readonly_fields = ['ticket_number', 'purchase_time']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'balance', 'total_spent', 'total_won']
    search_fields = ['user__username', 'phone']
    ordering = ['-total_spent']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'amount', 'description', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['user__username', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at']