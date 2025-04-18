from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from expense.views.user import RegisterUserView, GoogleLoginView
from expense.views.expense import ExpenseListView, ExpenseUpdateView, ExpenseDeleteView

urlpatterns = [
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/google-login/', GoogleLoginView.as_view(), name='google_login'),
    path('api/expenses/', ExpenseListView.as_view(), name='expense_list'),
    path('api/expenses/<int:pk>/', ExpenseUpdateView.as_view(), name='expense_update'),
    path('api/expenses/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense_delete'),
]
