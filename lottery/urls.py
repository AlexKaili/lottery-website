from django.urls import path
from . import views

app_name = 'lottery'

urlpatterns = [
    path('', views.home, name='home'),
    path('lottery/', views.lottery_list, name='lottery_list'),
    path('lottery/<int:lottery_type_id>/', views.lottery_detail, name='lottery_detail'),
    path('purchase/<int:lottery_type_id>/', views.purchase_lottery, name='purchase_lottery'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('draw-results/', views.draw_results, name='draw_results'),
    path('check-winnings/', views.check_winnings, name='check_winnings'),
    path('claim-prize/<int:ticket_id>/', views.claim_prize, name='claim_prize'),
]
