from django.db import models
from .user import User
from .company import Company

class Expense(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='expenses', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses', db_index=True)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
