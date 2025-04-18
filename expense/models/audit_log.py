from django.db import models
from .user import User
from .company import Company

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    changes = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
