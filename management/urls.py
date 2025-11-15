from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('sales-report/', views.sales_report, name='sales_report'),
    path('draw-management/', views.draw_management, name='draw_management'),
    path('conduct-draw/<int:draw_id>/', views.conduct_draw, name='conduct_draw'),
    path('create-draw/', views.create_draw, name='create_draw'),
    path('user-management/', views.user_management, name='user_management'),
    path('lottery-type-management/', views.lottery_type_management, name='lottery_type_management'),
]
