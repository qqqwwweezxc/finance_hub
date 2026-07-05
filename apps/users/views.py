from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.db.models import Sum
from django.shortcuts import redirect

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