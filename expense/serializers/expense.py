from rest_framework import serializers
from expense.models.expense import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'company', 'user', 'title', 'amount', 'category', 'created_at', 'updated_at']
        read_only_fields = ['company', 'user', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Add the current user and company to the validated data before saving
        validated_data['user'] = self.context['request'].user
        validated_data['company'] = self.context['request'].user.company
        return super().create(validated_data)
