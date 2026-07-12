from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.db.models import Sum
from django.shortcuts import redirect
from django.contrib import messages
from django.db import transaction as db_transaction

from decimal import Decimal

from apps.finance.currency import get_exchange_rate, convert_money
from apps.finance.models import Transaction, Budget, SavingsGoal

from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('finance:dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("finance:dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        return response


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("finance:dashboard")

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = self.request.user

        old_currency = User.objects.get(pk=user.pk).currency
        new_currency = form.cleaned_data.get("currency")

        if old_currency != new_currency:
            try:
                rate = get_exchange_rate(old_currency, new_currency)

                with db_transaction.atomic():
                    transactions = Transaction.objects.filter(user=user)

                    for item in transactions:
                        item.amount = convert_money(item.amount, rate)
                        item.save(update_fields=["amount"])

                    budgets = Budget.objects.filter(user=user)

                    for budget in budgets:
                        budget.limit_amount = convert_money(budget.limit_amount, rate)
                        budget.save(update_fields=["limit_amount"])

                    goals = SavingsGoal.objects.filter(user=user)

                    for goal in goals:
                        goal.target_amount = convert_money(goal.target_amount, rate)
                        goal.current_amount = convert_money(goal.current_amount, rate)
                        goal.save(update_fields=["target_amount", "current_amount"])

                    form.instance.currency = new_currency
                    form.instance.save()

                messages.success(
                    self.request,
                    f"Валюта изменена с {old_currency} на {new_currency}. Все суммы пересчитаны."
                )

                return redirect(self.success_url)

            except Exception as error:
                form.add_error(
                    "currency",
                    f"Не удалось изменить валюту: {error}"
                )
                return self.form_invalid(form)

        messages.success(
            self.request,
            "Профиль успешно обновлён."
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        transactions = Transaction.objects.filter(user=user)

        total_income = transactions.filter(
            category__type="INCOME"
        ).aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0.00")

        total_expense = transactions.filter(
            category__type="EXPENSE"
        ).aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0.00")

        context["transactions_count"] = transactions.count()
        context["budgets_count"] = Budget.objects.filter(user=user).count()
        context["goals_count"] = SavingsGoal.objects.filter(user=user).count()
        context["total_income"] = total_income
        context["total_expense"] = total_expense
        context["profile_balance"] = total_income - total_expense

        return context