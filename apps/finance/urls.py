from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
    path('transactions/add/', views.TransactionCreateView.as_view(), name='transaction_create'),
    path('transactions/<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='transaction_update'),
    path('transactions/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction_delete'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category_create'),
    path('budget/create/', views.BudgetCreateView.as_view(), name='budget-create'),
    path('budget/<int:pk>/edit/', views.BudgetUpdateView.as_view(), name='budget-update'),
    path('budget/<int:pk>/delete/', views.delete_budget, name='budget_delete'),
    path('savings/create/', views.SavingsGoalCreateView.as_view(), name='savings-create'),
    path('savings/<int:pk>/edit/', views.SavingsGoalUpdateView.as_view(), name='savings-update'),
    path('savings/<int:pk>/delete/', views.delete_goal, name='goal_delete'),
    path('api/charts/data/', views.chart_data_api, name='api_chart_data'),
]