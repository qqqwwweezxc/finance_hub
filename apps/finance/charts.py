from datetime import date, datetime, timedelta

from django.db.models import F, Q, Sum
from django.db.models.functions import TruncMonth, TruncWeek, TruncYear
from django.utils import timezone

from .models import Transaction


CHART_PERIODS = {
    'day': {
        'label': 'День',
        'category_scope': 'за сегодня',
        'series_count': 14,
    },
    'week': {
        'label': 'Неделя',
        'category_scope': 'за текущую неделю',
        'series_count': 12,
    },
    'month': {
        'label': 'Месяц',
        'category_scope': 'за текущий месяц',
        'series_count': 12,
    },
    'year': {
        'label': 'Год',
        'category_scope': 'за текущий год',
        'series_count': 5,
    },
}

def _normalize_chart_period(period):
    if period in CHART_PERIODS:
        return period
    return "month"


def _week_start(value):
    return value - timedelta(days=value.weekday())


def _month_start(value):
    return date(value.year, value.month, 1)


def _shift_months(value, months):
    month = value.month - 1 + months
    year = value.year + month // 12
    month = month % 12 + 1
    return date(year, month, 1)


def _as_date(value):
    if isinstance(value, datetime):
        return value.date()
    return value


def _category_period_start(period, today):
    if period == "day":
        return today
    if period == "week":
        return _week_start(today)
    if period == "year":
        return date(today.year, 1, 1)
    return _month_start(today)


def _series_start(period, today):
    count = CHART_PERIODS[period]["series_count"]

    if period == "day":
        return today - timedelta(days=count - 1)
    if period == "week":
        return _week_start(today) - timedelta(weeks=count - 1)
    if period == "year":
        return date(today.year - count + 1, 1, 1)

    return _shift_months(_month_start(today), -(count - 1))


def _series_buckets(period, today):
    current = _series_start(period, today)

    if period == "day":
        while current <= today:
            yield current
            current += timedelta(days=1)
        return

    if period == "week":
        end = _week_start(today)
        while current <= end:
            yield current
            current += timedelta(weeks=1)
        return

    if period == "year":
        while current.year <= today.year:
            yield current
            current = date(current.year + 1, 1, 1)
        return

    end = _month_start(today)

    while current <= end:
        yield current
        current = _shift_months(current, 1)


def _period_trunc(period):
    if period == "day":
        return F("date")
    if period == "week":
        return TruncWeek("date")
    if period == "year":
        return TruncYear("date")

    return TruncMonth("date")


def _period_label(period, value):
    value = _as_date(value)

    if period == "day":
        return value.strftime("%d.%m")
    if period == "week":
        return f"с {value.strftime('%d.%m')}"
    if period == "year":
        return value.strftime("%Y")

    return value.strftime("%m.%Y")


def build_chart_data(user, params):
    today = timezone.localdate()

    fallback_period = _normalize_chart_period(params.get("period"))

    categories_period = _normalize_chart_period(
        params.get("categories_period") or fallback_period
    )

    dynamics_period = _normalize_chart_period(
        params.get("dynamics_period") or fallback_period
    )

    category_start = _category_period_start(categories_period, today)

    categories = (
        Transaction.objects
        .filter(
            user=user,
            category__type="EXPENSE",
            date__gte=category_start,
            date__lte=today,
        )
        .values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )

    series_start = _series_start(dynamics_period, today)

    dynamic_rows = (
        Transaction.objects
        .filter(
            user=user,
            date__gte=series_start,
            date__lte=today,
        )
        .annotate(period=_period_trunc(dynamics_period))
        .values("period")
        .annotate(
            inc=Sum("amount", filter=Q(category__type="INCOME")),
            exp=Sum("amount", filter=Q(category__type="EXPENSE")),
        )
        .order_by("period")
    )

    dynamic_totals = {
        _as_date(row["period"]): {
            "income": float(row["inc"] or 0),
            "expense": float(row["exp"] or 0),
        }
        for row in dynamic_rows
    }

    dynamic_labels = []
    dynamic_income = []
    dynamic_expense = []

    for bucket in _series_buckets(dynamics_period, today):
        totals = dynamic_totals.get(
            bucket,
            {
                "income": 0,
                "expense": 0,
            },
        )

        dynamic_labels.append(_period_label(dynamics_period, bucket))
        dynamic_income.append(totals["income"])
        dynamic_expense.append(totals["expense"])

    return {
        "categories": {
            "period": categories_period,
            "period_label": CHART_PERIODS[categories_period]["label"],
            "scope_label": CHART_PERIODS[categories_period]["category_scope"],
            "labels": [c["category__name"] for c in categories],
            "data": [float(c["total"] or 0) for c in categories],
        },
        "dynamics": {
            "period": dynamics_period,
            "period_label": CHART_PERIODS[dynamics_period]["label"],
            "labels": dynamic_labels,
            "income": dynamic_income,
            "expense": dynamic_expense,
        },
    }