from celery import shared_task
from django.core.mail import send_mail
from expense.models.user import User
from expense.models.expense import Expense
from django.utils.timezone import now, timedelta

@shared_task
def send_weekly_expense_report():
    one_week_ago = now() - timedelta(days=7)
    admins = User.objects.filter(role='Admin')
    for admin in admins:
        expenses = Expense.objects.filter(company=admin.company, created_at__gte=one_week_ago)
        summary = '\n'.join([f"{e.title}: {e.amount}" for e in expenses]) or 'No expenses this week.'
        send_mail(
            'Weekly Expense Report',
            summary,
            'noreply@expenseapp.com',
            [admin.email]
        )