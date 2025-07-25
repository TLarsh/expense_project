from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from social_django.utils import psa

from expense.models.user import User
from expense.models.audit_log import AuditLog
from expense.serializers.user import UserSerializer
from expense.permissions import IsAdmin

class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        user = serializer.save(company=self.request.user.company)
        AuditLog.objects.create(
            user=self.request.user,
            company=self.request.user.company,
            action='create_user',
            changes={'new_user': user.username, 'role': user.role}
        )
        

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get('access_token')
        if not token:
            return Response({'error': 'Missing access token'}, status=400)
        user = self._get_or_create_user(token)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })

    @psa('social:complete')
    def _get_or_create_user(self, token):
        user = self.request.backend.do_auth(token)
        if user and user.is_active:
            return user
        raise Exception('Authentication failed')


class UpdateUserRoleView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    lookup_field = 'pk'