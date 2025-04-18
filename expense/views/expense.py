from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from expense.models.audit_log import AuditLog
from expense.models.expense import Expense
from expense.serializers.expense import ExpenseSerializer
from expense.permissions import IsManager, IsAdmin, IsEmployee

# List all expenses for the logged-in company
class ExpenseListView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsEmployee]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'category']

    def get_queryset(self):
        return Expense.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        # Ensure the user is from the correct company
        serializer.save(user=self.request.user, company=self.request.user.company)
        expense = serializer.save(user=self.request.user, company=self.request.user.company)
        AuditLog.objects.create(
            user=self.request.user,
            company=self.request.user.company,
            action='create_expense',
            changes={'title': expense.title, 'amount': str(expense.amount), 'category': expense.category}
        )

        

# Update an existing expense (Admin or Manager)
class ExpenseUpdateView(generics.UpdateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsManager]

    def get_queryset(self):
        return Expense.objects.filter(company=self.request.user.company)
    
    def perform_update(self, serializer):
            old_data = Expense.objects.get(pk=self.get_object().pk)
            updated_expense = serializer.save()
            AuditLog.objects.create(
                user=self.request.user,
                company=self.request.user.company,
                action='update_expense',
                changes={
                    'before': {
                        'title': old_data.title,
                        'amount': str(old_data.amount),
                        'category': old_data.category,
                    },
                    'after': {
                        'title': updated_expense.title,
                        'amount': str(updated_expense.amount),
                        'category': updated_expense.category,
                    }
                }
            )   

# Delete an existing expense (Admin only)
class ExpenseDeleteView(generics.DestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return Expense.objects.filter(company=self.request.user.company)

    def perform_destroy(self, instance):
        AuditLog.objects.create(
            user=self.request.user,
            company=self.request.user.company,
            action='delete_expense',
            changes={
                'deleted': {
                    'title': instance.title,
                    'amount': str(instance.amount),
                    'category': instance.category,
                }
            }
        )
        instance.delete()







# List Expenses

# GET /api/expenses/
# Returns a list of expenses for the company that the logged-in user belongs to.

# Create Expense

# POST /api/expenses/
# Allows the logged-in user to create an expense. The company and user are inferred from the logged-in user.

# Update Expense

# PUT /api/expenses/{id}/
# Only accessible by Manager or Admin. Updates an existing expense.

# Delete Expense

# DELETE /api/expenses/{id}/delete/
# Only accessible by Admin. Deletes an existing expense.