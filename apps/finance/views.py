from decimal import Decimal
from django.db.models import Sum, Count, Avg, Q
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


from .models import Transaction, Budget, SavingsGoal
from .forms import TransactionForm, BudgetForm, SavingsGoalForm
from .filters import TransactionFilterForm


def landing(request):
    return render(request, 'landing.html')

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'finance/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        now = timezone.now()

        txs = Transaction.objects.filter(user=user)
        month_txs = txs.filter(date__year=now.year, date__month=now.month)

        agg = month_txs.aggregate(
            inc=Sum('amount', filter=Q(category__type='INCOME')),
            exp=Sum('amount', filter=Q(category__type='EXPENSE')),
            avg_exp=Avg('amount', filter=Q(category__type='EXPENSE')),
            cnt=Count('id')
        )

        inc = agg['inc'] or Decimal('0.00')
        exp = agg['exp'] or Decimal('0.00')

        total_agg = txs.aggregate(
            t_inc=Sum('amount', filter=Q(category__type='INCOME')),
            t_exp=Sum('amount', filter=Q(category__type='EXPENSE')),
        )

        income = total_agg['t_inc'] or Decimal('0.00')
        expense = total_agg['t_exp'] or Decimal('0.00')

        balance = income - expense

        completed_goals = []
        goals = SavingsGoal.objects.filter(user=user)

        for goal in goals:
            if goal.progress_percent >= 100:
                completed_goals.append(goal.title)
                goal.delete()

        context.update({
            'total_balance': balance,
            'month_income': inc,
            'month_expense': exp,
            'avg_expanse': agg['avg_exp'] or Decimal('0.00'),
            'tx_count': agg['cnt'],
            'recent_txs': txs.select_related('category')[:6],
            'budgets': Budget.objects.filter(user=user).select_related('category'),
            'goals': SavingsGoal.objects.filter(user=user)[:3],
            'completed_goals': completed_goals,
        })

        return context


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'finance/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        form = TransactionFilterForm(self.request.GET, user=self.request.user)

        if form.is_valid():
            type_val = form.cleaned_data.get('type')
            if type_val:
                queryset = queryset.filter(category__type=type_val)

            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)

            date_from = form.cleaned_data.get('date_from')
            if date_from:
                queryset = queryset.filter(date__gte=date_from)

            date_to = form.cleaned_data.get('date_to')
            if date_to:
                queryset = queryset.filter(date__lte=date_to)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TransactionFilterForm(self.request.GET, user=self.request.user)
        return context


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finance/transaction_form.html'
    success_url = reverse_lazy('finance:transaction_list')

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['user'] = self.request.user
        return kw

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finance/transaction_form.html'
    success_url = reverse_lazy('finance:transaction_list')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['user'] = self.request.user
        return kw


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    success_url = reverse_lazy('finance:transaction_list')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


@login_required
def chart_data_api(request):
    """Эндпоинт генерации JSON-датасетов для Chart.js"""
    user = request.user

    now = timezone.now()
    cats = Transaction.objects.filter(
        user=user, category__type='EXPENSE', date__year=now.year, date__month=now.month
    ).values('category__name').annotate(total=Sum('amount')).order_by('-total')

    months = Transaction.objects.filter(user=user).annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        inc=Sum('amount', filter=Q(category__type='INCOME')),
        exp=Sum('amount', filter=Q(category__type='EXPENSE')),
    ).order_by('month')

    return JsonResponse({
        'categories': {
            'labels':[c['category__name'] for c in cats],
            'data':[float(c['total']) for c in cats],
        },
        'dynamics': {
            'labels': [m['month'].strftime('%m.%Y') for m in months],
            'income': [float(m['inc'] or 0) for m in months],
            'expense': [float(m['exp'] or 0) for m in months],
        }
    })

class BudgetCreateView(CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'finance/budget_form.html'
    success_url = reverse_lazy('finance:dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SavingsGoalCreateView(CreateView):
    model = SavingsGoal
    form_class = SavingsGoalForm
    template_name = 'finance/savingsgoal_form.html'
    success_url = reverse_lazy('finance:dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'finance/budget_form.html'
    success_url = reverse_lazy('finance:dashboard')

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class SavingsGoalUpdateView(LoginRequiredMixin, UpdateView):
    model = SavingsGoal
    form_class = SavingsGoalForm
    template_name = 'finance/savingsgoal_form.html'
    success_url = reverse_lazy('finance:dashboard')

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)


@login_required
def delete_budget(request, pk):
    if request.method == 'POST':
        budget = get_object_or_404(Budget, id=pk, user=request.user)
        budget.delete()

    return redirect('finance:dashboard')


@login_required
def delete_goal(request, pk):
    if request.method == 'POST':
        goal = get_object_or_404(SavingsGoal, id=pk, user=request.user)
        goal.delete()

    return redirect('finance:dashboard')

