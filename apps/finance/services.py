from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone

from .models import Transaction, Budget, SavingsGoal


def get_month_range():
    today = timezone.now().date()
    month_start = today.replace(day=1)

    if today.month == 1:
        previous_month_start = today.replace(
            year=today.year - 1,
            month=12,
            day=1
        )
    else:
        previous_month_start = today.replace(
            month=today.month - 1,
            day=1
        )

    previous_month_end = month_start

    return today, month_start, previous_month_start, previous_month_end


def money(value):
    return value.quantize(Decimal("0.01"))


def get_financial_insights(user):
    insights = []

    today, month_start, previous_month_start, previous_month_end = get_month_range()

    current_expenses = Transaction.objects.filter(
        user=user,
        category__type="EXPENSE",
        date__gte=month_start,
        date__lte=today
    )

    previous_expenses = Transaction.objects.filter(
        user=user,
        category__type="EXPENSE",
        date__gte=previous_month_start,
        date__lt=previous_month_end
    )

    current_income = Transaction.objects.filter(
        user=user,
        category__type="INCOME",
        date__gte=month_start,
        date__lte=today
    ).aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0.00")

    current_expense_total = current_expenses.aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0.00")

    previous_expense_total = previous_expenses.aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0.00")


    if current_income > current_expense_total:
        difference = current_income - current_expense_total

        insights.append({
            "type": "success",
            "icon": "📈",
            "title": "Положительный баланс месяца",
            "text": f"Доходы превышают расходы на {money(difference)} {user.currency}."
        })

    elif current_expense_total > current_income and current_expense_total > 0:
        difference = current_expense_total - current_income

        insights.append({
            "type": "danger",
            "icon": "⚠️",
            "title": "Расходы выше доходов",
            "text": f"В этом месяце расходы больше доходов на {money(difference)} {user.currency}."
        })


    if previous_expense_total > 0:
        diff = current_expense_total - previous_expense_total
        percent = (diff / previous_expense_total) * 100

        if percent > 20:
            insights.append({
                "type": "warning",
                "icon": "🔥",
                "title": "Расходы выросли",
                "text": f"Вы тратите на {percent:.0f}% больше, чем в прошлом месяце."
            })

        elif percent < -20:
            insights.append({
                "type": "success",
                "icon": "💚",
                "title": "Расходы снизились",
                "text": f"Вы тратите на {abs(percent):.0f}% меньше, чем в прошлом месяце."
            })


    top_category = current_expenses.values(
        "category__name"
    ).annotate(
        total=Sum("amount")
    ).order_by("-total").first()

    if top_category:
        insights.append({
            "type": "info",
            "icon": "💰",
            "title": "Самая затратная категория",
            "text": f"{top_category['category__name']} — {money(top_category['total'])} {user.currency}."
        })


    budgets = Budget.objects.filter(
        user=user,
        category__type="EXPENSE"
    )

    for budget in budgets:
        if budget.is_exceeded:
            insights.append({
                "type": "danger",
                "icon": "🚨",
                "title": "Лимит превышен",
                "text": (
                    f"{budget.category.name}: "
                    f"{budget.current_spent:.0f} / {budget.limit_amount:.0f} {user.currency}."
                )
            })


    goals = SavingsGoal.objects.filter(user=user)

    for goal in goals:
        if 75 <= goal.progress_percent < 100:
            insights.append({
                "type": "success",
                "icon": "🎯",
                "title": "Цель почти достигнута",
                "text": f"{goal.title} выполнена на {goal.progress_percent}%."
            })


    if not insights:
        insights.append({
            "type": "info",
            "icon": "✨",
            "title": "Недостаточно данных",
            "text": "Добавьте несколько доходов и расходов, чтобы получить персональные инсайты."
        })

    return insights[:5]