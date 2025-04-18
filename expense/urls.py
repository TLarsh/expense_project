from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from expense.views.user import RegisterUserView, GoogleLoginView
from expense.views.expense import ExpenseListView, ExpenseUpdateView, ExpenseDeleteView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Expense API",
      default_version='v1',
      description="Multi-Tenant SaaS Expense Management API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/google-login/', GoogleLoginView.as_view(), name='google_login'),
    path('api/expenses/', ExpenseListView.as_view(), name='expense_list'),
    path('api/expenses/<int:pk>/', ExpenseUpdateView.as_view(), name='expense_update'),
    path('api/expenses/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense_delete'),
]
